# Enquiry tracking prototype: requirements for review

Date: November 11, 2026  
Status: First requirements review completed with user; local implementation and automated checks available; business acceptance pending  
Prepared by: BA

## Purpose

Demonstrate whether a small working application can retain and retrieve an enquiry's missing information, responsibility, follow-up date and absence cover. Replace assumptions about file declarations with observable prototype behaviour.

This is a supporting learning exercise. Results will apply to the tested prototype version, not a municipal application, and will not remove the operational publication hold. The separate AI use-case assessment and routing experiment remain undecided.

## Sources and authority

- [G-01](../03-current-state/practice-records/06-guidance-approval-record.md): named representative retains responsibility; supervisor arranges named cover; permitted recording and retrieval must be established.
- [Version 1.2 draft](../03-current-state/practice-records/07-missed-collection-guidance-v1.2-draft.md): business wording and unresolved tracking dependencies.
- [Evidence assessment](../03-current-state/tracking-method-check-plan.md): configuration checks do not verify running behaviour, permissions or history.
- Stakeholder exercise in this conversation: manager requested a demonstrable method covering responsibility, missing information, last action, follow-up, cover, correspondence and change history. These are review inputs, not real operational approvals.

The acceptance criteria below translate those inputs into prototype behaviour reviewed with the user in this conversation. Role-agent input is scenario content, not operational approval. The existing configuration's status names and transitions are not approved requirements for this application.

## Scope

One workflow: record a synthetic missed-collection enquiry, request missing details, maintain follow-up responsibility, arrange cover, and retrieve the record during handover.

Included: persistent records, synthetic correspondence, explicit test roles, validation, responsibility and cover changes, and a visible change history.

Excluded: AI classification, actual email delivery, production integration, collection scheduling, service eligibility, automatic closure, reminders, automatic reassignment and a full referral/closure workflow. AI classification remains part of the separate assessment, not this tracking demonstration.

## Roles

| Role | Proposed responsibility |
|---|---|
| Representative | Record and update enquiries they are authorised to handle |
| Supervisor | Arrange cover and review outstanding work |
| Covering representative | Retrieve and update an enquiry assigned for cover |
| Unauthorised test user | Must not retrieve or change the protected enquiry |
| BA | Maintain requirements, prepare tests, inspect results and record gaps |
| Systems Administrator / developer | Implement the application and explain technical constraints |
| Customer Service Manager | Review business fit; prototype test success does not confer operational approval |

## Requirements and acceptance criteria

| ID | Requirement and basis | Acceptance criteria |
|---|---|---|
| TR-01 | Retain an identifiable enquiry and its correspondence. Manager review input. | Save two distinct synthetic enquiries, each with a unique reference, received timestamp, resident message and synthetic outgoing request for details. After restarting the application, an authorised user can search by each reference and retrieve the correct enquiry with all values unchanged and both messages attached to the correct record. Do not send email. |
| TR-02 | Record outstanding information, last action and next action. G-01 and manager input. | Save “collection address missing,” the request for that address, and the next action. Reopen and amend the record. When the representative records the supplied collection address, mark that detail as received so it is no longer outstanding; retain any other missing details. Retain the original enquiry, request for details and resident reply. Record the actor and timestamp of the update in history. Save and reopen to confirm the current position and earlier correspondence remain retrievable. Recording an address must not automatically refer the enquiry. |
| TR-03 | Retain a named responsible representative. G-01. | Saving a tracked enquiry without a responsible representative is rejected with a clear message. Requesting missing information, recording a resident reply and assigning cover do not silently change the original responsibility. After the collection address is recorded, save and reopen the enquiry and confirm that the named responsible representative is unchanged. Receiving missing details does not constitute receiving-team acceptance; that later workflow is outside this prototype. Display the responsible representative and covering representative separately. |
| TR-04 | Record an agreed follow-up date. G-01 proposed wording; validation is a proposed design choice. | Saving an enquiry awaiting details without a valid follow-up date is rejected. A valid date can be saved, retrieved and changed. An overdue date remains visible; it does not trigger closure or reassignment. No fixed follow-up interval is imposed. |
| TR-05 | Supervisor arranges named absence cover. G-01; handback details require review. | A supervisor can assign and remove a named covering representative. A representative cannot grant themselves cover access. The assigned cover can retrieve the enquiry and correspondence and record the next action. Removing cover removes that user's access unless another permission applies. Record both changes in history. |
| TR-06 | Restrict access to authorised users. Manager input; exact permissions are proposed. | Test responsible representative, assigned cover and supervisor access. A different representative cannot read or amend the enquiry, including through a direct request to the application. Hiding a screen alone does not count as access control. |
| TR-07 | Preserve change history. Manager input. | Changes to responsibility, missing information, follow-up date and cover record the authenticated actor, timestamp, changed item, and old and new values. Ordinary users cannot edit or delete history through the application. Reopening after a restart retains it. This is application history, not a claim of tamper-proof storage. |

## Decision BR-01: Internal responsibility transfer

Agreed for the prototype during the November 11 requirements review: the user accepted the manager agent's proposal that the Customer Service Supervisor may authorise and record a permanent transfer within Customer Service for workload changes, staff departure or a longer absence requiring transfer.

Before transfer, the supervisor confirms the receiving representative can take over. Record the new representative, reason, authorising supervisor and effective timestamp. Preserve previous responsibility in history. Ordinary representatives cannot perform this operation. Temporary cover remains separate; waiting for information or an overdue date does not trigger transfer. Cross-department acceptance is outside this prototype.

This decision extends TR-03 and TR-07; it is an agreed prototype rule, not evidence of an operational policy. Other draft requirements and implementation decisions retain their stated review status.

## Test approach and evidence

Use synthetic enquiries and separate test identities. A role selector alone cannot establish authenticated-user permissions; if used for an early demonstration, label access results as simulated.

For each criterion capture: test ID, requirement ID, application version, environment, test identity, preconditions, steps, expected result, actual result, pass/fail/not-run outcome, and evidence reference. Include negative checks and restart/retrieval checks, not only successful saves. Record defects and retest results without replacing the original failure evidence.

Azure Boards will track requirements, tasks, findings and defects. Link automated test results from Azure Pipelines if configured. Check account access before choosing Azure Test Plans; test evidence can initially be maintained in the repository and linked from Boards. The application will run locally first; no cloud hosting or paid service is assumed.

## Decisions required before implementation

1. Confirm that this limited tracking exercise is worth adding alongside the main assessment.
2. Review TR-01–TR-07, particularly cover access, handback and the supervisor's visibility.
3. Agree the authentication approach and distinguish demonstrated permissions from simulated roles.
4. Select the implementation approach and record any reduced scope before building.

### Implementation update: November 11

The user authorised the local build after the requirements and test-case review. Version 0.1.0 uses Python's standard library, SQLite persistence, generated local test accounts, hashed passwords and authenticated server-side sessions. No paid dependency or cloud hosting was introduced. See the [application guide](../../prototype/tracking/README.md) for implementation decisions, including free-text missing-information updates and removing active cover before a permanent transfer. These design choices and browser usability still need user review; implementing them does not establish business acceptance.

Automated HTTP checks have run against the local application. See the [execution summary](../../results/tracking-prototype/README.md) for version hashes, results, initial environment failures and remaining limits. Azure pipeline execution and operational system verification remain outstanding.

## Completion criteria

The agreed criteria have reproducible test results for an identified running version; failures and untested checks remain explicit; limitations and evidence are reviewed. Prototype completion does not establish municipal system capability, permission to use live resident data, or authority to publish the operational guidance.



