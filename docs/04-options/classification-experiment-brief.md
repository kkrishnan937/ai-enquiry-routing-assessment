# Waste-enquiry classification: experiment brief

Prepared: November 14, 2026  
Status: Draft for BA review; dataset, model and acceptance thresholds not agreed

## Decision to support

Does AI offer enough improvement over simple keyword rules on a narrow synthetic enquiry-classification task to justify further investigation? A positive result would support further assessment, not municipal deployment or a claim of reduced staff effort.

## Why this experiment

The initial [option comparison](evidence-and-data-comparison.md) leaves routing and FAQ assistance needing preparation and real trend analysis without suitable records. This small classification experiment retains a connection to enquiry handling while avoiding unresolved departmental destination decisions. It was proposed for feasibility and learning value, not established as the highest-value organisational investment. Guidance/intake improvement remains a non-AI foundation; the tracking prototype is a separate supporting exercise.

## Task and boundaries

Input: synthetic resident enquiry text. Output: a suggested enquiry type, or a human-review outcome where a single type cannot be supported. Use the same rules for both approaches.

- Types: **Missed collection**, **Reported dumped waste**, **Other**.
- Other means a clearly identifiable different topic, not unknown intent.
- Unclear intent and mixed target types require human review; do not force a type.
- Missing address/date is a separate intake issue, not an enquiry type or automatic reason to abstain when intent is clear. Required-detail extraction is outside this experiment.
- No departmental routing, legal findings, eligibility, service promises, resident replies, automatic dispatch or live data.

Definitions and public-source limits: [classification source check](classification-source-check.md). The source check uses public reference material; it does not constitute internal approval.

## Comparison

1. Simple keyword rules with a defined human-review fallback.
2. One AI approach selected after confirming local feasibility or permitted API access and cost. No model, service, subscription or paid expenditure is authorised by this brief.

Both approaches receive the same held-out text and return the same type/review outcomes. Both can abstain; neither gets an artificial advantage from a different task definition. No additional web application is needed.

## Data and review

Prepare a compact synthetic set containing clear examples of all types, paraphrases, negation, distracting words, incomplete details, ambiguous intent and mixed requests. Existing eight examples are discussion material, not an automatically accepted test set.

Before execution: agree annotation rules, review expected outcomes against the source definitions, flag unresolved labels, and separate development examples from held-out evaluation. Record who generated and reviewed the examples, disagreements and adjudication. Keep near-duplicates and template families out of both sides of the split. Do not tune rules or prompts against held-out answers.

Dataset size, class mix and reviewer arrangements remain to be agreed proportionately; synthetic balance does not establish real demand. If the AI generating examples also contributes to labels, disclose that dependency and potential bias. Agent agreement is not independent municipal validation.

## Evaluation and evidence

- Report total examples, expected type/review distribution and any unresolved examples excluded from scored results.
- Report the full outcome/confusion table, including review outcomes; do not hide abstentions in an accuracy percentage.
- For classifiable examples, report overall correct outcomes, per-type results, coverage (share receiving a type prediction), and accuracy among classified cases together. Count an unnecessary abstention as an unsuccessful automatic classification in the overall result.
- For examples expected to require review, report the share flagged and the share incorrectly forced into a type. Report accuracy and review behaviour separately rather than claiming they are the same metric.
- Inspect errors by clear intent, missing details, ambiguous intent, mixed requests and wording variation. Report small counts alongside percentages.
- Record model/prompt/rule versions, test-set version, runtime environment and execution time. Assess runtime, repeatability and cost where measurable. Model self-reported confidence is not calibrated evidence.
- Agree performance targets and acceptable error trade-offs before running held-out evaluation. No numerical target or winner has been invented here.

## Completion and stopping point

Complete when reviewed definitions, development/evaluation data, reproducible rules and one feasible AI approach, results, error analysis and a short recommendation are available. A finding that rules are sufficient or evidence is inconclusive is valid. Do not add tracking features, new pilots, multiple AI models or deployment work merely to enlarge the portfolio.

## Immediate next step

Review a few development examples against these boundaries, then agree the annotation guide, dataset plan and evaluation targets before implementation.

## Development discussion: November 14

These examples were discussed with the user and must not appear in the held-out evaluation set or be paraphrased into it as near-duplicates.

| Example | Reviewed outcome | Reason |
|---|---|---|
| My garbage cart wasn't emptied yesterday. Can you help? | Missed collection | Clear report of collection not happening. Address absence is separate. The user's initial dumped-waste suggestion was corrected during coaching. |
| Someone left several bags of rubbish on the verge beside our property. They aren't in our collection cart. | Reported dumped waste | Describes alleged deposited waste, not a missed collection of the resident's cart. |
| The wheel on my garbage cart has broken. Can I get it repaired? | Other | Clear damaged-cart topic. The user's initial human-review suggestion was corrected: Other is not uncertainty. |

Only three straightforward examples have been discussed. Ambiguous, mixed-intent, negation and distracting-keyword rules still need to be fixed in the annotation guide before scoring. No held-out set has been created by recording these examples.
