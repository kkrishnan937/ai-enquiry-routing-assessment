# Classification experiment — success measures

Prepared: November 14, 2026  
Status: Working evaluation rules; no experiment executed

## Comparison and prerequisites

Compare one fixed keyword baseline and one feasible AI approach against the same frozen synthetic enquiries under the [labelling guide](../../data/labelling-guide.md). Input is enquiry text only. No source answer labels, annotation reasons or test-specific hints are supplied to either approach.

Before execution, review development edge cases, settle dataset composition, freeze source files and expected labels, and record rule/model/prompt versions, inference settings and environment. Keep development and evaluation scenario families separate. Dataset size and model remain open; do not generate a final test set until its review/split arrangements are clear. Use small-sample counts alongside percentages.

## Measures

| Measure | Calculation / interpretation |
|---|---|
| Correct automatic classification | For examples with a definite expected type: correct type with no review flag / all such examples. Wrong types, unnecessary review and unusable outputs count as unsuccessful. |
| Coverage | Definite-type examples receiving a valid type prediction without review / all definite-type examples. Report alongside accuracy, not alone. |
| Accuracy among classified examples | Correct type predictions / definite-type examples receiving valid non-review type predictions. If denominator is zero, report not applicable, not 100%. |
| Review detection | Examples expected to need review that receive a valid null-type review outcome / all examples expected to need review. Report unclear and mixed subsets separately. |
| Forced classification of review cases | Review-expected examples receiving a valid non-review type / all review-expected examples. Report counts; incorrect automatic action must not be hidden in aggregate accuracy. |
| Invalid/failed outputs | Count timeouts, execution failures and inconsistent or unparseable output combinations separately. Do not drop them or count them as safe review. Include them as unsuccessful in applicable primary denominators. |
| Per-type and error results | Full expected-versus-actual table, including review and invalid outcomes. Inspect clear, incomplete-detail, negation, ambiguity and mixed-request subsets. |
| Runtime and cost | Record execution time, resource/API usage and any directly observed cost. Distinguish local hardware use from a claim of zero total cost. No staff-time saving is inferred. |

## Decision rule agreed before scored execution

The purpose is a paired comparison, not certification against an invented industry benchmark. Recommend further AI investigation only if it produces **more correct automatic classifications on the same classifiable examples**, with **no reduction in correct review detection and no increase in forced classifications of review cases**, relative to the baseline. Invalid-output counts and error severity must also be considered; a parsing failure is not a safety improvement.

If AI ties, performs worse, or trades better type accuracy for worse review handling, report that it has not demonstrated a clear advantage under this rule. A recommendation to retain simple rules or conclude evidence is insufficient is valid. Small synthetic results are exploratory and do not establish statistical superiority, operational accuracy or financial benefit.

Feasibility also matters: report whether the method can be reproduced on the available environment and whether resource/cost requirements are acceptable. No operational latency/cost threshold is claimed. Any proposed budget or target must be explicitly recorded before execution rather than invented after results.

## Evidence and stopping point

Retain frozen inputs/expected labels, predictions, failures, versions, run settings, metrics and a concise error analysis. One model and one baseline are enough for this portfolio. Explain any model access limitation instead of quietly substituting fabricated predictions. Complete with a short recommendation and limitations; no new user interface, deployment or extensive benchmark programme is required.
