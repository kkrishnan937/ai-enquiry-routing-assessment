# Tracking prototype — automated acceptance results

Run: 20261111T214650602254Z
Executed UTC: 2026-11-11T21:46:50.602254+00:00
Python: 3.12.7
Application SHA-256: `349d5ac4b0730a9550ec98bc5bb9191d5b8b9dc0cab72e4dda9fd7bb4d0468c8`
Test SHA-256: `1580de5b5d27f7192599dfcb953f078f9a44ab6def0797d25f76f3a04e8215f5`

Environment: local subprocess HTTP server, isolated temporary SQLite database per case; authenticated sessions; controlled test date.

| Case | Automated outcome |
|---|---|
| TC-01 | PASS |
| TC-02 | PASS |
| TC-03 | PASS |
| TC-04 | PASS |
| TC-05 | PASS |
| TC-06 | PASS |
| TC-07 | PASS |

### TC-01

Two references searched and retrieved after process restart using unchanged database; timestamps and both messages unchanged and separate. No email integration exists. Detail page returns HTML.

### TC-02

Address received; other missing detail retained; three messages preserved; actor/time history available; responsible rep unchanged and state remains Open. No referral integration exists.

### TC-03

Ownerless creation rejected without persistence; requests, resident reply and cover preserve rep-a; rep-b stored separately as cover.

### TC-04

Blank/impossible dates rejected on create and update; valid changed date persisted. Isolated clock advanced Nov11 to Nov14 through process restart; record remains Open, rep-a responsible, overdue true. No scheduler or timed jobs implemented; no indefinite behaviour guarantee.

### TC-05

Self-assignment denied; supervisor cover grants read/update; removal revokes same-session API and page access; stale update rejected; original responsibility retained and both cover events stored.

### TC-06

Responsible rep, named cover and supervisor can read/update. Unrelated rep cannot list/search/read messages/history or write; signed-out direct reads/writes return 401. Denied changes not persisted.

### TC-07

Field/cover events retain actor, old/new values and UTC timestamps. Ordinary-user history POST/PATCH/DELETE denied. History persists through two process restarts. Non-supervisor/incomplete transfers denied; complete supervisor transfer and reason retained; receiving rep gains access and former rep loses it.

## Limits

- HTTP automation; browser interaction and visual layout not assessed
- Synthetic data only; no municipal system or operational approval
- No Azure Pipeline executed; tests ran locally
- No timed jobs implemented; overdue observation covers controlled date-boundary checks only

These results cover implemented HTTP assertions, not completed manual sign-off of every test-case step. Temporary test databases and passwords were removed after execution. Failed-run details, if any, are retained in results.json.
