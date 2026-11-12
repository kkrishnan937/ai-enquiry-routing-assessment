# Project scope

Initial working scope based on the direction agreed November 6, 2026.

## Purpose and scenario

Build an interview-ready AI Business Analyst portfolio connecting a business problem to assessment, data readiness, a small experiment, and an evidence-based recommendation.

A municipal customer-service team handles citizen enquiries about roads, waste collection, water services, and recreation. Start with email and web-form enquiries, from receipt to acceptance by the responsible team. Document the current process and investigate the causes of enquiry-handling difficulties. See the [draft sponsor request](01-plan/sponsor-request-memo.md).

Compare three candidates: enquiry routing, FAQ assistance, and enquiry trend analysis. Enquiry routing is the initial prototype candidate, subject to the assessment.

## Assessment

Compare business value, feasibility, data readiness, citizen impact, ethical risk, regulatory complexity, and alignment with the organization's objectives. Define scoring anchors and assumptions before scoring. Consider simpler non-AI alternatives and record uncertainty.

Assess relevant data quality, provenance, ownership, and labelling needs. Synthetic data can demonstrate checks; it cannot establish a real organization's data readiness.

## Prototype

The proposed routing experiment accepts a synthetic enquiry and suggests a category and responsible team for human review. Compare keyword rules with an AI classification approach on the same held-out examples.

No production integration, live citizen data, automatic request dispatch, or service eligibility decisions are planned. Technology, model, labels, dataset size, evaluation targets, and review workflow remain open decisions.

## Planned evidence

- Problem statement, process map, and stakeholder assumptions.
- Use-case comparison with scoring rationale and selection decision.
- Data-readiness assessment and synthetic-data documentation.
- Prototype requirements and acceptance criteria.
- Runnable prototype with reproducible evaluation and error analysis.
- Recommendation covering limitations and further evidence needed.

These are planned outputs, not completed work. Keep documentation proportionate to the decisions it supports.

## Evaluation

Define a labelling guide and separate development examples from held-out evaluation examples. Report classification performance, routing errors, and human-review needs. Assess runtime and cost where relevant. Do not infer real-world accuracy, production readiness, or time savings from synthetic results alone.

## Next step

Define the organization's service boundaries and current enquiry-handling process before selecting a model or building the prototype.

## GitHub

Development repository: https://github.com/kkrishnan937/ai-enquiry-routing-assessment. The repository is private while the portfolio is developed.
