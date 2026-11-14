# Classification dataset and review plan

Prepared: November 14, 2026  
Status: User agreed counts and disclosed review approach on November 14; no final evaluation data generated

## Size and composition

Use 20 development examples and 40 held-out evaluation examples. The six coached examples already discussed count toward the development set, not an extra set. Prepare the remaining development examples first; freeze rules and prompts before the scored evaluation.

| Expected outcome | Development count | Held-out count |
|---|---:|---:|
| Missed collection | 5 | 10 |
| Reported dumped waste | 5 | 10 |
| Other | 5 | 10 |
| Human review — unclear | 2 | 5 |
| Human review — mixed | 3 | 5 |
| Total | 20 | 40 |

These are deliberately chosen learning quotas, not an estimate of municipal demand, statistically powered sample or industry standard. Report actual counts and percentages; with only five examples in a review subset, one error changes its rate by 20 percentage points. Do not claim precise generalisation or statistical superiority.

Vary wording and context across both sets. Include clear intent with missing details, partial collection, non-target topics, negation and distracting words. Do not reuse the six coached texts or their close paraphrases in evaluation. Assign distinct scenario/template families to a single split and check for exact/near duplicates. A different address or synonym alone does not create an independent example.

## Roles and review sequence

1. **BA/user:** agrees the guide, plan and decision measures. Reviews development examples and unresolved boundaries; no real service-owner approval is implied.
2. **Assistant as author:** prepares synthetic development examples and, after development decisions are fixed, a separately stored candidate evaluation set. Record generation method and label provenance.
3. **Second-pass reviewer:** reviews evaluation text against the frozen guide before seeing author labels or any rules/model predictions. Use a separate reviewer pass/role where available and record its actual identity and access. A simulated/AI reviewer is not an independent municipal expert; disclose shared-model context and correlated bias.
4. **BA adjudication:** compare proposed labels and reasons. Log disagreements; use the guide, not future predictions, to resolve them. User adjudicates unresolved rule questions. If necessary revise the guide before freezing and recheck affected labels. Do not show/tune on final test texts during normal development; escalate only genuinely unresolved review questions.
5. If no second-pass review is available, do not claim independent review. Record the weaker author/self-review process and reduce the strength of conclusions.

## Storage and freeze

- Separate development data, evaluation input text and expected evaluation labels. Keep source references and annotation reasons in review material, not model input.
- Use neutral example identifiers; do not encode labels in identifiers or input filenames supplied to the model. Shuffle execution order reproducibly.
- Record guide version, dataset versions, split assignments, reviewer decisions, exclusion counts and file hashes before the scored run. A freeze identifies a fixed version, not a certification of quality.
- Both baseline and AI receive the identical evaluation text only. No expected labels, review reasons or result-specific prompts.
- Unresolved examples are not silently discarded. Either resolve before freeze or list exclusions and adjust reported denominators/composition transparently; do not invent replacements to meet quotas.
- After predictions are examined, do not tune and report the same set as unseen. Any result-informed revision requires disclosure and new evaluation data for a fresh claim.

## Success and stopping point

Apply the [evaluation plan](classification-evaluation-plan.md), including classification coverage, correct classifications, review detection, forced classifications and failed outputs. No extra model comparison, user interface or data-collection pilot is required. Finish with the paired results, a short error analysis and an evidence-limited recommendation.

## Immediate next action

User agreement to these quotas and the disclosed review approach was recorded in the November 14 conversation. Prepare only the development set next. Do not generate, publish or freeze held-out data yet. No reviewer has been assigned and no blind review completed by this plan.
