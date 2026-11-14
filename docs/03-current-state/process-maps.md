# Enquiry handling process maps

These maps consolidate the recorded walkthrough and proposed guidance. They do not add a service standard or confirm municipal practice.

## As-Is: walkthrough account

Based on the [intake summary](intake-process-summary.md), steps 1–7, and the [elicitation notes](elicitation-notes-2026-11-08.md), representative account. The system statuses below were described during the walkthrough; no operational system was inspected. The map covers a referral case. Direct answers were mentioned but not walked through.

```mermaid
flowchart TD
    subgraph Resident[Resident]
        A[Send email or web enquiry]
        D[Supply requested details]
        N[Receive referral reference and updates]
    end
    subgraph CS[Customer Service Representative]
        B[Read enquiry and check required information]
        C{Enough information?}
        E[Request missing details and record what is outstanding]
        F[Retain responsibility while waiting]
        G[Update record and check reply]
        H[Refer to service team and record Referred]
        I[Check outstanding referrals]
        J{Acceptance recorded?}
        K[Contact receiving team and record follow-up]
    end
    subgraph Team[Receiving service team]
        L{Belongs to team and enough details?}
        M[Record Accepted with actor and time]
        O[Investigate and progress request]
    end
    subgraph Supervisor[Customer Service Supervisor]
        P[Assist with no response or disputed responsibility]
    end
    A --> B --> C
    C -->|No| E --> F
    E --> D --> G --> C
    C -->|Yes| H
    H --> N
    H --> L
    H --> I --> J
    L -->|Yes| M --> O
    M --> J
    J -->|Yes| O
    J -->|No| K --> P --> I
    L -->|No: reason needs checking| K
```

Waiting for a resident or a team does not transfer tracking responsibility. A return alone does not prove an ownership dispute. Acceptance is not resolution or a promised collection date.

## To-Be: proposed missed-collection handling

Based on [G-01](practice-records/06-guidance-approval-record.md), [draft version 1.2](practice-records/07-missed-collection-guidance-v1.2-draft.md), [D-01](practice-records/05-delegation-record.md) and the interim direction in the [elicitation notes](elicitation-notes-2026-11-08.md). Collection details and named responsibility have scenario approval. The permitted tracking method, final wording, publication and briefing conditions remain unresolved. This is a proposed process, not released staff guidance.

```mermaid
flowchart TD
    subgraph Resident[Resident]
        A[Report missed collection]
        E[Reply with missing details]
    end
    subgraph Rep[Customer Service Representative]
        B[Record collection address, cart type and reported missed date]
        C{All required details supplied?}
        D[Request missing details and retain correspondence]
        F[Keep named responsibility and agree follow-up date]
        G[Check reply and remaining missing details]
        H[Apply confirmed referral procedure]
        I[Track referral until receiving team accepts]
        J{Receiving team accepted?}
    end
    subgraph Supervisor[Customer Service Supervisor]
        K[Arrange named cover during absence]
        L[Check cover can access record and messages]
        M[Record team reasons and coordinate unresolved referral]
    end
    subgraph Team[Receiving service team]
        N[Review details and responsibility]
        O[Record acceptance and take investigation responsibility]
    end
    subgraph Managers[Customer Service Manager and service managers]
        P[Review unresolved boundary with service managers]
        Q{Standing boundary agreed?}
        R[Record joint approval within delegated scope]
        S[Refer disputed boundary to Director, Municipal Operations]
        T[Record decision before treating it as a standing rule]
    end
    A --> B --> C
    C -->|No| D --> F
    D --> E --> G --> C
    F -->|Representative absent| K --> L --> F
    F -->|Follow-up unresolved| M
    C -->|Yes| H --> N
    H --> I --> J
    N -->|Accepted| O --> J
    J -->|Yes| U[Handoff complete; service work not yet complete]
    J -->|No response or disagreement| M --> I
    M -->|Unresolved boundary| P --> Q
    Q -->|Yes| R --> T
    Q -->|No| S --> T
```

The tracking method must be verified before guidance release. This map prescribes no unverified status, field, reminder, automatic reassignment or automatic closure. The model experiment does not decide departmental ownership. Responsibility for sending the acceptance acknowledgement is not established by these sources.

## Legend

1. Role boxes group actions by the person or team described in the source.
2. Rectangles show actions or recorded outcomes.
3. Diamonds show a decision that needs evidence.
4. Labelled arrows show the reason for a branch or a repeat check.
5. A handoff ends tracking only after acceptance; it does not show service resolution.
