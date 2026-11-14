# Waste-enquiry classification — results and recommendation

Prepared: November 14, 2026  
Status: Initial final experiment findings for BA review; no operational approval

## Decision supported

The local AI classified more clear synthetic enquiries than the simple keyword baseline, but handled unclear/mixed enquiries less reliably. It **did not meet the pre-agreed comparison rule**. Do not recommend autonomous classification or operational deployment of either tested approach from these results.

## Method and evidence

- Twenty development examples reviewed with user coaching/batch acceptance; two AI development passes, with one authorised prompt revision. No model weights were trained.
- Guide, baseline, revised prompt and settings were snapshotted before the evaluation candidates were authored: [approach manifest](../../data/classification-evaluation/frozen-approach/manifest.json).
- Forty candidate texts were authored by the root assistant; a separate existing AI agent reviewed texts/guide without author labels or predictions by instruction, not enforced access separation. All proposed labels matched. This is not independent municipal validation.
- Two candidates were excluded for concrete development-overlap concerns before any predictions: one repair/negation near-paraphrase and one mixed-target structural overlap. No replacements were added merely to meet quotas. [Adjudication and limitations](../../data/classification-evaluation/adjudication.json).
- Actual evaluated set: 38 examples — 10 missed collection, 10 reported dumped waste, 9 Other, 5 unclear and 4 mixed. [Dataset freeze](../../data/classification-evaluation/evaluation-freeze.json).
- One fixed paired run, no retries or post-result prompt/rule changes: [report](../../results/classification/held-out-final/report.md), [raw predictions, metrics and versions](../../results/classification/held-out-final/predictions.json).

## Results

| Measure | Keyword baseline | Local AI |
|---|---:|---:|
| Correct automatic classification / 29 clear-type cases | 7 (24.1%) | 22 (75.9%) |
| Clear-type cases receiving a type / 29 | 8 (27.6%) | 23 (79.3%) |
| Correct among clear-type cases actually classified | 7/8 (87.5%) | 22/23 (95.7%) |
| Correct review flag / 9 review-expected cases | 7 (77.8%) | 4 (44.4%) |
| Forced type / 9 review-expected cases | 2 (22.2%) | 5 (55.6%) |
| Invalid or failed outputs / 38 | 0 | 0 |
| Exact expected type/review outcome / 38 | 14 (36.8%) | 26 (68.4%) |

Accuracy among classified cases excludes review outcomes; it must not be presented alone as overall accuracy. The overall matching-outcome count is descriptive, not the pre-agreed success rule.

### Per-type and review subsets

| Expected subset | Keyword correct | AI correct |
|---|---:|---:|
| Missed collection | 0/10 | 10/10 |
| Reported dumped waste | 5/10 | 8/10 |
| Other | 2/9 | 4/9 |
| Unclear — review required | 5/5 | 2/5 |
| Mixed — review required | 2/4 | 2/4 |

AI requests took approximately 10.92 seconds in total, median 0.22 seconds each, on the observed local environment. This is not a service-response or staff-effort measure. Shared-prompt caching, prior model residency and load effects limit runtime comparisons. No paid inference API was used; hardware, electricity and staff effort were not costed. Baseline runtime was not instrumented, so no quantified relative speed claim is supported.

## Error analysis

**Keyword baseline:** all ten clear missed-collection cases were unnecessarily referred for review. Its small literal patterns missed descriptions such as skipped/uncompleted service, while words such as “report” and “collection” alone were intentionally insufficient. This exposes narrow lexical coverage. It is not proof that a well-developed non-AI rules system would perform as poorly. The baseline also over-reviewed seven Other cases and forced two review cases into types.

**AI uncertainty handling:** three vague/status/reopening requests were incorrectly forced into missed collection. Two mixed requests were likewise forced into missed collection, losing their second intent. A valid JSON object did not make these decisions semantically correct.

**AI scope handling:** five clear Other topics were unnecessarily reviewed, including facility hours, storage advice, stolen-container replacement, swimming registration and service charges. One explicit waste-disposal report was labelled missed collection and another was unnecessarily reviewed. The development prompt revision therefore did not produce consistent interpretation of its decision rules on new texts.

## Interpretation against the agreed rule

The plan requires more correct automatic classifications without worse review detection or more forced review-case classifications. AI improves the first measure but fails both review safeguards. It therefore has **not demonstrated a clear advantage under that rule**, despite higher overall matching outcomes.

This is a trade-off finding, not a claim that keyword rules are universally superior or that all AI is unsuitable. Both approaches have substantial shortcomings. Human-review fallback also creates work; its benefit cannot be assumed without workload evidence.

## Recommendation and stopping point

1. Complete the portfolio experiment with the observed trade-off and retain all development/final results. Do not tune against the now-seen evaluation set or search for a winning model within this exercise.
2. Keep clearer intake/ownership guidance as an assessed non-AI foundation, while acknowledging that its adoption and benefits have not been measured.
3. If a real organisation later considers AI assistance, require representative authorised data, agreed business trade-offs, independent domain labels and assessment of human-review workload before a further pilot. That future work is not claimed complete here.
4. Do not deploy either prototype, replace staff judgement or infer actual departmental routing, illegality, eligibility or time savings.

## Evidence limitations

- Small, deliberately balanced synthetic set; not actual demand or a statistically powered comparison.
- Dataset author had development/prompt-result context. Second-pass AI review had prior project context and shared limitations; author/reviewer agreement does not establish domain correctness.
- Exact and lexical screening plus two exclusions do not establish full scenario-family disjointness. Repeated patterns within the evaluation set reduce effective diversity. Treat “held-out” as text excluded from development execution/tuning, with these semantic-independence qualifications.
- Unknown prior-case status requests were treated as unclear underlying intent under the guide. A different real business task could legitimately classify them as an administrative category.
- Broader alleged unauthorised container disposal was interpreted using the intended-disposal definition, without making a legal finding. Municipal operational taxonomy was not verified.
- Only one small model, one simple baseline and one final pass. Repeatability across multiple runs/settings and stronger baselines were not established. No confidence calibration, accessibility, production security or end-to-end benefit study.

## Next BA action

Review this recommendation with the user, then consolidate the options rationale, concise data-readiness findings and interview walkthrough. The tracking prototype, pilot proposals and operational guidance hold remain separate. No additional application features or measurement pilot is needed to explain the experiment.
