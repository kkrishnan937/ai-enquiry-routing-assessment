# Municipal Enquiry Handling: AI Use-Case Assessment

Independent portfolio project. Synthetic data. Not affiliated with any government.

## Problem

The case examines incomplete enquiries, repeated responsibility checks and uncertain handoffs. The assessment asks which improvement to investigate and what evidence is needed before proceeding. It does not establish how often these problems occur in a municipality.

## My role

I set the scope, asked elicitation questions, checked understanding, reviewed requirements and labels, performed browser checks and examined the findings. I did not independently code the implementation.

## What I produced

- [As-Is and To-Be process maps](docs/03-current-state/process-maps.md).
- [Options comparison and selection rationale](docs/04-options/evidence-and-data-comparison.md).
- [Readable backlog and acceptance criteria](docs/05-requirements/backlog.md).
- [Requirements-to-test traceability](docs/05-requirements/traceability-matrix.md).
- [Results, errors and recommendation](docs/06-evaluation/classification-results-and-recommendation.md).

## Key finding

On 38 synthetic evaluation examples, the local model correctly classified **22/29 clear cases**, compared with **7/29** for keyword rules. It correctly flagged **4/9 review cases**, compared with **7/9** for rules. It forced classifications on five review cases; rules did so on two.

The agreed safeguard required improved classification without worse review handling. The model failed that safeguard despite classifying more clear enquiries correctly.

## Recommendation

Do not deploy either tested method. Retain clearer intake and ownership guidance as a foundation to investigate. Any operational pilot would need authorised representative records, independent service-owner labels and agreed error and review-workload limits. No additional build is proposed.

## Supporting prototype

A separate local tracking application demonstrates saved records, responsibility, cover, permissions and history; its [test evidence](docs/06-evaluation/tracking-prototype-test-summary.md) is separate from the classifier results.

## Limits

- Synthetic and related scenarios, including remaining overlap after two exclusions, do not represent municipal demand.
- Labels were not independently validated by service owners.
- The dataset author and reviewer shared project context.
- One model and one final run do not establish general performance.
- The simple keyword baseline does not represent a mature rules system.
- No operational savings or service improvement was measured, and model runtime is not staff effort.
- The prototype is not a municipal system and establishes neither production security, complete manual sign-off nor operational approval or removal of the guidance publication hold.
