# Municipal Enquiry Handling: AI Use-Case Assessment

Repository: `ai-enquiry-routing-assessment`.

This case study examines incomplete enquiries, repeated responsibility checks and uncertain handoffs before considering solutions. It compares four improvement options and tests a smaller enquiry-type classification task against keyword rules. A separate local tracking prototype demonstrates requirements and acceptance testing. **Status: complete, with limitations.** This does not authorise operational deployment or staff-guidance publication.

[Read the one-page project summary](SUMMARY.md).

## Key result

On 38 synthetic evaluation examples, Qwen2.5 3B correctly classified **22/29 clear cases**, compared with **7/29** for keyword rules. It correctly flagged **4/9 review cases**, compared with **7/9** for rules. The model failed the agreed safeguard: improve classification without worse handling of unclear or mixed reports. Neither tested method is recommended for operational use.

![Classification and review comparison on 38 synthetic examples](docs/images/classification-comparison.png)

## Artifacts

| Artifact | What it shows | Link |
|---|---|---|
| Process maps | Current handoffs and proposed handling, with source and approval boundaries | [As-Is and To-Be](docs/03-current-state/process-maps.md) |
| Options and data readiness | Why the task was narrowed and what evidence is missing | [Comparison](docs/04-options/evidence-and-data-comparison.md) / [Readiness](docs/04-options/data-readiness-assessment.md) |
| Requirements and backlog | Roles, acceptance criteria and readable Azure work items | [Requirements](docs/05-requirements/tracking-prototype-requirements.md) / [Backlog](docs/05-requirements/backlog.md) |
| Traceability | Requirement-to-story-to-test mapping and qualified results | [Matrix](docs/05-requirements/traceability-matrix.md) |
| Results and recommendation | Classification/review errors and decision against rollout | [Results](docs/06-evaluation/classification-results-and-recommendation.md) / [Recommendation](docs/06-evaluation/final-recommendation.md) |
| Implementation and evidence | Local code, final evidence and development history | [Classifier](prototype/classification/README.md) / [Tracking](prototype/tracking/README.md) / [Evidence index](results/README.md) |

## How to read this repo in 5 minutes

- Start with the [summary](SUMMARY.md) for the problem, role and decision.
- Follow the [process maps](docs/03-current-state/process-maps.md) and [options comparison](docs/04-options/evidence-and-data-comparison.md).
- Check the [backlog](docs/05-requirements/backlog.md) and [traceability](docs/05-requirements/traceability-matrix.md).
- Read the [results](docs/06-evaluation/classification-results-and-recommendation.md) and [recommendation](docs/06-evaluation/final-recommendation.md), including their limitations.

## BA framework

| Stage | Analysis and evidence |
|---|---|
| 1. Business problem | [Sponsor request](docs/01-plan/sponsor-request-memo.md), [source evidence](docs/01-plan/evidence-review.md) and [scope](docs/project-scope.md) define the concern and investigation boundary. |
| 2. Stakeholders | [Elicitation notes](docs/03-current-state/elicitation-notes-2026-11-08.md) and [delegated authority](docs/03-current-state/practice-records/05-delegation-record.md) distinguish work, approval and escalation responsibilities. |
| 3. As-Is process | [Current-state map](docs/03-current-state/process-maps.md#as-is-walkthrough-account) shows missing-information loops and acceptance. |
| 4. Options and recommendation | [Options comparison](docs/04-options/evidence-and-data-comparison.md) and [data readiness](docs/04-options/data-readiness-assessment.md) explain the smaller experiment selected. |
| 5. To-Be process | [Proposed process map](docs/03-current-state/process-maps.md#to-be-proposed-missed-collection-handling) and [guidance draft](docs/03-current-state/practice-records/07-missed-collection-guidance-v1.2-draft.md) distinguish approved scenario rules from release dependencies. |
| 6. Requirements | [Tracking requirements](docs/05-requirements/tracking-prototype-requirements.md) and [experiment brief](docs/04-options/classification-experiment-brief.md) define behaviour, limits and acceptance criteria. |
| 7. Backlog | [Readable backlog](docs/05-requirements/backlog.md) records Azure items and requirement-based story summaries. |
| 8. Interface | [Tracking application guide](prototype/tracking/README.md) describes the working local interface. |
| 9. Testing | [Traceability matrix](docs/05-requirements/traceability-matrix.md) connects requirements to cases, outcomes and evidence. |
| 10. Change management | [Article versions](docs/03-current-state/practice-records/03-article-versions.md), [approval conditions](docs/03-current-state/practice-records/06-guidance-approval-record.md) and [prompt revision](results/classification/prompt-revision-review.md) retain the change rationale. |

## Evidence limits

Forty evaluation candidates were prepared; two development-overlap cases were excluded before predictions. The small synthetic dataset, related scenarios, shared author/reviewer context, lack of independent service-owner validation and simple baseline limit the conclusions. One model and one final run do not establish general performance. No operational savings or service improvements were measured. Model runtime is not staff effort; hardware, electricity and staff costs were not assessed.

Public service information supports the context, not internal municipal approval, a financial ranking or evidence of problem frequency. Enquiry-type classification does not decide departmental ownership, eligibility or illegality. Missing operational details remain separate from the type.

The supporting tracking prototype was accepted for demonstration with limitations. Its results do not verify a municipality's system, establish production security or remove the guidance publication hold. Some observations are user-reported; full manual sign-off, accessibility and security reviews were not completed. Concurrent edits, manual confirmations and direct database modification remain limitations. See the [test summary](docs/06-evaluation/tracking-prototype-test-summary.md) and [application guide](prototype/tracking/README.md).

Change records demonstrate review of wording and approval conditions. They do not establish an enterprise change-request workflow. The working interface is a local demonstration; the requirements are proportionate specifications.

## Project records

[Azure Boards captures](docs/azure-boards-evidence.md) retain the states shown at capture, including Active and New items. Portfolio completion does not retrospectively change those records. The [readable backlog](docs/05-requirements/backlog.md) separates recorded statuses from delivered evidence. [Contribution record](ai-assistance-and-ownership-log.md).

## Reproduce the classification work

The keyword development check uses Python's standard library:

```powershell
python prototype/classification/run_development.py
```

AI execution requires a local Ollama installation and the recorded Qwen2.5 3B model. See the [classification guide](prototype/classification/README.md) for commands, model/settings evidence and retained results. The final-run script refuses to overwrite its existing run. Do not rerun a now-seen evaluation set and call the result unseen, or re-run the dataset-preparation script over frozen data.

## Run the supporting application

Requires Python 3.12; no external packages or paid services are needed. From the repository root:

```powershell
python prototype/tracking/app.py --init
python prototype/tracking/app.py --port 8766
```

Open http://127.0.0.1:8766. Generated test passwords and the working database stay in the ignored `prototype/tracking/local-data/` directory. Never upload them. See the [application guide](prototype/tracking/README.md) for roles, limitations and test instructions.

Run the automated checks with:

```powershell
python prototype/tracking/test_acceptance.py
```

This application demonstrates enquiry tracking and handover; it is separate from the AI classification experiment. It was accepted for its learning purpose in conversation, and a clean assisted browser persistence repeat passed. Results apply to the local prototype, not a municipality's system. Operational guidance publication remains on hold. The [optional Azure pipeline definition](prototype/tracking/azure-pipelines.yml) is supplied but has not been configured or run in Azure DevOps.

## Context and disclosure

The assessment is inspired by Deliverable D3 of RFS-230-2026, Use-Case Assessment and Data Readiness Report. This is a smaller learning exercise. The prototype is an independent extension; the RFS excludes use-case implementation.

Published with written permission from Lana Currie-Lingelbach
Government of Saskatchewan
Procurement Business Partner
Strategic Sourcing
Business &  Technology Solutions
Procurement Management Division
Ministry of SaskBuilds & Procurement on Nov 5,2026, for educational and
portfolio use of the RFS materials. This project is an independent learning
exercise. It is not commissioned by, endorsed by, or affiliated with the
Government of Saskatchewan.

This project is for learning and portfolio purposes: the scenario and stakeholder conversations are simulated, the enquiry data is synthetic, and no municipal interviews or operational measurements were conducted; it is not commissioned by or affiliated with any government or agency.

This portfolio was created using AI for stakeholder role-play, research support, drafting, code, synthetic data and testing, with the author reviewing decisions and findings.

Free tools were used; no paid inference service was used. Hardware, electricity and staff effort were not costed. No further model tuning or tracking features are planned.

© 2026 Kailas Krishnan. Shared for portfolio review. All rights reserved.
