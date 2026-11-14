# Single prompt revision — development review

Date: November 14, 2026  
Scope: Twenty known development examples; no held-out set generated or inspected

## Change and provenance

After the first development run, the user authorised one focused prompt revision. The original prompt is preserved byte-for-byte at prototype/classification/prompts/classification-v0.1.txt. The current classification-prompt.txt is the revised working prompt (v0.2). The model, schema, inference settings, dataset and keyword baseline were unchanged. Per-run hashes are retained in the structured evidence.

The revision prioritises mixed/unclear review decisions and explains that clear billing, disposal-advice and schedule topics are Other. It adds four development-derived illustrations. This is explicit development tuning, not improved unseen performance. Those illustrations and close variants must be excluded from evaluation alongside the development set.

## Evidence

- [Original pass](ai-development-20261114T200027864720Z/report.md).
- [Revised pass](ai-development-20261114T200233209487Z/report.md).
- Each run retains raw model responses and per-example predictions in predictions.json. No rule/prompt edits occurred within either run; no output was replaced by an expected answer.

## Result

| Measure | Keyword baseline | Original AI prompt | Revised AI prompt |
|---|---:|---:|---:|
| Correct automatic types / 15 classifiable | 12 | 12 | 12 |
| Correct review flags / 5 review cases | 5 | 0 | 2 |
| Forced classifications of review cases | 0 | 5 | 3 |
| Matching expected outcomes / 20 | 17 | 12 | 14 |
| Invalid outputs | 0 | 0 | 0 |

The revised prompt handles the two unclear reports correctly and fixes the three previously mishandled Other examples. However, it still forces all three mixed reports into missed collection and now misclassifies three clear dumped-waste reports as missed collection. Aggregate improvement masks this new error pattern.

Neither AI pass demonstrates a clear advantage under the working comparison rule: correct clear-type counts do not exceed the baseline, and review handling remains worse. This is a development finding only. It does not establish future held-out results or prove all AI approaches are unsuitable.

## Recommended stopping point

Retain both passes and stop prompt tuning after the single authorised revision. The revised prompt can be taken forward as an explicitly limited candidate if the user agrees, with known mixed-intent and dumped-waste errors. Freeze the guide, baseline, prompt and settings before preparing/evaluating held-out data. Do not switch models, add a hybrid or repeat tuning merely to obtain a win. A held-out result favouring simple rules or an inconclusive recommendation is a valid portfolio outcome.
