# Paired development diagnostics — keyword rules and local AI

**Development data only. Not held-out performance or proof of business value.**

Model: qwen2.5:3b; baseline version: 0.1. Both used the same 20 enquiry texts.

| Measure | Keyword rules | AI |
|---|---:|---:|
| matching_outcomes | 17 | 12 |
| correct_automatic_classifications | 12 | 12 |
| coverage_count | 12 | 13 |
| correct_review_flags | 5 | 0 |
| forced_types_on_review_cases | 0 | 5 |
| invalid_outputs | 0 | 0 |

Clear-type denominator: 15. Review-expected denominator: 5. See structured evidence for per-type, unclear/mixed subsets and full confusion counts.

## AI disagreements

| Example | Expected | AI output |
|---|---|---|
| DEV-004 | review | reported_dumped_waste |
| DEV-005 | review | missed_collection |
| DEV-015 | other | missed_collection |
| DEV-016 | other | review |
| DEV-017 | other | review |
| DEV-018 | review | reported_dumped_waste |
| DEV-019 | review | missed_collection |
| DEV-020 | review | reported_dumped_waste |

## Runtime and limits

Total request wall time: 8.40s; median: 0.41s.

Rules were written with development data visible; the prompt uses the reviewed guide. Development labels were assistant-authored and user-reviewed with coaching, not independent domain ground truth. No fine-tuning or weight training was performed. Output schema enforcement does not guarantee semantic correctness. No prompt/rule change was made during this run and no failed output was retried or silently replaced. Preserve this run if later development changes occur. No paid inference API was used; electricity, hardware and staff effort are not costed. No held-out data was generated or read.
