# Keyword baseline — development diagnostics

These are development results, not unseen evaluation or operational performance.

Executed UTC: 2026-11-14T19:46:28.045453+00:00
Baseline version: 0.1

| Measure | Count |
|---|---|
| total | 20 |
| matching_outcomes | 17 |
| classifiable_total | 15 |
| correct_automatic_classifications | 12 |
| classifiable_receiving_type | 12 |
| review_expected_total | 5 |
| correct_review_flags | 5 |
| forced_types_on_review_cases | 0 |

## Disagreements

| Example | Expected | Predicted |
|---|---|---|
| DEV-006 | other | review |
| DEV-009 | missed_collection | review |
| DEV-015 | other | review |

## Limits

The rules use lexical matches, not full meaning. They do not handle negation, historical context or distinguish a separate request from contextual wording. Multiple matched types trigger review, and no match also triggers review. Error reasons must be inspected in the prediction file before changing rules. Rules were authored with development examples visible; these results are not independent validation. No held-out set or AI predictions exist yet.
