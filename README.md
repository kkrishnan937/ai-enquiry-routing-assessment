# AI Use-Case Assessment and Data Readiness

An independent AI Business Analyst portfolio exploring how a fictional public-service organization can assess AI opportunities and test a recommendation with a small prototype.

Status — November 12, 2026: Discovery and practice-record review are in progress. A supporting enquiry-tracking application (v0.1.1) is runnable locally; eight automated test groups passed, including a timestamp-validation regression. Assisted walkthrough evidence and remaining limitations are documented. The AI use-case comparison, formal data-readiness assessment, AI experiment and final recommendation remain outstanding.

## Work available for review

- [Sponsor request and business context](docs/01-plan/sponsor-request-memo.md).
- [Current-state intake summary](docs/03-current-state/intake-process-summary.md) and [connected practice records](docs/03-current-state/practice-records/README.md).
- [Tracking requirements and acceptance criteria](docs/05-requirements/tracking-prototype-requirements.md).
- [Seven designed test cases](docs/06-evaluation/tracking-prototype-test-cases.md), [test summary](docs/06-evaluation/tracking-prototype-test-summary.md) and [versioned execution evidence](results/tracking-prototype/README.md).
- [Synthetic enquiry examples](data/README.md), prepared for discussion rather than a validated evaluation set.

## Run the supporting application

Requires Python 3.12; no external packages or paid services are needed. From the repository root:

```powershell
python prototype/tracking/app.py --init
python prototype/tracking/app.py --port 8766
```

Open http://127.0.0.1:8766. Generated test passwords and the working database stay in the ignored `prototype/tracking/local-data/` directory. Never upload them. See the [application guide](prototype/tracking/README.md) for roles, limitations and test instructions.

Run the automated checks with:

```powershell
python prototype/tracking/test_acceptance.py
```

This application demonstrates enquiry tracking and handover; it is not the proposed AI routing experiment. Results apply to the local prototype, not a municipality's system. Full business acceptance and a clean manual persistence-test repeat remain outstanding. The [optional Azure pipeline definition](prototype/tracking/azure-pipelines.yml) is supplied but has not been configured or run in Azure DevOps.

## Business question

Which AI opportunity should the organization pursue first, and what must be ready before it proceeds?

## Planned approach

1. Define the citizen-enquiry process, its problems, and the evidence needed to assess them.
2. Compare enquiry routing, FAQ assistance, and enquiry trend analysis against consistent criteria.
3. Assess data readiness and consider simpler non-AI alternatives.
4. Select a narrow prototype task, subject to the assessment.
5. Compare a simple baseline with an AI approach, document errors, and recommend next steps.

Enquiry routing is the initial prototype candidate: suggest a category and responsible team for a synthetic request, with a person reviewing the suggestion. Technology and model choices remain open.

See [Project scope](docs/project-scope.md) for boundaries and intended evidence.

## Context and disclosure

The assessment is inspired by Deliverable D3 of RFS-230-2026, Use-Case Assessment and Data Readiness Report. This is a smaller learning exercise. The prototype is an independent extension; the RFS excludes use-case implementation.

This project is for learning and portfolio purposes only. The municipality, roles, and business scenario are fictional; no real stakeholder interviews or municipal operational measurements have been conducted. Request data will be synthetic. This project is not commissioned by or affiliated with the Government of Saskatchewan or any real agency. This disclosure applies to all project documents and code. Assumptions will be distinguished from measured results, and AI assistance will be disclosed.

Free tools are preferred. No paid licenses are assumed.
