# Municipal Enquiry Handling: AI Use-Case Assessment

Independent portfolio project. Synthetic data. Not affiliated with any government.

## Problem

The case examines incomplete enquiries, repeated responsibility checks and uncertain handoffs. The assessment asks which improvement to investigate and what evidence is needed before proceeding. It does not establish how often these problems occur in a municipality.

## My role

I set the scope, asked elicitation questions, checked understanding, reviewed requirements and labels, performed browser checks and examined the findings. I did not independently code the implementation. The contribution record separates my work from drafting and implementation support.

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

## Limitations

Small synthetic samples are not representative demand. Labels lack independent domain validation. Dataset author and reviewer shared project context. Related scenario patterns remain despite two pre-run overlap exclusions. One model, a simple baseline and one final run do not establish general performance. Model runtime is not staff effort. No savings, municipal improvement, production security or operational approval was demonstrated. The separate tracking prototype does not remove the guidance publication hold.
