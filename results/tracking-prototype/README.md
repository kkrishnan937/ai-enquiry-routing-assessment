# Tracking prototype — execution summary

Prepared: November 11, 2026

Update November 12: [Consolidated test summary](../../docs/06-evaluation/tracking-prototype-test-summary.md) covers the later assisted walkthrough, targeted negative checks, copied-environment checks and open findings. The sections below retain the initial automated-run context.

## Latest successful automated execution

Superseding run: [November 12 version 0.1.1 retest](../archive/tracking-prototype/20261112T224218784803Z/report.md), **8 of 8 groups passed**, including the timestamp whitespace/error-message regression. [Structured evidence](../archive/tracking-prototype/20261112T224218784803Z/results.json) identifies the tested source hashes. The November 11 run below is retained as the original baseline.

- Run: [20261111T214650602254Z report](../archive/tracking-prototype/20261111T214650602254Z/report.md).
- Machine-readable evidence, source hashes, outcomes and observations: [results.json](../archive/tracking-prototype/20261111T214650602254Z/results.json).
- Result: **7 of 7 automated HTTP test groups passed**, mapped to TC-01–TC-07.
- Environment: local Python HTTP application processes; isolated SQLite databases; generated authenticated test accounts. Persistence checks stopped and restarted actual application processes using the same database.
- Code and reproduction instructions: [application guide](../../prototype/tracking/README.md).

## Initial failures and corrections

Two earlier runs are retained: [first attempt](../archive/tracking-prototype/20261111T214527349490Z/results.json) and [second attempt](../archive/tracking-prototype/20261111T214623165290Z/results.json). Both reported startup errors because the restricted execution environment denied connections to localhost. They are environment errors, not evidence that the seven business behaviours failed.

The successful run used permission to connect to the local application. During investigation, the runner was changed to bypass HTTP proxies for localhost and reliably clean up child processes on setup failure. Database connections were also changed to close explicitly after each operation; the initial failed cleanup had exposed Windows file-lock behaviour. Do not report the failed runs as passed or remove them from the evidence trail.

The first attempt's generic report footer incorrectly says temporary data and passwords were removed; cleanup errors mean that statement is not established for that attempt. Later cleanup handling was corrected. None of the evidence files intentionally contains test passwords; generated credentials are excluded from source control.

## Browser smoke check

A separate interactive local instance was opened at <http://127.0.0.1:8766>. Using supervisor-a, the browser successfully signed in, saved a sample enquiry and reopened its detail page. The displayed reference was ENQ-43BE1F6D79A9; responsibility was rep-a, cover was None, missing information was Collection address, and follow-up date was November 12, 2026. Correspondence, supervisor controls and creation history were present in the page's accessible content. The visible upper record layout was inspected.

This was a limited smoke check, not full browser execution of TC-01–TC-07. The interactive database is separate from the temporary databases used by the automated suite. Credentials are in the ignored local-data directory; do not publish them.

## Conclusions and limits

The local prototype now has observed behaviour beyond configuration declarations. The automated assertions cover persistence, missing-information updates, retained responsibility, date validation, cover, access denial and history including supervisor transfer. Detailed observations and tested source hashes are in the successful run.

- Full manual business acceptance, accessibility review and comprehensive security testing have not occurred.
- Missing-information updates are manual text changes; the application does not infer completion from an address.
- Supervisor confirmation of receiving-representative availability is an assertion, not a separate recipient approval workflow.
- Concurrent stale edits, direct database modification and deployment security remain limitations documented in the application guide.
- No outbound email, automatic referral, closure, timed reminders or AI component is implemented.
- An optional Azure pipeline file exists but has not been configured or run. No Azure Boards updates or GitHub uploads were performed in this build step.
- These results establish only the tested local prototype behaviour. They do not verify a municipality's system, approve a permitted operational method or release the held guidance.
