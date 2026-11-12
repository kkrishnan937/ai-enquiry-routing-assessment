from pathlib import Path
import json
from datetime import datetime, timezone

root=Path('results/acceptance-message-dry-run')
root.mkdir(parents=True,exist_ok=True)
request={'request_id':'PRACTICE-E002','status':'Accepted','receiving_team':'Waste Services','contact':'resident@example.invalid','acceptance_message_sent':False,'collection_date':None}
checks={'accepted_before_message':request['status']=='Accepted','contact_present':bool(request['contact']),'no_previous_acceptance_message':not request['acceptance_message_sent']}
assert all(checks.values())
message='Subject: Your missed-collection request PRACTICE-E002\n\nWaste Services has accepted your missed-collection request for investigation. A collection date has not been confirmed.\n\nPlease quote PRACTICE-E002 if you contact us about this request.\n'
(root/'message-preview.txt').write_text(message,encoding='utf-8')
log={'request_id':request['request_id'],'test_actor':'Unassigned practice sender','channel':'Local file only','recorded_at_utc':datetime.now(timezone.utc).isoformat(),'outcome':'SIMULATED_SEND_SAVED_LOCALLY','recipient':request['contact'],'actual_delivery':False,'message_file':'message-preview.txt'}
(root/'simulated-send-record.json').write_text(json.dumps(log,indent=2)+'\n',encoding='utf-8')
report='''# Acceptance-message dry run

Status: Local scripted dry run completed. No email was sent.

## Purpose

Exercise the proposed sequence before assigning business responsibility. The test actor is an unassigned practice sender.

## Inputs and checks

- Practice request E002 is marked accepted in the test input.
- Fictional contact uses example.invalid, which is not a deliverable recipient.
- The input declares no prior acceptance message.
- All three prerequisite checks passed.

## Observed outputs

- A message preview was saved, confirming investigation without promising a collection date.
- A simulated send record was saved with actor, time, channel and outcome.
- No delivery attempt was made. The outcome is explicitly a local simulation.

## Limits

Inputs were authored, not retrieved from an application. Contact presence does not prove valid contact details. The script does not verify real permissions, system acceptance, delivery, duplicate prevention under concurrent use, or failure handling. It does not measure a staff member preparing, sending and recording a message. No staff workload estimate or ownership decision follows from this run.

## Next review

The BA and stakeholders should review the message and recorded fields. A later observed task trial should use an agreed test participant, realistic application access and a non-production delivery mechanism; record active work and waiting separately. The final responsible role remains open.
'''
(root/'report.md').write_text(report,encoding='utf-8')
print('Prerequisites: 3/3 passed. Message preview and simulated record saved. Actual messages sent: 0.')
