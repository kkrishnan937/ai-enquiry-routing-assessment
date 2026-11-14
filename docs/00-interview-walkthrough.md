# Interview walkthrough

Working outline — November 14, 2026. Adapt to your own understanding; do not memorise claims you cannot explain. Main disclosure is in the README.

## Two-minute explanation

I developed an independent BA case study about municipal enquiry handling. Public service information grounded the context, while stakeholder conversations, enquiries and operational records were simulated.

I explored intake and handoffs, distinguishing missing information from ownership disagreements and team acceptance from resolution. Reviewing connected query, email, article and approval records helped me identify unsupported instructions and explain why a later approval cannot prove an earlier publication was authorised.

I compared routing assistance, FAQ assistance, trend analysis and guidance improvements. The available evidence did not support a real investment ranking or benefit calculation. I chose a narrow enquiry-type classification experiment because it could be defined and tested without pretending unresolved departmental boundaries were settled.

I reviewed a labelling guide and twenty development examples, then compared keyword rules with a locally run AI model. A separate evaluation used thirty-eight synthetic examples after two overlap exclusions. AI correctly classified more clear enquiries, but flagged fewer unclear/mixed requests for review, so it did not meet our success rule.

My recommendation was not to roll out either tested approach. The value of the work is the traceable decision: requirements, evidence gaps, fair output rules, errors and a recommendation consistent with the criteria rather than a forced AI success story.

AI assisted with source review, drafting, code and automated tests. I participated in elicitation, challenged and refined definitions, reviewed labels, performed browser checks and reviewed findings. I would describe the implementation as AI-assisted rather than independently coded.

## Evidence to show

| Interview point | Artifact |
|---|---|
| Business context and evidence boundaries | [Sponsor memo](01-plan/sponsor-request-memo.md) and [evidence review](01-plan/evidence-review.md) |
| Current-state understanding | [Intake summary](03-current-state/intake-process-summary.md) |
| Governance judgement | [G-01](03-current-state/practice-records/06-guidance-approval-record.md), revised draft and retained publication hold |
| Options and data readiness | [Comparison](04-options/evidence-and-data-comparison.md), [readiness assessment](04-options/data-readiness-assessment.md) |
| Evaluation design and honest provenance | [Labelling guide](../data/labelling-guide.md), [dataset plan](06-evaluation/classification-dataset-plan.md), [freeze and exclusions](../data/classification-evaluation/evaluation-freeze.json) |
| Actual AI implementation and findings | [Classification guide](../prototype/classification/README.md), [results](06-evaluation/classification-results-and-recommendation.md) |
| Recommendation | [Final recommendation](06-evaluation/final-recommendation.md) |

## Questions to practise

1. Why was classification selected rather than departmental routing? Explain the ownership-rule gap and limited experiment objective.
2. Why can Other and human review not mean the same thing? Give one clear non-target request and one unknown/mixed intent example.
3. Why did we report coverage with accuracy? Explain how abstaining on clear cases can inflate accuracy among classified cases.
4. Why not recommend AI when 22/29 clear cases were correct? Explain the pre-agreed review safeguard and its 5/9 forced classifications.
5. How was leakage controlled, and what remained weak? Explain freezing, separate labels, two exclusions and the lack of full semantic/domain independence.
6. Did we measure savings? No. Model runtime is not active staff effort or response time; no operational baseline exists.
7. What did I personally do, and what did AI do? Point to coached reviews, user checks and assistant-authored implementation. Do not convert agent agreement into real stakeholder validation.

## Supporting tracking demonstration

The local tracking application illustrates requirements and acceptance testing for responsibility, absence cover, persistence, permissions and history. Eight automated groups passed; a clean assisted browser persistence repeat passed later. It is a separate learning extension, not the AI classifier or a municipal system. Keep its demonstration brief unless asked.

## Claims to avoid

Do not say you implemented AI for Saskatoon, interviewed municipal staff, proved savings, trained/fine-tuned a model, validated production security, ran Azure Pipelines, obtained operational approval or wrote all code independently. The full assessment recommendation remains subject to the user's final review.
