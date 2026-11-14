"""Paired development diagnostics, never held-out evaluation. Standard library only."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import statistics
import time
import urllib.request

from keyword_baseline import classify, VERSION

ROOT = Path(__file__).resolve().parents[2]
FOLDER = Path(__file__).parent
MODEL = 'qwen2.5:3b'
SETTINGS = {'temperature': 0, 'seed': 42, 'num_ctx': 2048, 'num_predict': 128}
SCHEMA = {'type': 'object', 'properties': {
    'type': {'enum': ['missed_collection', 'reported_dumped_waste', 'other', None]},
    'review_required': {'type': 'boolean'}},
    'required': ['type', 'review_required'], 'additionalProperties': False}
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def request(path, body=None):
    req = urllib.request.Request('http://127.0.0.1:11434' + path,
                                 data=None if body is None else json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json'})
    with OPENER.open(req, timeout=180) as response:
        return json.load(response)


def valid(value):
    return (isinstance(value, dict) and set(value) == {'type', 'review_required'} and
            type(value['review_required']) is bool and
            value['type'] in ('missed_collection', 'reported_dumped_waste', 'other', None) and
            (value['type'] is None) == value['review_required'])


def outcome(prediction):
    if prediction is None:
        return 'invalid'
    return prediction['type'] or 'review'


def metrics(rows, approach):
    clear = [r for r in rows if not r['expected_review']]
    review = [r for r in rows if r['expected_review']]
    typed = [r for r in clear if r[approach] is not None and not r[approach]['review_required']]
    correct = sum(r[approach] is not None and r[approach]['type'] == r['expected_type'] and
                  r[approach]['review_required'] == r['expected_review'] for r in rows)
    correct_clear = sum(r[approach] is not None and r[approach]['type'] == r['expected_type'] and
                        not r[approach]['review_required'] for r in clear)
    result = {'total': len(rows), 'matching_outcomes': correct,
              'classifiable_total': len(clear), 'correct_automatic_classifications': correct_clear,
              'coverage_count': len(typed), 'coverage_rate': len(typed) / len(clear) if clear else None,
              'accuracy_among_classified': correct_clear / len(typed) if typed else None,
              'overall_classifiable_success': correct_clear / len(clear) if clear else None,
              'review_expected_total': len(review),
              'correct_review_flags': sum(outcome(r[approach]) == 'review' for r in review),
              'forced_types_on_review_cases': sum(outcome(r[approach]) not in ('review', 'invalid') for r in review),
              'invalid_outputs': sum(r[approach] is None for r in rows)}
    result['review_subsets'] = {group: {'total': sum(r['review_group'] == group for r in review),
                                       'correct_flags': sum(r['review_group'] == group and outcome(r[approach]) == 'review' for r in review)}
                                for group in ('unclear', 'mixed')}
    result['per_type'] = {kind: {'total': sum(r['expected_type'] == kind for r in clear),
                                 'correct': sum(r['expected_type'] == kind and outcome(r[approach]) == kind for r in clear)}
                          for kind in ('missed_collection', 'reported_dumped_waste', 'other')}
    table = {}
    for row in rows:
        expected = row['expected_type'] or 'review'
        predicted = outcome(row[approach])
        table.setdefault(expected, {})[predicted] = table.setdefault(expected, {}).get(predicted, 0) + 1
    result['confusion_counts'] = table
    return result


def main():
    source = ROOT / 'data/classification-development.json'
    dataset = json.loads(source.read_text(encoding='utf-8'))
    assert dataset['split'] == 'development', 'Development runner must not use held-out data'
    prompt_path = FOLDER / 'classification-prompt.txt'
    prompt = prompt_path.read_text(encoding='utf-8')
    started = dt.datetime.now(dt.timezone.utc)
    destination = ROOT / 'results/classification' / ('ai-development-' + started.strftime('%Y%m%dT%H%M%S%fZ'))
    destination.mkdir(parents=True)
    installed = next(m for m in request('/api/tags')['models'] if m['name'] == MODEL)
    paths = {'dataset': source, 'prompt': prompt_path, 'baseline': FOLDER / 'keyword_baseline.py',
             'runner': Path(__file__), 'guide': ROOT / 'data/labelling-guide.md'}
    report = {'started_utc': started.isoformat(), 'status': 'running',
              'scope': 'development only; no held-out material; not a final advantage claim',
              'model': installed, 'ollama_version': request('/api/version'), 'settings': SETTINGS,
              'baseline_version': VERSION, 'schema': SCHEMA,
              'hashes': {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in paths.items()},
              'examples_sent': 'Only enquiry text as user content; fixed system prompt and schema. No expected labels, annotations or identifiers sent.',
              'predictions': []}

    def save():
        (destination / 'predictions.json').write_text(json.dumps(report, indent=2), encoding='utf-8')

    save()
    for example in dataset['examples']:
        base = classify(example['text'])
        row = {'id': example['id'], 'text': example['text'], 'expected_type': example['expected_type'],
               'expected_review': example['review_required'], 'review_group': example['review_group'],
               'baseline': {'type': base['type'], 'review_required': base['review_required']},
               'baseline_patterns': base['matched_patterns'], 'ai': None}
        clock = time.perf_counter()
        try:
            response = request('/api/chat', {'model': MODEL, 'messages': [{'role': 'system', 'content': prompt},
                                                                        {'role': 'user', 'content': example['text']}],
                                           'stream': False, 'format': SCHEMA, 'options': SETTINGS})
            row['raw_response'] = response
            parsed = json.loads(response['message']['content'])
            if not response.get('done') or not valid(parsed):
                raise ValueError('Incomplete response or inconsistent output schema')
            row['ai'] = parsed
        except Exception as exc:
            row['error'] = {'kind': type(exc).__name__, 'message': str(exc)}
        row['wall_seconds'] = time.perf_counter() - clock
        report['predictions'].append(row)
        save()
        print(f"{len(report['predictions'])}/{len(dataset['examples'])}: {example['id']} -> {outcome(row['ai'])}", flush=True)

    rows = report['predictions']
    report['summary'] = {approach: metrics(rows, approach) for approach in ('baseline', 'ai')}
    report['runtime'] = {'total_seconds': sum(r['wall_seconds'] for r in rows),
                         'median_seconds_per_request': statistics.median(r['wall_seconds'] for r in rows),
                         'min_seconds': min(r['wall_seconds'] for r in rows), 'max_seconds': max(r['wall_seconds'] for r in rows),
                         'note': 'Sequential local requests; includes any load/warmup; shared prompt may be cached. Not staff effort or production latency.'}
    report['active_runners_after'] = request('/api/ps')
    report['completed_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
    report['status'] = 'complete'
    save()
    baseline, ai = report['summary']['baseline'], report['summary']['ai']
    lines = ['# Paired development diagnostics — keyword rules and local AI', '',
             '**Development data only. Not held-out performance or proof of business value.**', '',
             f'Model: {MODEL}; baseline version: {VERSION}. Both used the same {len(rows)} enquiry texts.', '',
             '| Measure | Keyword rules | AI |', '|---|---:|---:|']
    for key in ('matching_outcomes', 'correct_automatic_classifications', 'coverage_count', 'correct_review_flags', 'forced_types_on_review_cases', 'invalid_outputs'):
        lines.append(f'| {key} | {baseline[key]} | {ai[key]} |')
    lines += ['', 'Clear-type denominator: 15. Review-expected denominator: 5. See structured evidence for per-type, unclear/mixed subsets and full confusion counts.', '',
              '## AI disagreements', '', '| Example | Expected | AI output |', '|---|---|---|']
    disagreements = [r for r in rows if outcome(r['ai']) != (r['expected_type'] or 'review')]
    lines += [f"| {r['id']} | {r['expected_type'] or 'review'} | {outcome(r['ai'])} |" for r in disagreements]
    if not disagreements:
        lines += ['No AI disagreements on this development pass.']
    lines += ['', '## Runtime and limits', '', f"Total request wall time: {report['runtime']['total_seconds']:.2f}s; median: {report['runtime']['median_seconds_per_request']:.2f}s.", '',
              'Rules were written with development data visible; the prompt uses the reviewed guide. Development labels were assistant-authored and user-reviewed with coaching, not independent domain ground truth. No fine-tuning or weight training was performed. Output schema enforcement does not guarantee semantic correctness. No prompt/rule change was made during this run and no failed output was retried or silently replaced. Preserve this run if later development changes occur. No paid inference API was used; electricity, hardware and staff effort are not costed. No held-out data was generated or read.']
    (destination / 'report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('Report:', destination / 'report.md')


if __name__ == '__main__':
    main()
