# Backlog and acceptance criteria

## Recorded Azure work items

This is a readable copy of the ten recorded epic, feature and task titles. States were cross-checked against the Azure work-item lists. The [screenshots](../azure-boards-evidence.md) provide the published visual evidence. Active or New does not mean the related portfolio evidence is absent; it is the recorded board state. It has not been changed for presentation.

| Azure ID | Type | Title | Recorded state | Evidence scope |
|---|---|---|---|---|
| [#1](https://dev.azure.com/W0850313/AI%20Enquiry%20Assessment/_workitems/edit/1) | Epic | Assess improvements to municipal enquiry handling | Active | Overall assessment |
| [#5](https://dev.azure.com/W0850313/AI%20Enquiry%20Assessment/_workitems/edit/5) | Feature | Understand the current enquiry process | New | Current-state evidence |
| [#6](https://dev.azure.com/W0850313/AI%20Enquiry%20Assessment/_workitems/edit/6) | Feature | Assess improvement options and data readiness | Active | Options and readiness |
| [#7](https://dev.azure.com/W0850313/AI%20Enquiry%20Assessment/_workitems/edit/7) | Feature | Define and evaluate a small prototype after use-case selection | Active | Classification experiment and supporting tracking prototype |
| [#2](https://dev.azure.com/W0850313/AI%20Enquiry%20Assessment/_workitems/edit/2) | Task | Review guidance version 1.2 and confirm permitted tracking method | Active | Operational publication remains on hold |
| [#3](https://dev.azure.com/W0850313/AI%20Enquiry%20Assessment/_workitems/edit/3) | Task | Review synthetic enquiry examples and labelling rules | New | Initial starter examples; distinct from later classification labels |
| [#4](https://dev.azure.com/W0850313/AI%20Enquiry%20Assessment/_workitems/edit/4) | Task | Assess acceptance-message workload and agree responsible role | New | No operational workload measurement completed |
| [#8](https://dev.azure.com/W0850313/AI%20Enquiry%20Assessment/_workitems/edit/8) | Task | Prepare guidance version 1.2 draft | Closed | Draft delivered; not publication approval |
| [#9](https://dev.azure.com/W0850313/AI%20Enquiry%20Assessment/_workitems/edit/9) | Task | Assess tracking-method evidence and unresolved system checks | Closed | Evidence assessment complete; operational verification not established |
| [#10](https://dev.azure.com/W0850313/AI%20Enquiry%20Assessment/_workitems/edit/10) | Task | Review version 1.2 draft and record release-readiness decision | Closed | Review concluded publication must remain on hold |

Priorities were not recorded in Azure Boards.

Azure User Story IDs, priorities and full parent-child links were not exported. The seven BA-US items summarise requirements TR-01 to TR-07.

## Requirement-based story summaries

The BA-US identifiers are document-local summaries, not exported Azure story IDs or newly created board items. Acceptance criteria are reproduced from the requirements. Status describes retained test evidence, not an Azure story state.

## BA-US-01: Retain an identifiable enquiry and its correspondence

**Source:** TR-01, [tracking requirements](tracking-prototype-requirements.md).

As a customer service representative, I want to save and retrieve each enquiry with its correspondence, so that I can follow up without mixing residents’ records.

**Acceptance criteria**

Save two distinct synthetic enquiries, each with a unique reference, received timestamp, resident message and synthetic outgoing request for details. After restarting the application, an authorised user can search by each reference and retrieve the correct enquiry with all values unchanged and both messages attached to the correct record. Do not send email.

**Status:** Implemented; corresponding automated TC-01 passed on the retained version 0.1.1 run. Manual qualifications and limitations remain in the [traceability matrix](traceability-matrix.md). This is not operational acceptance.

## BA-US-02: Record outstanding information, last action and next action

**Source:** TR-02, [tracking requirements](tracking-prototype-requirements.md).

As a customer service representative, I want to update outstanding information while retaining earlier messages, so that I can see what is still needed and what has already happened.

**Acceptance criteria**

Save “collection address missing,” the request for that address, and the next action. Reopen and amend the record. When the representative records the supplied collection address, mark that detail as received so it is no longer outstanding; retain any other missing details. Retain the original enquiry, request for details and resident reply. Record the actor and timestamp of the update in history. Save and reopen to confirm the current position and earlier correspondence remain retrievable. Recording an address must not automatically refer the enquiry.

**Status:** Implemented; corresponding automated TC-02 passed on the retained version 0.1.1 run. Manual qualifications and limitations remain in the [traceability matrix](traceability-matrix.md). This is not operational acceptance.

## BA-US-03: Retain a named responsible representative

**Source:** TR-03, [tracking requirements](tracking-prototype-requirements.md).

As a customer service representative, I want to see named responsibility separately from temporary cover, so that tracking responsibility remains clear during clarification and handover.

**Acceptance criteria**

Saving a tracked enquiry without a responsible representative is rejected with a clear message. Requesting missing information, recording a resident reply and assigning cover do not silently change the original responsibility. After the collection address is recorded, save and reopen the enquiry and confirm that the named responsible representative is unchanged. Receiving missing details does not constitute receiving-team acceptance; that later workflow is outside this prototype. Display the responsible representative and covering representative separately.

**Status:** Implemented; corresponding automated TC-03 passed on the retained version 0.1.1 run. Manual qualifications and limitations remain in the [traceability matrix](traceability-matrix.md). This is not operational acceptance.

**BR-01 extension:** The supervisor may permanently transfer responsibility within Customer Service for workload changes, departure or longer absence, after confirming the receiving representative can take over. Retain the reason, authorising supervisor, effective timestamp and earlier responsibility. Ordinary representatives cannot transfer. Temporary cover and cross-department acceptance remain separate.

## BA-US-04: Record an agreed follow-up date

**Source:** TR-04, [tracking requirements](tracking-prototype-requirements.md).

As a customer service representative, I want to save and retrieve an agreed follow-up date, so that outstanding enquiries remain visible without automatic closure or reassignment.

**Acceptance criteria**

Saving an enquiry awaiting details without a valid follow-up date is rejected. A valid date can be saved, retrieved and changed. An overdue date remains visible; it does not trigger closure or reassignment. No fixed follow-up interval is imposed.

**Status:** Implemented; corresponding automated TC-04 passed on the retained version 0.1.1 run. Manual qualifications and limitations remain in the [traceability matrix](traceability-matrix.md). This is not operational acceptance.

## BA-US-05: Supervisor arranges named absence cover

**Source:** TR-05, [tracking requirements](tracking-prototype-requirements.md).

As a customer service supervisor, I want to assign and remove named absence cover, so that an authorised representative can continue the work during absence.

**Acceptance criteria**

A supervisor can assign and remove a named covering representative. A representative cannot grant themselves cover access. The assigned cover can retrieve the enquiry and correspondence and record the next action. Removing cover removes that user's access unless another permission applies. Record both changes in history.

**Status:** Implemented; corresponding automated TC-05 passed on the retained version 0.1.1 run. Manual qualifications and limitations remain in the [traceability matrix](traceability-matrix.md). This is not operational acceptance.

## BA-US-06: Restrict access to authorised users

**Source:** TR-06, [tracking requirements](tracking-prototype-requirements.md).

As a customer service supervisor, I want to restrict enquiry access to authorised users, so that unrelated or signed-out users cannot read or change protected records.

**Acceptance criteria**

Test responsible representative, assigned cover and supervisor access. A different representative cannot read or amend the enquiry, including through a direct request to the application. Hiding a screen alone does not count as access control.

**Status:** Implemented; corresponding automated TC-06 passed on the retained version 0.1.1 run. Manual qualifications and limitations remain in the [traceability matrix](traceability-matrix.md). This is not operational acceptance.

## BA-US-07: Preserve change history

**Source:** TR-07, [tracking requirements](tracking-prototype-requirements.md).

As a customer service supervisor, I want to retain attributable changes and responsibility transfers, so that staff can review who changed the record and what changed.

**Acceptance criteria**

Changes to responsibility, missing information, follow-up date and cover record the authenticated actor, timestamp, changed item, and old and new values. Ordinary users cannot edit or delete history through the application. Reopening after a restart retains it. This is application history, not a claim of tamper-proof storage.

**Status:** Implemented; corresponding automated TC-07 passed on the retained version 0.1.1 run. Manual qualifications and limitations remain in the [traceability matrix](traceability-matrix.md). This is not operational acceptance.

## Scope limits

The tracking prototype has no actual email delivery, automatic referral, closure, reminders, automatic reassignment or full referral workflow. Classification is a separate experiment. Passing local checks does not release staff guidance or verify a municipal system. No Azure Pipeline was executed.
