# Paired development diagnostics — keyword rules and local AI

**Development data only. Not held-out performance or proof of business value.**

Model: qwen2.5:3b; baseline version: 0.1. Both used the same 20 enquiry texts.

| Measure | Keyword rules | AI |
|---|---:|---:|
| matching_outcomes | 17 | 14 |
| correct_automatic_classifications | 12 | 12 |
| coverage_count | 12 | 15 |
| correct_review_flags | 5 | 2 |
| forced_types_on_review_cases | 0 | 3 |
| invalid_outputs | 0 | 0 |

Clear-type denominator: 15. Review-expected denominator: 5. See structured evidence for per-type, unclear/mixed subsets and full confusion counts.

## AI disagreements

| Example | Expected | AI output |
|---|---|---|
| DEV-005 | review | missed_collection |
| DEV-011 | reported_dumped_waste | missed_collection |
| DEV-012 | reported_dumped_waste | missed_collection |
| DEV-014 | reported_dumped_waste | missed_collection |
| DEV-019 | review | missed_collection |
| DEV-020 | review | missed_collection |

## Runtime and limits

Total request wall time: 6.99s; median: 0.34s.

Rules were written with development data visible; the prompt uses the reviewed guide. Development labels were assistant-authored and user-reviewed with coaching, not independent domain ground truth. No fine-tuning or weight training was performed. Output schema enforcement does not guarantee semantic correctness. No prompt/rule change was made during this run and no failed output was retried or silently replaced. Preserve this run if later development changes occur. No paid inference API was used; electricity, hardware and staff effort are not costed. No held-out data was generated or read.
