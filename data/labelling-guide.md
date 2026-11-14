# Waste-enquiry labelling guide

Version: 0.1  
Prepared: November 14, 2026  
Status: Working rules for the bounded experiment; review before freezing evaluation data

## Purpose and source basis

Label the intent reported in synthetic enquiry text, not verified incidents, legal findings, eligibility or departmental responsibility. Source basis and exclusions: [public-source check](../docs/04-options/classification-source-check.md). The same guide applies to the keyword baseline and AI.

## Expected outputs

Record `type` as `missed_collection`, `reported_dumped_waste`, `other`, or null; record `review_required` as true/false. For this single-label experiment, a review outcome uses null type. A brief annotation reason is recorded for review evidence, not scored as generated prose. Missing-detail notes are separate descriptive metadata, not an additional model prediction task.

| Decision | Rule |
|---|---|
| Missed collection | Text clearly reports an expected scheduled collection was missed or partial. No proof of cause, eligibility or entitlement is inferred. |
| Reported dumped waste | Text clearly reports waste allegedly left/deposited/abandoned outside its intended disposal arrangement. Do not infer an offence or removal owner. |
| Other | Text establishes a clear topic outside both target types: for example damaged cart, schedule question or billing. Not a substitute for unknown intent. |
| Human review — unclear | Text does not supply enough context to distinguish the topic. Set type null and review_required true. |
| Human review — mixed | Text contains two or more distinct active requests from different types with no single supported primary intent. Set type null and review_required true. Includes a target request combined with a distinct Other request. Repeated wording about one request is not mixed. |

## Apply consistently

1. Read the whole message; do not label from isolated words. Negated, quoted, historical or hypothetical mentions are not automatically active requests. Use an explicit current primary request where the text establishes one.
2. Missing address, cart details or exact date does not alone require human review if the type is clear. Do not invent missing facts. A message too vague to establish intent does require review.
3. A full cart alone does not prove dumping. Waste on a road alone may be ambiguous; look for explicit abandoned/deposited context. If context is unresolved, use review.
4. A schedule question mentioning no missed event is Other. A clear current missed-event report can still be missed collection even when accompanied by contextual schedule wording that is not a separate request.
5. Keep an annotation reason and source-rule reference. If reviewers cannot apply the guide consistently, adjudicate before freezing labels; do not silently guess. Record unresolved cases separately and exclude them from scored ground truth with a count and reason.

## Review and split controls

- Development includes the three coached examples in the experiment brief; neither those texts nor close paraphrases belong in evaluation.
- Group related template/scenario families on one side of the split. Include variation, negation and distracting words; avoid a test consisting only of distinctive keywords.
- Record generation method, author/reviewer roles, disagreements and decisions. Assistant-generated and agent-reviewed labels are not independent municipal validation. User review is a separate contribution, not proof of domain expertise.
- Finalise expected labels without consulting model outputs. Freeze the guide, test set and expected labels before the scored run. Keep expected labels out of model input.
- Do not tune rules, prompts or model choice on held-out results. If later changes are informed by those results, disclose that the set is now development evidence and use a new held-out set for a fresh claim.

## Current position

No held-out set or independent domain review exists yet. The mixed-intent interpretation below was confirmed with the user; this does not by itself freeze the complete guide or evaluation design.

## Development edge-case review — November 14

| Discussed text | Reviewed outcome | Reason |
|---|---|---|
| There's rubbish outside my house. Can you sort it out? | Human review — unclear | Outside location does not establish dumping or missed collection. Clarification could distinguish cart contents from separately left waste; no reply exists. Initial dumped-waste suggestion was corrected during coaching. |
| My cart wasn't emptied, and someone has dumped a sofa beside the lane. | Human review — mixed | Two distinct active reports: missed collection and dumped waste. User explicitly confirmed this interpretation after the initial single-type suggestion was corrected. |
| My cart is damaged, but no collection has been missed and no waste has been dumped. How do I get it repaired? | Other | Active request is cart repair; target keywords occur only in negated reports. User agreed with the explained interpretation. |

These are development material; exclude them and near-duplicate variants from held-out evaluation. The review demonstrates coached clarification of rules, not independent annotator agreement. Clear Other versus review has also been discussed using the broken-cart example in the experiment brief. The initial ambiguous, mixed and negation review is complete; dataset composition, review arrangements and evaluation freeze still need explicit recording.
