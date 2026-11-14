"""One development-example smoke check; not model evaluation."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import time
import urllib.request

root = Path(__file__).resolve().parents[2]
folder = Path(__file__).parent
opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def request(path, body=None):
    raw = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request('http://127.0.0.1:11434' + path, data=raw,
                                 headers={'Content-Type': 'application/json'})
    with opener.open(req, timeout=180) as response:
        return json.load(response)


model = 'qwen2.5:3b'
prompt_path = folder / 'classification-prompt.txt'
prompt = prompt_path.read_text(encoding='utf-8')
example = json.loads((root / 'data/classification-development.json').read_text())['examples'][0]
tags = request('/api/tags')
installed = next(m for m in tags['models'] if m['name'] == model)
schema = {'type': 'object', 'properties': {'type': {'enum': ['missed_collection', 'reported_dumped_waste', 'other', None]},
                                         'review_required': {'type': 'boolean'}},
          'required': ['type', 'review_required'], 'additionalProperties': False}
started = time.perf_counter()
response = request('/api/chat', {'model': model, 'messages': [{'role': 'system', 'content': prompt},
                                                           {'role': 'user', 'content': example['text']}],
                               'stream': False, 'format': schema,
                               'options': {'temperature': 0, 'seed': 42, 'num_ctx': 2048, 'num_predict': 128}})
elapsed = time.perf_counter() - started
prediction = json.loads(response['message']['content'])
assert set(prediction) == {'type', 'review_required'}
assert type(prediction['review_required']) is bool
assert prediction['type'] in ('missed_collection', 'reported_dumped_waste', 'other', None)
assert (prediction['type'] is None) == prediction['review_required']
report = {'executed_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
          'scope': 'one known development example; verifies execution/format, not accuracy or advantage',
          'ollama_version': request('/api/version'), 'model': installed,
          'active_runners': request('/api/ps'),
          'prompt_sha256': hashlib.sha256(prompt_path.read_bytes()).hexdigest(),
          'input': {'id': example['id'], 'text': example['text']},
          'settings': {'temperature': 0, 'seed': 42, 'num_ctx': 2048, 'num_predict': 128},
          'response': response, 'prediction': prediction, 'wall_seconds': elapsed,
          'valid_output': True,
          'matches_development_label': prediction['type'] == example['expected_type'] and prediction['review_required'] == example['review_required']}
directory = root / 'results/classification'
directory.mkdir(exist_ok=True)
destination = directory / ('local-smoke-' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
destination.write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps({'prediction': prediction, 'valid_output': True, 'wall_seconds': round(elapsed, 2),
                  'matches_development_label': report['matches_development_label']}, indent=2))
print('Evidence:', destination)
