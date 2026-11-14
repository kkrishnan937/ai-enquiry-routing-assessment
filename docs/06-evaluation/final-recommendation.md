# Final assessment recommendation

Prepared: November 14, 2026  
Status: Completed assessment recommendation; not an organisational approval

## Recommendation

Do not recommend operational rollout of the tested AI classifier or the simple keyword baseline. Retain clearer intake and ownership guidance as a foundational improvement to investigate, without claiming measured savings or reduced errors. Close the experiment with the observed classification and review results.

## Business question and options

The investigation asks how enquiry handling could support correct, useful answers/referrals without unnecessary repeat contact or staff checks. The [qualitative comparison](../04-options/evidence-and-data-comparison.md) considers resident benefit, staff effort, data readiness, delivery effort/cost and risk/control. Numerical benefits, budgets and operational rankings were not supported by the available evidence.

| Option | Assessment disposition |
|---|---|
| Routing assistance | Departmental routing needs agreed ownership rules. A narrower enquiry-type classification task was chosen for a manageable experiment, not as proof this was the greatest-value investment. |
| FAQ assistance | Reasonable alternative for later assessment, but no checked question/answer collection was prepared. Public references alone are not an approved operational knowledge base. |
| Trend analysis | Real trend claims deferred because no suitable operational time series was available to this project. |
| Guidance/intake improvement | Retain as a foundation and possible simpler response to the scenario. Approval, adoption and effects still require evidence. The separate tracking demonstration does not prove guidance effectiveness. |

## Experiment and result

One local Qwen2.5 3B model was compared with a transparent keyword baseline. Twenty development examples informed one prompt revision; the approach was then frozen. Forty evaluation candidates were reviewed before predictions; two overlap cases were excluded, leaving thirty-eight. No final-run tuning or output replacement occurred.

- Clear-type cases: AI correct on **22/29**, rules **7/29**.
- Review-expected cases: AI correctly flagged **4/9**, rules **7/9**.
- Forced classifications of review cases: AI **5/9**, rules **2/9**.
- Invalid outputs: zero for both.

The pre-agreed rule required improved correct classifications without worse review handling. AI did not meet it. A higher overall matching-outcome count does not override that safeguard. The weak lexical baseline also failed many unfamiliar phrasings, so the result does not establish that a mature rules solution would perform this poorly. [Full results and error analysis](classification-results-and-recommendation.md).

## What the evidence supports

The prototype demonstrates a reproducible local comparison and the importance of assessing uncertainty separately from type accuracy. It does not demonstrate municipal performance improvement, staff-time savings, cost-effectiveness, correct departmental routing or readiness to replace staff judgement.

The synthetic examples and labels were not independently validated by service owners. Remaining semantic-family overlap, small review subsets and one run limit generalisation. [Data-readiness assessment](../04-options/data-readiness-assessment.md).

## Follow-on conditions for a real organisation

Before proposing an operational pilot: establish agreed service boundaries and taxonomy, authorised representative enquiry data, independent service-owner labels, appropriate privacy/access arrangements, and acceptable error/review workload targets. Assess human-review effort and source maintenance. These are future conditions, not additional deliverables or commitments for this portfolio.

## Closeout position

The assessment and experiment are complete, with limitations. The repository and Azure Boards retain the delivery evidence and recorded decisions. The supporting tracking prototype was accepted for demonstration with documented limitations. The scenario guidance publication hold remains because the operational release conditions were not met. No further build or pilot is planned.
