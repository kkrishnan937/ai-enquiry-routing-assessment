# Tracking-method evidence assessment

Prepared: November 10, 2026  
Technical input: Systems Administrator agent  
Reviewer: Business Analyst  
Status: First assessment for BA review; operational verification outstanding

## Purpose

Assess whether the available evidence establishes a usable, permitted way to record responsibility, missing information, follow-up dates and absence cover for the version 1.2 guidance.

## Evidence inspected

- Authored local configuration: `prototype/config/enquiry-statuses.json`, version 0.1, environment `local-practice`.
- Inspection script: `prototype/checks/inspect_configuration.py`.
- [Latest inspection report](../../results/local-configuration-inspection.md), including execution timestamp and configuration hash.
- [Version 1.2 draft](practice-records/07-missed-collection-guidance-v1.2-draft.md).

The script was rerun during this assessment: **10 of 10 file checks passed**. The configuration hash identifies the inspected bytes. This is reproducible file inspection, not observed application behaviour. Business use of a status is not approved merely because the file declares it.

## Check plan and current findings

| Check | Available evidence and finding | Check still required |
|---|---|---|
| Identify configuration version | Version, environment and SHA-256 are available in the file/report. | Establish that a future test environment uses the identified configuration. |
| Statuses and transitions | File declares Open, Awaiting Information, Referred, Accepted and Closed; its transition endpoints are declared statuses. | Observe permitted transitions and rejection of invalid transitions in an authorised test environment. |
| Retain responsible representative | `retain_named_representative` is true. | Observe ownership before and after a status change. No storage field or ownership validation is specified in the file. |
| Record missing information | No field or storage method is specified. **Evidence gap.** | Identify permitted recording method; enter, retrieve and amend a sample record. |
| Follow-up date | `follow_up_date_required` is true. No date field, validation or review mechanism is specified. | Attempt save without a date and with a valid date; inspect saved data and staff retrieval. |
| Automatic closure, reassignment and timers | File declares these false for awaiting-information handling; no direct awaiting-to-closed transition is listed. | Inspect other workflow rules and scheduled jobs; establish actual runtime behaviour. |
| Assign absence cover | No covering-representative field or temporary assignment mechanism is specified. **Evidence gap.** | Check assignment authority, handover, return/transferred responsibility and recorded changes. |
| Staff access during handover | No roles, permissions or accounts are supplied. **Evidence gap.** | Demonstrate that authorised covering staff can access the enquiry and correspondence, while unauthorised staff cannot. |
| Audit history | No audit settings or request histories are supplied. **Evidence gap.** | Observe who changed responsibility, status and follow-up details, when, and whether history is retained. |

## Later execution method

If authorised non-production access becomes available, use a sample request and appropriate test roles. For each check record the configuration version, actor, starting conditions, action, expected result, actual result and evidence reference. Separate observed results from assumptions. No such application tests have been performed.

## Decision supported

The current evidence supports statements about the authored file's declarations and reveals missing definitions. **It does not establish a usable, permitted operational tracking method.**

The BA can review this assessment and record the evidence gaps. Final system verification and operational release must remain outstanding. Do not build a full request-management application merely to close this learning task; confirm whether further testing is necessary within the portfolio scope.

## Next actions

- BA reviews findings and limitations against the version 1.2 draft.
- Manager reviews business wording separately from system readiness at the November 12 checkpoint.
- Systems Administrator identifies evidence/access needed for any further checks; no external system access or new completion date is assumed.