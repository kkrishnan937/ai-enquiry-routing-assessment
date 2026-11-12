# Tracking prototype — test cases

Prepared: November 11, 2026  
Status: TC-01–TC-07 designed; automated HTTP checks executed; full manual acceptance not completed  
Requirements: [Tracking prototype requirements](../05-requirements/tracking-prototype-requirements.md)

## Execution update — November 11

The **Not run** entries below preserve the original manual-case templates; they are not current claims that no application testing exists. Automated checks mapped to TC-01–TC-07 have now executed against a running local application. See the [execution summary and run evidence](../../results/tracking-prototype/README.md). Automated group success does not mean every manual step or usability check was performed. Manual execution records remain unpopulated; no municipal system or Azure pipeline was tested.

## TC-01 — Retrieve separate enquiries and correspondence after restart

Requirement: TR-01  
Objective: Establish that saved enquiry details and correspondence persist across an application restart and remain associated with the correct enquiry.  
Execution status: **Not run — working application not yet available.**

### Preconditions

- An identified application build is running against a dedicated test database.
- Test account `rep-a` is authenticated and authorised to create and retrieve both enquiries.
- Test data below has not already been entered for this execution.
- Outbound email is disabled; correspondence is stored only.
- The tester can stop and restart the application without clearing or replacing its database. Use the same database after restart.

### Test data

No operational address is needed for this persistence check. Dates and account identifiers are test inputs, not evidence of actual enquiries or an agreed service interval.

| Item | Enquiry A | Enquiry B |
|---|---|---|
| Received timestamp | 2026-11-11T09:00:00-06:00 | 2026-11-11T09:15:00-06:00 |
| Resident message | My garbage cart was not emptied. | My recycling cart was not emptied. |
| Stored outgoing message | Please provide the collection address for your garbage enquiry. | Please confirm the missed collection date for your recycling enquiry. |
| Missing information | Collection address | Missed collection date |
| Responsible representative | rep-a | rep-a |
| Follow-up date, if required to save | 2026-11-12 | 2026-11-13 |

### Steps and expected results

| Step | Action | Expected result |
|---|---|---|
| 1 | Create Enquiry A using the supplied data; save and record its reference. | Save succeeds and a non-empty reference identifies A. |
| 2 | Store A's outgoing message against that enquiry. | The enquiry contains its resident message and the exact outgoing message, with their directions distinguishable. No email is sent. |
| 3 | Create Enquiry B, save, and store B's outgoing message. Record its reference. | B has a different reference from A and contains B's two messages. |
| 4 | Stop the application, confirm the process has stopped, and restart it using the same database. Sign in again as rep-a. | The application is available again without recreating the records or reseeding their content. |
| 5 | Search using A's exact reference and open the result. | The result is A. Its reference, received timestamp and message content match the saved values. Both A messages are present; neither B message appears. An equivalent timestamp display is acceptable if it represents the same instant and states its time zone. |
| 6 | Search using B's exact reference and open the result. | The result is B. Its reference, received timestamp and message content match the saved values. Both B messages are present; neither A message appears. |

### Execution record

Create a separate execution record for each run; do not overwrite a failed run when retesting.

| Field | Value |
|---|---|
| Run ID | Not assigned |
| Tester and execution date | Not recorded |
| Application version / commit | Not available |
| Environment and database identifier | Not available |
| Test identity | Planned: rep-a; actual identity not recorded |
| References generated for A and B | Not generated |
| Actual result for each step | Not observed |
| Overall outcome | Not run |
| Evidence references | None |
| Defect references | None recorded; this does not establish absence of defects |

### Evidence and outcome rules

- Capture the two saved references and their pre-restart content, evidence of the process restart, and each retrieved record after restart. Screenshots or automated output must identify the run and tested version through the execution record.
- Pass only if every expected result is observed. Record any mismatch against its step and raise a defect with reproduction details.
- If a precondition prevents execution, record the run as blocked and identify the reason; do not mark it passed.
- This case tests persistence and record association. Permission denial, updates, cover removal and audit history require separate cases under TR-02–TR-07.

## Shared execution arrangements for TC-02–TC-07

Use the execution-record fields and outcome rules defined under TC-01 for every case. Record actual results for each numbered step and retain separate runs for retests. All cases below are **Not run — working application not yet available**; no execution identities, versions, dates, evidence or defects have been recorded.

Use a fresh enquiry for each case, or restore a documented fixture before each independent scenario. Do not depend on another case having passed. Use authenticated test accounts: `rep-a` (responsible representative), `rep-b` (potential cover), `rep-c` (unrelated representative), and `supervisor-a`. Only the supervisor has the proposed supervisor role. The exact permission model and authentication approach require implementation review; a role selector alone cannot establish access-control results.

Record the application version, database identifier, configured time zone and test clock where relevant. Use synthetic correspondence only. All dates below are test inputs, not a service standard. Access checks must exercise application-side enforcement as well as visible screens. Record the actual routes and request payloads once the application exists; missing routes or unclear behaviour must be resolved before execution rather than assumed to pass.

## TC-02 — Receive missing information without losing earlier evidence

Requirement: TR-02  
Objective: Update the current position while preserving other outstanding details, correspondence and change history.  
Execution status: **Not run.**

### Preconditions and test data

- An enquiry belongs to rep-a, with collection address and missed collection date both outstanding.
- Original message: “My garbage cart was not emptied.” Stored outgoing message: “Please provide the collection address and missed collection date.”
- Last action: “Requested address and missed date.” Next action: “Review resident reply.” Follow-up date: 2026-11-12.
- New resident reply: “The collection address is Test Property A.” This is a synthetic location label; address validity is not being tested.

### Steps and expected results

| Step | Action | Expected result |
|---|---|---|
| 1 | As rep-a, save and reopen the initial record. | Both missing details, last action, next action and correspondence are retained. |
| 2 | Store the new reply, enter Test Property A as the collection address and mark that detail received. Update last action to “Recorded collection address” and next action to “Request missed collection date.” Save. | Address is retained and no longer outstanding. Missed date remains outstanding. Last and next actions match the changes. |
| 3 | Reopen the record and its correspondence. | Original enquiry, outgoing request and new reply remain attached to the same reference, with no overwritten message. |
| 4 | Inspect history. | Missing-information changes identify rep-a, time of change and old/new values. |
| 5 | Inspect responsibility and any referral information. | rep-a remains responsible. Recording the address has not dispatched or automatically referred the enquiry. |

Evidence: before/after record, all three messages, history entry and confirmation of no referral side effect. Actual results: **Not observed**.

## TC-03 — Require and retain the responsible representative

Requirement: TR-03  
Objective: Reject missing responsibility and prevent unrequested responsibility changes during clarification and cover.  
Execution status: **Not run.**

### Preconditions and test data

- rep-a and supervisor-a can perform their authorised operations.
- A new enquiry has valid content, outstanding collection address and a valid follow-up date; only its responsible representative is omitted for the negative check.
- rep-b is available as cover but has no other access to the enquiry.

### Steps and expected results

| Step | Action | Expected result |
|---|---|---|
| 1 | Attempt to save without a responsible representative, including a direct request omitting that value if the screen supplies a default. | Application rejects the invalid request with a clear message; no ownerless enquiry is persisted. A default must not mask the negative check. |
| 2 | Save a valid enquiry with rep-a responsible. Store a request for the missing address. | Save succeeds; rep-a remains responsible. |
| 3 | Record a resident reply and the supplied address; save and reopen. | rep-a is unchanged. No team acceptance is inferred from the reply. |
| 4 | As supervisor-a, assign rep-b as cover and reopen the record. | Responsible representative displays rep-a and covering representative displays rep-b separately. Cover has not replaced rep-a. |

Evidence: rejected save and persisted-record check, enquiry reference, before/after responsibility and distinct cover display. Actual results: **Not observed**.

## TC-04 — Validate follow-up dates and retain overdue enquiries

Requirement: TR-04  
Objective: Require a valid date, retain changes and avoid automatic closure or reassignment when follow-up becomes overdue.  
Execution status: **Not run.**

### Preconditions and test data

- A tracked enquiry awaiting details belongs to rep-a; other required values are valid.
- Use separate attempts for blank date, impossible date `2026-02-30`, and valid dates `2026-11-12` and `2026-11-13`.
- An isolated test clock can advance across the follow-up date without changing the computer's system clock. If that facility is unavailable, record the date-boundary check as blocked, not passed.

### Steps and expected results

| Step | Action | Expected result |
|---|---|---|
| 1 | Attempt save with no follow-up date. | Clear validation error; no invalid record is persisted. |
| 2 | Independently attempt save with the impossible date, using a direct request if the date picker prevents entry. | Application rejects the invalid date; the previously saved record, if any, remains unchanged. |
| 3 | Set the test date to November 11, 2026. Save with November 12 and reopen. | Valid date is retained accurately. No fixed interval is substituted. |
| 4 | Change the date to November 13; save and reopen. | New date persists and the change appears in history. |
| 5 | Advance the isolated test date to November 14; execute any configured time-based processing and reopen the enquiry. | Follow-up date is visibly overdue. Enquiry is still open for review, rep-a is unchanged, and no automatic closure or reassignment occurred. If no time-based processing exists, record that scope and the observation period; do not claim an indefinite guarantee. |

Evidence: validation responses, persisted dates, history, test-clock settings, processing/log evidence where applicable, and overdue record. Actual results: **Not observed**.

## TC-05 — Assign and remove absence cover

Requirement: TR-05; supporting coverage of TR-03 and TR-06  
Objective: Allow supervisor-controlled cover, usable handover and removal of access granted by cover.  
Execution status: **Not run.**

### Preconditions and test data

- An enquiry belongs to rep-a and includes correspondence, missing address, next action and follow-up date.
- rep-b initially has no assignment, cover or other permission for this enquiry.
- Separate authenticated sessions are available for rep-a, rep-b and supervisor-a.

### Steps and expected results

| Step | Action | Expected result |
|---|---|---|
| 1 | As rep-b, attempt to grant themselves cover through a direct request. | Request is denied; cover and permissions remain unchanged. |
| 2 | As supervisor-a, assign rep-b as cover. | Assignment succeeds; rep-a remains responsible and rep-b is separately identified as cover. History records the assignment. |
| 3 | As rep-b, retrieve the enquiry and correspondence; record next action “Follow up for collection address.” Save and reopen. | Cover can see handover details and retain the update. History identifies rep-b as the actor. |
| 4 | As supervisor-a, remove rep-b's cover. | Cover is cleared, rep-a is unchanged, and history records previous cover, new value, actor and time. |
| 5 | Without signing rep-b out, attempt to reopen and update the enquiry using its direct link and a direct update request. Refresh or resubmit any already-open page. | New reads and updates are denied. A previously loaded page cannot successfully save changes. Server-side record remains unchanged by the denied attempt. Already downloaded content cannot be retroactively withdrawn; that is not claimed. |

Evidence: denied self-assignment, supervisor assignment/removal, cover's saved action, history, denied requests after removal and authorised retrieval showing no unauthorised update. Actual results: **Not observed**.

## TC-06 — Enforce access for each test identity

Requirement: TR-06  
Objective: Demonstrate authorised reads/updates and deny unrelated users through both screens and direct requests.  
Execution status: **Not run.**

### Preconditions and test data

- An enquiry belongs to rep-a, with rep-b assigned as cover; rep-c is unrelated.
- supervisor-a has the proposed supervisor permission. Separate authenticated sessions prevent accidental identity reuse.
- Record the enquiry reference and the application's actual read/update routes. Prepare a harmless next-action change for authorised checks and “UNAUTHORISED CHANGE” for denied checks.

### Steps and expected results

| Step | Action | Expected result |
|---|---|---|
| 1 | Independently as rep-a, rep-b and supervisor-a, open the enquiry and save a distinct next-action update. | Each authorised identity can retrieve and update the enquiry; history identifies the actual actor for each change. |
| 2 | As rep-c, search for the reference and inspect the enquiry list. | Enquiry content is not disclosed in the list or search results. |
| 3 | As rep-c, use a known direct link/read request, correspondence request and update request. | Requests are denied without disclosing protected content. Update does not persist. Record actual response codes/messages; a hidden screen is insufficient. |
| 4 | Sign out and repeat direct read/update attempts without authentication. | Authentication is required; no protected content is returned and no update persists. |
| 5 | As rep-a, reopen the enquiry and inspect correspondence and history. | Authorised content remains intact; the unauthorised change was not saved. |

Evidence: identity/session record, authorised results, denied list/search/direct requests with response details, and post-attempt record inspection. Actual results: **Not observed**. This is defined functional permission coverage, not a comprehensive security assessment.

## TC-07 — Retain attributable history and prevent ordinary-user amendment

Requirement: TR-07  
Objective: Preserve actor, timestamp, changed item and old/new values across updates and restart, while rejecting ordinary-user history changes.  
Execution status: **Not run.**

### Preconditions and test data

- A fresh enquiry belongs to rep-a with address outstanding, follow-up date November 12, 2026 and no cover.
- Record its reference and initial values. Use independently authenticated rep-a and supervisor-a sessions and a known time zone.
- Cover can be assigned and removed. BR-01 defines supervisor-authorised permanent transfer within Customer Service. Use rep-c as the receiving representative, with a recorded confirmation that they can take over and reason “Workload redistribution.”

### Steps and expected results

| Step | Action | Expected result |
|---|---|---|
| 1 | As rep-a, mark the collection address received and change follow-up date from November 12 to November 13. | History identifies each changed item, its old/new values, rep-a and timestamp. Separate entries or one event with both field changes are acceptable. |
| 2 | As supervisor-a, assign rep-b as cover and then remove cover in a second saved action. | Both changes remain visible: none → rep-b, then rep-b → none, attributed to supervisor-a with their respective timestamps. |
| 3 | Compare all events with the actions performed and the recorded execution time. | Actor identities match authenticated sessions; timestamps use a stated time zone and fall within the execution window. Earlier events have not been overwritten. |
| 4 | As rep-a, attempt to amend or delete an existing history event through a direct application request using the actual route identified during implementation review. If no history mutation route exists, inspect routes and attempt an unsupported mutation against the actual history resource. | Application rejects the attempt; history is unchanged. Lack of edit buttons alone is insufficient evidence. Repeat for rep-b while authorised as cover using a separate fixture. |
| 5 | Stop and restart the application with the same database; sign in as an authorised user and reopen history. | All tested events, actors, timestamps and values remain intact and associated with the correct enquiry. |
| 6 | As rep-a, attempt to change the responsible representative to rep-c through a direct request. | Request is denied; responsibility and history of successful changes remain unchanged. |
| 7 | As supervisor-a, attempt permanent transfer without a reason or receiving-representative confirmation; test each omission independently. | Each incomplete request is rejected without changing responsibility. |
| 8 | As supervisor-a, record confirmation that rep-c can take over and transfer responsibility from rep-a to rep-c with reason “Workload redistribution.” | Transfer succeeds. Current responsibility is rep-c; history retains rep-a → rep-c, reason, authorising supervisor-a and effective timestamp. Temporary cover has not been used to represent this transfer. |
| 9 | Restart with the same database and retrieve as supervisor-a. | New responsibility and the complete transfer event persist alongside earlier history. |

Evidence: action/event comparison, before/after history, rejected mutation requests, route review and post-restart history. Actual results: **Not observed**. Application-level protection does not establish resistance to a database administrator changing stored data.

### Responsibility-transfer decision

BR-01 was agreed during the November 11 prototype review. Steps 6–9 cover authority, required transfer information and retained history. Recording receiving-representative confirmation is not proof that a real person agreed; this execution uses test participants and synthetic data.

## Coverage and readiness summary

| Requirement | Primary case | Supporting cases | Design limitation |
|---|---|---|---|
| TR-01 | TC-01 | TC-02, TC-05 | Runtime and storage not yet available |
| TR-02 | TC-02 | TC-07 | No execution evidence |
| TR-03 | TC-03 | TC-02, TC-05, TC-07 | BR-01 transfer checks designed; no execution evidence |
| TR-04 | TC-04 | TC-07 | Date-boundary execution requires an isolated clock or equivalent controlled fixture |
| TR-05 | TC-05 | TC-03, TC-06, TC-07 | Cover permissions remain a proposed design pending implementation review |
| TR-06 | TC-06 | TC-05 | Authenticated identities and actual request routes required |
| TR-07 | TC-07 | TC-02–TC-06 | BR-01 transfer history included; no execution evidence |

Seven cases were designed before implementation. Execution has since progressed through automated HTTP checks and an assisted walkthrough; see the [November 12 test summary](tracking-prototype-test-summary.md) for current results, deviations and remaining gaps. The Not run fields in the original templates above are not updated execution records. Passing prototype checks does not establish operational approval or municipal system readiness.
