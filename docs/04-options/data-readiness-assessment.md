# Data-readiness assessment

Date: November 14, 2026  
Scope: Available portfolio evidence; not an assessment of municipal data holdings  
Conclusion: Sufficient for a limited synthetic classification experiment; insufficient for an operational business case or deployment decision.

## Decision context

Assess whether available information can support comparing enquiry types and handling uncertainty. This is narrower than departmental routing, response generation or real demand analysis. Definitions: [labelling guide](../../data/labelling-guide.md); source basis: [public-source check](classification-source-check.md).

| Dimension | Evidence inspected / finding | Consequence and outstanding need |
|---|---|---|
| Availability and purpose | Eight initial discussion examples; separate twenty-example classification development set; forty candidate evaluation texts reduced to thirty-eight before scoring. | Enables a controlled learning test. No operational extract, actual topic frequency, routing baseline or effort measurement. Do not add the sets together as independent enquiries or real demand. |
| Provenance | Text and initial labels authored by the assistant; development labels reviewed with user coaching/batch acceptance. Evaluation labels received a second AI review before predictions. | Authorship and review documented, but correlated generation/review bias remains. Independent domain labelling would be needed for operational conclusions. |
| Accuracy and authority | Public City service descriptions support distinctions between reported collection issues and dumped waste. They do not establish legal findings, provider responsibility or approved internal taxonomy. | Classify reported intent only. Departmental destinations remain unsupported where responsibility rules are unresolved. |
| Completeness | Missing location/date is preserved as a separate intake issue; unclear and mixed text is represented. | Do not infer absent facts. A clear type can still have incomplete operational details. Relevant real-world fields and workflow completeness are unverified. |
| Consistency and labels | Three types plus separate review outcomes; source rules, coached corrections and pre-prediction review are recorded. | A consistent experimental definition exists. Prior-case administrative questions and container-disposal boundaries remain task-specific interpretations, not universal municipal labels. |
| Diversity and representativeness | Deliberate quotas; minority review subsets are small. Lexical overlap screen and reviewer flags led to two exclusions. Remaining repeated semantic families are disclosed. | No claim of representative demand or full scenario independence. Results are sensitive to wording, label scope and the simple baseline. |
| Separation and leakage | Approach frozen before evaluation authoring; model receives text, prompt and schema only; author labels stored separately; both methods evaluated once. | Text was not used in development runs. Dataset author still knew development results, and reviewer context was not technically isolated. Full independent holdout is not established. |
| Ownership and maintenance | User/BA owns portfolio decisions; assistant authored artifacts. No municipal data/content owner participated. | Cannot approve operational use or source maintenance. A real organisation would assign owners and change/retention responsibilities. |
| Privacy and access | Dataset is synthetic and uses public service descriptions. Local account credentials and working tracking database are excluded from publication. | Does not establish permission to process real resident information. An operational exercise would require authorised access, minimisation, retention and privacy review. |
| Lineage and reproducibility | Approach/dataset hashes, model digest, prompt/rule versions, settings, raw predictions and exclusions retained. | Supports rerunning the documented software method, not guaranteed identical future inference or an independent performance claim. No repeatability study was performed. |

## Readiness by use case

- **Enquiry-type classification:** learning experiment executed with explicit synthetic/review limitations. No automatic destination decision.
- **Departmental routing:** agreed ownership rules and reviewed destinations not established across scope; classification performance does not fill that gap.
- **FAQ assistance:** public-source approach identified, but a checked answer corpus and owner-maintenance process were not assembled or evaluated.
- **Trend analysis:** no suitable operational time series; real trends cannot be assessed.
- **Guidance/intake improvement:** practice draft supports review of wording and traceability; real adoption and reduced rework remain unmeasured.

## Evidence and disposition

[Dataset/review plan](../06-evaluation/classification-dataset-plan.md), [pre-prediction adjudication](../../data/classification-evaluation/adjudication.json), [frozen dataset manifest](../../data/classification-evaluation/evaluation-freeze.json), [results and limitations](../06-evaluation/classification-results-and-recommendation.md).

Do not collect more synthetic data simply to make the portfolio appear larger. Retain the observed limitations in the recommendation. Any future real pilot would require authorised representative records, domain reviewers and agreed business measures; none is assumed available or approved.
