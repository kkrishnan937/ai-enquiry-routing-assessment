# Tracking prototype: test summary

Review date: November 12, 2026  
Version: Local application 0.1.0  
Application SHA-256: `349d5ac4b0730a9550ec98bc5bb9191d5b8b9dc0cab72e4dda9fd7bb4d0468c8`  
Prepared by: BA  
Status: Supporting prototype accepted for learning in conversation; operational publication remains on hold

Current position: November 14: the timestamp fix passed regression, the clean TC-01 repeat passed, and the user agreed to accept this supporting prototype for its learning purpose with limitations. Original review fields and earlier pending findings below are historical; they are not current open blockers. This acceptance does not confer municipal approval, permit live data or establish completion of the separate AI assessment. See the [final recommendation](final-recommendation.md) for the assessment decision.

## Retest update: timestamp correction

F-01 is corrected in local version 0.1.1. Surrounding whitespace is trimmed before validating and storing the received timestamp. Blank/non-text, malformed or impossible, and missing-time-zone inputs now receive distinct errors.

[Retest run 20261112T224218784803Z](../../results/archive/tracking-prototype/20261112T224218784803Z/report.md) passed **8 of 8 automated groups**: the seven original groups plus the new F-01 regression. The regression checks whitespace acceptance, persistence after restart, accurate rejection messages and absence of records created by invalid requests. Source hashes are in the run evidence. The version 0.1.0 walkthrough findings below remain historical evidence; F-01 no longer remains open for the tested 0.1.1 behaviour. Business acceptance and the clean manual TC-01 repeat remain outstanding.

## Assessment

### Clean TC-01 repeat completed: November 12

The fresh-fixture assisted repeat passed on version 0.1.1. ENQ-057CABB1757A (garbage) and ENQ-3207A18BD57D (recycling) each contained their own incoming enquiry and outgoing request. After stopping the actual interactive application process and restarting with the same database, the assistant signed in as rep-a, searched each exact reference in the browser and inspected both records. Full HTTP comparisons confirmed all saved values and histories matched the [before snapshot](../../results/tracking-prototype/TC01-clean-2026-11-12-before.json); [after evidence and outcome](../../results/tracking-prototype/TC01-clean-2026-11-12-after.json) are retained. Minor input wording/whitespace differences are disclosed in that evidence and do not affect persistence or correspondence association.

This resolves the previously outstanding clean manual TC-01 repeat. Earlier references below to that repeat being outstanding describe the position before this update. Prototype business acceptance remains pending; operational publication remains on hold.

The tested local prototype demonstrates enquiry persistence, manual tracking updates, retained responsibility, supervisor-controlled cover and transfers, application-side access controls and retained change history. Seven automated HTTP test groups passed on November 11. Assisted browser checks and targeted HTTP checks on November 11–12 provide additional evidence.

This is not an unqualified statement that all manual cases passed. TC-01's manual fixture contained a corrected data-entry error. Some checks were completed through automation rather than repeated in the browser. User-reported observations and assistant-inspected results are distinguished below. No Azure pipeline ran, no real municipal application was inspected, and operational publication remains on hold.

## Scope and method

Requirements: [TR-01–TR-07 and BR-01](../05-requirements/tracking-prototype-requirements.md). Test design: [TC-01–TC-07](tracking-prototype-test-cases.md).

The walkthrough used authenticated local accounts, synthetic enquiries and SQLite persistence. Negative requests were submitted using separate authenticated HTTP sessions; absence of authentication was tested separately. Overdue and later history-restart checks used temporary copies of the working database, with actual application processes. Only the overdue check used a controlled application date. Computer time was not altered.

Primary automated baseline: [run report](../../results/archive/tracking-prototype/20261111T214650602254Z/report.md) and [structured results](../../results/archive/tracking-prototype/20261111T214650602254Z/results.json). Initial environment failures remain recorded in the [execution overview](../../results/tracking-prototype/README.md).

## Results by case

| Case | Observed result | Evidence and qualification |
|---|---|---|
| TC-01: persistence and correspondence | Both walkthrough references retrieved after actual application restart; contents retained. Automated clean-fixture check passed. | [Assisted execution](../../results/tracking-prototype/manual-TC01-2026-11-11.md). Manual fixture deviation: recycling message initially entered on garbage record; correction preserved. Clean manual repeat remains outstanding. |
| TC-02: partial information | Address saved, missed date remained outstanding, correspondence and history retained; rep-a unchanged. | [Manual execution](../../results/tracking-prototype/manual-TC02-2026-11-11.md). Pass for observed scenario; updates are manual, not automatically inferred. |
| TC-03: named responsibility | Missing representative rejected; no record created; valid retry saved. Cover assignment retained rep-a separately from rep-b. | [Required-representative check](../../results/tracking-prototype/TC03-required-20261112T205850562579Z.json). Clarification retention observed on earlier TC-02 record and automated TC-03; full original manual sequence was not repeated on this single fixture. |
| TC-04: follow-up date | Browser blocked blank input (user reported); server rejected blank/impossible dates without changes. Valid amendment saved with history. Controlled overdue date displayed warning without closure or reassignment. | [Invalid-date checks](../../results/tracking-prototype/TC04-invalid-dates-20261112T221815071307Z.json), [overdue check](../../results/tracking-prototype/TC04-overdue-20261112T222300029896Z.json). Assistant inspected browser history: rep-a changed Nov13 → Nov14 at 2026-11-12T22:20:21.291780+00:00. No separate screenshot retained. No timed jobs implemented. |
| TC-05: absence cover | Supervisor assignment/removal recorded; rep-b updated next action while assigned; responsibility remained rep-a. After removal, read and update denied; rep-a could still open the record (user reported). | [Denied update](../../results/tracking-prototype/cover-denied-update-20261112T214522253824Z.json); browser history observations listed below. Self-assignment denial and original-session revocation were covered by automated TC-05, not independently repeated in the walkthrough. |
| TC-06: access | Unrelated rep-c search returned no result and direct link denied (user reported). Direct update rejected; signed-out read/update rejected, with record/history unchanged. | [Unrelated update](../../results/tracking-prototype/TC06-unrelated-update-20261112T223135778462Z.json), [signed-out checks](../../results/tracking-prototype/TC06-signed-out-20261112T223318684843Z.json). Authorised updates by each role and protected correspondence/history reads were covered in automated TC-06. Not a comprehensive security assessment. |
| TC-07: transfer and history | Supervisor transfer rep-a → rep-c retained reason, actor and time. Missing reason/confirmation and ordinary-user transfer rejected. Ordinary-user history mutations rejected. Copied-environment restart retained all six events. | [Rejected transfers](../../results/tracking-prototype/TC07-rejected-transfers-20261112T223733606317Z.json), [history protection and restart](../../results/tracking-prototype/TC07-history-20261112T223841568398Z.json). Read/write application-route protection does not establish tamper-proof database storage. Cover-user history mutation was covered by automated TC-07. |

### Shared walkthrough record and history

Enquiry ENQ-94C05BDDAD83 was used across cases; this differs from independent fresh manual fixtures. Assistant browser inspections observed:

- supervisor-a assigned rep-b as cover at 2026-11-12T21:05:19.981602+00:00.
- rep-b changed next action at 2026-11-12T21:27:53.160605+00:00.
- supervisor-a removed cover at 2026-11-12T21:42:06.443501+00:00.
- rep-a changed follow-up Nov13 → Nov14 at 2026-11-12T22:20:21.291780+00:00.
- supervisor-a transferred responsibility rep-a → rep-c, reason “Workload redistribution,” at 2026-11-12T22:35:59.238764+00:00.

The later restart evidence retains these events. rep-c was unrelated during the earlier TC-06 checks; after the authorised transfer, rep-c became responsible. Its earlier denial must not be described as its current access status.

## Findings and remaining work

| ID | Finding / limitation | Recommended disposition |
|---|---|---|
| F-01 | Leading tab before a valid received timestamp caused rejection with misleading time-zone wording. Reproduced during TC-02 setup; trimming the input allowed save. | Open usability defect: accept harmless surrounding whitespace or provide an accurate format error. Add regression coverage before claiming fixed. No code change made. |
| F-02 | Manual TC-01 data entry attached recycling text to an open garbage record. Correction retained in history. | Test-data deviation, not an established application association defect. Repeat a clean manual fixture if unqualified manual completion is required. |
| F-03 | Some walkthrough observations are user-reported; browser checks have no retained screenshot package. | Keep evidence provenance explicit. Capture step evidence for any formal sign-off repeat. |
| F-04 | Cover/transfer confirmations, missing-information updates and handover actions rely on staff input. | Accept only as demonstrated manual workflow; do not claim automatic verification of business facts. |
| F-05 | No Azure pipeline execution, production deployment or external-system verification. | Track separately; local results do not establish Azure execution or operational readiness. |
| F-06 | Local-only authentication, no comprehensive security review, no stale-edit conflict handling, database administrators can modify history. | Retain development-only scope. Do not approve live resident data or shared operational deployment based on this exercise. |

## Decision requested

Review whether the observed workflow meets the learning prototype's business purpose, whether F-01 needs correction before demonstration, and whether a clean manual TC-01 repeat is required. No user acceptance or release decision is recorded in this summary.

Recommended next step: address the timestamp usability finding and record the acceptance decision for this limited prototype, then return to the main options and data-readiness assessment. Expanding this into a full request-management system is not required to support the portfolio.
