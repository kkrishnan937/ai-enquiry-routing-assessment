# Project scope

Updated November 14, 2026.

## Business question

Which improvement to enquiry handling should be investigated first, and what information is needed to support that decision?

## Assessment

The case covers email and web-form enquiries about roads, waste collection, water services and recreation, from receipt to acceptance by a service team. The assessment compares routing assistance, FAQ assistance, trend analysis and improvements to guidance and intake.

The comparison uses five criteria: resident benefit, staff effort, data readiness, delivery effort/cost and risk/control. Available evidence supports a qualitative comparison, not a financial business case or numerical investment ranking.

## Delivered work

- Current-state intake summary, elicitation notes and linked query, response, guidance and approval records.
- Options comparison and data-readiness assessment.
- Classification definitions, reviewed development examples and a frozen evaluation set.
- Keyword baseline and local Qwen2.5 3B comparison, with retained predictions and error analysis.
- Supporting tracking prototype, requirements, acceptance criteria and test evidence.
- [Final recommendation](06-evaluation/final-recommendation.md).

## Classification experiment

Classify the reported enquiry as missed collection, reported dumped waste or Other. Refer unclear or mixed reports for human review. Missing operational details are assessed separately from the enquiry type.

The experiment uses twenty development examples and thirty-eight evaluated examples after two pre-run exclusions. It does not assign departmental ownership, decide eligibility or generate resident answers.

## Supporting tracking prototype

Demonstrate saved enquiry records, missing-information updates, responsibility, absence cover, permissions and change history. It is separate from the classification experiment and was accepted for its demonstration purpose with documented limitations.

## Exclusions

Production integration, live resident data, automatic dispatch, operational deployment, additional models and further application features are outside scope. No measured savings or municipal performance improvements are claimed. The optional Azure pipeline has not been configured or run.

## Closeout

The assessment and experiment are documented. Final recommendation review remains. Operational guidance publication is a separate scenario decision and remains on hold.

[Private development repository](https://github.com/kkrishnan937/ai-enquiry-routing-assessment).
