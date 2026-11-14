# Frozen held-out comparison — initial result

One keyword baseline and one local AI model on 38 frozen synthetic texts. No retries or post-result tuning. Two of forty candidates excluded for overlap before scoring.

| Measure | Keyword baseline | AI |
|---|---:|---:|
| correct_automatic_classifications | 7 | 22 |
| coverage_count | 8 | 23 |
| correct_review_flags | 7 | 4 |
| forced_types_on_review_cases | 2 | 5 |
| invalid_outputs | 0 | 0 |
| matching_outcomes | 14 | 26 |

Clear-type denominator: 29. Review-expected denominator: 9. Actual subset composition is in structured evidence.

Meets predefined paired comparison rule: **False**.

## Evidence and limits

Per-example raw responses, confusion tables, per-type/subset counts, hashes, runtime and freeze provenance are in predictions.json. Labels were reviewed before predictions. Synthetic data was authored by the same assistant involved in development; the second-pass AI review is not independent domain validation. Semantic similarity and generation bias remain limitations despite the scenario-family and duplicate check. No claims about actual demand, operational accuracy, savings or statistical superiority follow. Do not tune on these outputs and call a later run unseen.

AI request total: 10.92s; median: 0.22s. Includes caching/load effects; not staff time or service response time.
