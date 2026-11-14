"""Single frozen paired evaluation. Refuses missing review/freeze evidence or changed approach."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import statistics
import time

from keyword_baseline import classify
from run_ai_development import MODEL, SETTINGS, SCHEMA, request, valid, outcome, metrics

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / 'data/classification-evaluation'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    freeze = json.loads((DATA / 'evaluation-freeze.json').read_text())
    for name, expected in freeze['dataset_hashes'].items():
        assert digest(DATA / name) == expected, 'Frozen dataset/review changed: ' + name
    approach = json.loads((DATA / 'frozen-approach/manifest.json').read_text())
    for item in approach['files']:
        assert digest(ROOT / item['source']) == item['sha256'], 'Approach changed: ' + item['source']
    assert SETTINGS == approach['settings']
    assert MODEL == approach['model']
    installed = next(m for m in request('/api/tags')['models'] if m['name'] == MODEL)
    assert installed['digest'] == approach['model_digest'], 'Model digest changed'
    inputs = json.loads((DATA / 'inputs.json').read_text())['examples']
    labels = {r['id']: r for r in json.loads((DATA / 'reviewed-labels.json').read_text())['examples']}
    assert set(labels) == {r['id'] for r in inputs} and len(inputs) == freeze['retained_count']
    assert freeze['status'] == 'frozen_before_predictions'
    output = ROOT / 'results/classification/held-out-final'
    if output.exists():
        raise SystemExit('Final run directory exists. Do not overwrite or silently rerun held-out evaluation.')
    output.mkdir()
    prompt = (DATA / 'frozen-approach/classification-prompt.txt').read_text(encoding='utf-8')
    report = {'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'status': 'running',
              'scope': 'Frozen synthetic held-out text, authored after development choices; not real-world validation.',
              'model': installed, 'settings': SETTINGS, 'schema': SCHEMA, 'ollama_version': request('/api/version'),
              'freeze': freeze, 'runner_sha256': digest(Path(__file__)), 'predictions': []}

    def save():
        (output / 'predictions.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

    save()
    for example in inputs:
        expected = labels[example['id']]
        baseline = classify(example['text'])
        row = {'id': example['id'], 'text': example['text'], 'expected_type': expected['expected_type'],
               'expected_review': expected['review_required'], 'review_group': expected['review_group'],
               'baseline': {k: baseline[k] for k in ('type', 'review_required')},
               'baseline_patterns': baseline['matched_patterns'], 'ai': None}
        clock = time.perf_counter()
        try:
            response = request('/api/chat', {'model': MODEL, 'messages': [{'role': 'system', 'content': prompt},
                                                                        {'role': 'user', 'content': example['text']}],
                                           'stream': False, 'format': SCHEMA, 'options': SETTINGS})
            row['raw_response'] = response
            parsed = json.loads(response['message']['content'])
            if not response.get('done') or not valid(parsed):
                raise ValueError('Incomplete or invalid output')
            row['ai'] = parsed
        except Exception as exc:
            row['error'] = {'kind': type(exc).__name__, 'message': str(exc)}
        row['wall_seconds'] = time.perf_counter() - clock
        report['predictions'].append(row)
        save()
        print(f"{len(report['predictions'])}/{len(inputs)} processed", flush=True)
    rows = report['predictions']
    report['summary'] = {method: metrics(rows, method) for method in ('baseline', 'ai')}
    b, a = report['summary']['baseline'], report['summary']['ai']
    report['meets_predefined_comparison_rule'] = (
        a['correct_automatic_classifications'] > b['correct_automatic_classifications'] and
        a['correct_review_flags'] >= b['correct_review_flags'] and
        a['forced_types_on_review_cases'] <= b['forced_types_on_review_cases'] and
        a['invalid_outputs'] <= b['invalid_outputs'])
    report['runtime'] = {'total_request_seconds': sum(r['wall_seconds'] for r in rows),
                         'median_request_seconds': statistics.median(r['wall_seconds'] for r in rows),
                         'min_seconds': min(r['wall_seconds'] for r in rows), 'max_seconds': max(r['wall_seconds'] for r in rows)}
    report['active_runners_after'] = request('/api/ps')
    report['completed_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    report['status'] = 'complete'
    save()
    lines = ['# Frozen held-out comparison — initial result', '',
             f"One keyword baseline and one local AI model on {len(inputs)} frozen synthetic texts. No retries or post-result tuning. Two of forty candidates excluded for overlap before scoring.", '',
             '| Measure | Keyword baseline | AI |', '|---|---:|---:|']
    for key in ('correct_automatic_classifications', 'coverage_count', 'correct_review_flags', 'forced_types_on_review_cases', 'invalid_outputs', 'matching_outcomes'):
        lines.append(f'| {key} | {b[key]} | {a[key]} |')
    lines += ['', f"Clear-type denominator: {b['classifiable_total']}. Review-expected denominator: {b['review_expected_total']}. Actual subset composition is in structured evidence.", '',
              f"Meets predefined paired comparison rule: **{report['meets_predefined_comparison_rule']}**.", '',
              '## Evidence and limits', '',
              'Per-example raw responses, confusion tables, per-type/subset counts, hashes, runtime and freeze provenance are in predictions.json. Labels were reviewed before predictions. Synthetic data was authored by the same assistant involved in development; the second-pass AI review is not independent domain validation. Semantic similarity and generation bias remain limitations despite the scenario-family and duplicate check. No claims about actual demand, operational accuracy, savings or statistical superiority follow. Do not tune on these outputs and call a later run unseen.', '',
              f"AI request total: {report['runtime']['total_request_seconds']:.2f}s; median: {report['runtime']['median_request_seconds']:.2f}s. Includes caching/load effects; not staff time or service response time."]
    (output / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'summary': report['summary'], 'meets_rule': report['meets_predefined_comparison_rule']}, indent=2))
    print('Report:', output / 'report.md')


if __name__ == '__main__':
    main()
