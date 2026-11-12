"""Execute TC-03's required-representative checks against the interactive local app."""
import datetime as dt
import hashlib
import json
from pathlib import Path
from test_acceptance import Client

root = Path(__file__).resolve().parents[2]
passwords = json.loads((Path(__file__).parent / 'local-data' / 'credentials.json').read_text())
client = Client(8766).login('rep-a', passwords['rep-a'])
supervisor = Client(8766).login('supervisor-a', passwords['supervisor-a'])
code, before = supervisor.request('/api/enquiries')
assert code == 200
payload = dict(received='2026-11-12T09:00:00-06:00', message='TC-03 required-representative test: garbage cart not emptied.',
               missing='Collection address', last_action='Prepared test enquiry', next_action='Request collection address', follow_up='2026-11-13')
bad_code, bad_body = client.request('/api/enquiries', payload)
code, after_bad = supervisor.request('/api/enquiries')
assert code == 200
assert bad_code == 400, (bad_code, bad_body)
assert {r['id'] for r in before} == {r['id'] for r in after_bad}, 'Rejected save created an enquiry'
assert bad_body.get('error') == 'A named responsible representative is required'
payload['responsible'] = 'rep-a'
good_code, created = client.request('/api/enquiries', payload)
assert good_code == 201, (good_code, created)
code, retrieved = client.request('/api/enquiries/' + created['id'])
assert code == 200 and retrieved['responsible'] == 'rep-a'
code, after_good = supervisor.request('/api/enquiries')
assert code == 200 and {r['id'] for r in after_good} - {r['id'] for r in after_bad} == {created['id']}
report = dict(executed_utc=dt.datetime.now(dt.timezone.utc).isoformat(), identity='rep-a',
              evidence_identity='supervisor-a for before/after full record list',
              environment='existing local application on port 8766; separate authenticated HTTP sessions, not browser submission',
              application_sha256=hashlib.sha256((Path(__file__).parent/'app.py').read_bytes()).hexdigest(),
              rejected_request=payload | {'responsible': '(omitted in rejected request)'},
              rejected_response=dict(status=bad_code, body=bad_body),
              records_before=len(before), records_after_rejected_save=len(after_bad),
              accepted_status=good_code, created_reference=created['id'], retrieved_responsible=retrieved['responsible'],
              outcome='PASS for missing-representative rejection, no creation on rejection, and valid save/retrieval',
              remaining='TC-03 clarification and cover responsibility-retention steps not executed in this run')
destination = root / 'results' / 'tracking-prototype' / ('TC03-required-' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
destination.write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report, indent=2))
print('Evidence:', destination)
