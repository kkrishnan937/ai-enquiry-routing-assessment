# Municipal Enquiry Handling: AI Use-Case Assessment

Repository: `ai-enquiry-routing-assessment`.

This case study examines incomplete enquiries and uncertain handoffs before comparing four improvement options. Unresolved departmental responsibility led to one smaller experiment: classify the enquiry topic, with a separate review outcome for unclear or mixed reports. The decision was whether the model improved classification without weakening that review safeguard. **Status: complete, with limitations.**

[Read the one-page project summary](SUMMARY.md).

## Key result and decision

On 38 evaluation examples, Qwen2.5 3B correctly classified **22/29 clear cases**, compared with **7/29** for keyword rules. It correctly flagged **4/9 review cases**, compared with **7/9** for rules. The model failed the agreed safeguard. The recommendation is against operational rollout of either tested method.

![Classification and review comparison on 38 synthetic examples](docs/images/classification-comparison.png)

## Artifacts

| Artifact | What it shows | Link |
|---|---|---|
| Stakeholders and decision rights | Role responsibilities, authority boundaries and RACI | [Stakeholders](docs/03-current-state/stakeholders.md) |
| Process maps | Current handoffs and proposed handling | [As-Is and To-Be](docs/03-current-state/process-maps.md) |
| Options, baseline and data readiness | Why the task was narrowed and which records would support business measures | [Comparison](docs/04-options/evidence-and-data-comparison.md) / [Baseline measures](docs/04-options/baseline-measures.md) / [Readiness](docs/04-options/data-readiness-assessment.md) |
| Results and recommendation | Classification and review errors informing the decision | [Results](docs/06-evaluation/classification-results-and-recommendation.md) / [Recommendation](docs/06-evaluation/final-recommendation.md) |
| Supporting requirements and tests | Readable work items, criteria and requirement-to-test mapping | [Backlog](docs/05-requirements/backlog.md) / [Traceability](docs/05-requirements/traceability-matrix.md) |
| Implementation and evidence | Classifier code, fixed final evidence and development history | [Classifier](prototype/classification/README.md) / [Evidence index](results/README.md) |

## How to read this repo in 5 minutes

- Start with the [summary](SUMMARY.md) for the problem, role and decision.
- Follow the [stakeholders](docs/03-current-state/stakeholders.md), [process maps](docs/03-current-state/process-maps.md) and [options](docs/04-options/evidence-and-data-comparison.md).
- Check the [baseline measures](docs/04-options/baseline-measures.md), [backlog](docs/05-requirements/backlog.md) and [traceability](docs/05-requirements/traceability-matrix.md).
- Read the [results](docs/06-evaluation/classification-results-and-recommendation.md) and [recommendation](docs/06-evaluation/final-recommendation.md).

## BA framework

| Stage | Analysis and evidence |
|---|---|
| 1. Business problem | [Sponsor request](docs/01-plan/sponsor-request-memo.md), [source evidence](docs/01-plan/evidence-review.md) and [scope](docs/project-scope.md) define the concern and investigation boundary. |
| 2. Stakeholders | [Stakeholder analysis and RACI](docs/03-current-state/stakeholders.md) separate work, approval and escalation responsibilities. |
| 3. As-Is process | [Current-state map](docs/03-current-state/process-maps.md#as-is-walkthrough-account) shows missing-information loops and acceptance. |
| 4. Options and recommendation | [Options comparison](docs/04-options/evidence-and-data-comparison.md) and [data readiness](docs/04-options/data-readiness-assessment.md) explain the smaller experiment selected. |
| 5. To-Be process | [Proposed process map](docs/03-current-state/process-maps.md#to-be-proposed-missed-collection-handling) and [guidance draft](docs/03-current-state/practice-records/07-missed-collection-guidance-v1.2-draft.md) distinguish approved scenario rules from release dependencies. |
| 6. Requirements | [Tracking requirements](docs/05-requirements/tracking-prototype-requirements.md) and [experiment brief](docs/04-options/classification-experiment-brief.md) define behaviour, limits and acceptance criteria. |
| 7. Backlog | [Readable backlog](docs/05-requirements/backlog.md) records Azure items and requirement-based story summaries. |
| 8. Interface | [Tracking application guide](prototype/tracking/README.md) describes the working local interface. |
| 9. Testing | [Traceability matrix](docs/05-requirements/traceability-matrix.md) connects requirements to cases, outcomes and evidence. |
| 10. Change management | [Article versions](docs/03-current-state/practice-records/03-article-versions.md), [approval conditions](docs/03-current-state/practice-records/06-guidance-approval-record.md) and [prompt revision](results/classification/prompt-revision-review.md) retain the change rationale. |

## Limits

- Synthetic, related scenarios and shared author/reviewer context limit independence; labels lack independent service-owner validation despite two overlap exclusions.
- One model, one final run and a simple keyword baseline do not establish general performance or comparison with a mature rules system.
- No operational savings, service improvement, error frequency, investment ranking or staff effort was measured; model runtime is not staff effort, and hardware, electricity and staff costs were not assessed.
- The local tracking demonstration does not verify a municipal system, production security, complete manual sign-off or accessibility; concurrent edits, manual confirmations and direct database modification remain limitations.
- Public sources do not grant internal approval, classification does not settle ownership or eligibility, and static board records do not establish release; guidance publication remains on hold, no enterprise change-request workflow was established and no Azure Pipeline ran.

See the [summary limits](SUMMARY.md#limits), [evaluation detail](docs/06-evaluation/classification-results-and-recommendation.md#evidence-limitations) and [tracking test qualifications](docs/06-evaluation/tracking-prototype-test-summary.md).

## Supporting prototype

A separate local tracking application demonstrates saved enquiries, responsibility, absence cover, permissions and history. It was accepted for its learning purpose with documented qualifications. The [requirements](docs/05-requirements/tracking-prototype-requirements.md), [test summary](docs/06-evaluation/tracking-prototype-test-summary.md) and [Azure captures](docs/azure-boards-evidence.md) show that supporting work.

## Implementation guides

The [classification guide](prototype/classification/README.md) records the local setup, commands and frozen-run controls. The [tracking guide](prototype/tracking/README.md) explains how to start the supporting application. [Contribution record](ai-assistance-and-ownership-log.md).

## Context and disclosure

The assessment is inspired by Deliverable D3 of RFS-230-2026, Use-Case Assessment and Data Readiness Report. The prototype is an independent extension; the RFS excludes use-case implementation.

Published with written permission from the Government of Saskatchewan, Ministry of SaskBuilds and Procurement (Procurement Management Division), received Nov4,2026, for educational and portfolio use of the RFS materials. This project is an independent learning exercise. It is not commissioned by, endorsed by, or affiliated with the Government of Saskatchewan.

The scenario and stakeholder conversations are simulated, the enquiry data is synthetic, and no municipal interviews or operational measurements were conducted.

This portfolio was created using AI for stakeholder role-play, research support, drafting, code, synthetic data and testing, with the author reviewing decisions and findings.

Free tools were used; no paid inference service was used.

© 2026. Shared for portfolio review. All rights reserved.
