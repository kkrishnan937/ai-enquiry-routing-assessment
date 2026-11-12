# Tracking prototype — automated acceptance results

Run: 20261111T214527349490Z
Executed UTC: 2026-11-11T21:45:27.349490+00:00
Python: 3.12.7
Application SHA-256: `349d5ac4b0730a9550ec98bc5bb9191d5b8b9dc0cab72e4dda9fd7bb4d0468c8`
Test SHA-256: `1580de5b5d27f7192599dfcb953f078f9a44ab6def0797d25f76f3a04e8215f5`

Environment: local subprocess HTTP server, isolated temporary SQLite database per case; authenticated sessions; controlled test date.

| Case | Automated outcome |
|---|---|
| TC-01 | ERROR |
| TC-02 | ERROR |
| TC-03 | ERROR |
| TC-04 | ERROR |
| TC-05 | ERROR |
| TC-06 | ERROR |
| TC-07 | ERROR |



## Limits

- HTTP automation; browser interaction and visual layout not assessed
- Synthetic data only; no municipal system or operational approval
- No Azure Pipeline executed; tests ran locally
- No timed jobs implemented; overdue observation covers controlled date-boundary checks only

These results cover implemented HTTP assertions, not completed manual sign-off of every test-case step. Temporary test databases and passwords were removed after execution. Failed-run details, if any, are retained in results.json.
