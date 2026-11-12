# Local enquiry tracking application

Version 0.1.1. A supporting exercise for [TR-01–TR-07](../../docs/05-requirements/tracking-prototype-requirements.md), separate from the later AI experiment. Uses Python 3.12 and its standard library; no paid services or external packages are needed.

## Start locally

From the repository root:

```powershell
python prototype/tracking/app.py --init
python prototype/tracking/app.py
```

Open <http://127.0.0.1:8765>. Initialisation creates four accounts and stores their generated passwords in `prototype/tracking/local-data/credentials.json`, excluded from Git. View that file locally to sign in; do not upload it. Repeating initialisation does not reset existing accounts. Treat this computer and its local files as trusted.

Accounts: rep-a, rep-b, rep-c and supervisor-a. Representatives can create their own enquiries. Supervisors can see all enquiries and arrange cover or permanent transfer. Use separate browser sessions or sign out between identities.

Enter synthetic information only. Received time includes its offset, for example `2026-11-11T09:00:00-06:00`. The collection address is optional when first recording an enquiry; describe outstanding details in the missing-information field. Staff manually revise that text when information arrives. This version does not infer whether an address is valid or clear outstanding details automatically.

The application saves enquiries and history in SQLite. Correspondence is stored, not sent. Follow-up dates do not trigger jobs or automatic closure. The original status configuration is not loaded: this limited application keeps enquiries Open and implements no referral/closure workflow.

## Run automated acceptance checks

```powershell
python prototype/tracking/test_acceptance.py
```

The runner starts real local HTTP processes with separate authenticated accounts and temporary databases, restarts them for persistence checks, and removes temporary credentials afterwards. Version hashes, outcomes and observations are saved under `results/tracking-prototype/<run-id>/`. These tests do not change the interactive application's database.

An isolated clock is available for test runs through `--test-today YYYY-MM-DD`; it changes only the application's overdue calculation, not history timestamps or the computer clock. Default interactive operation uses the computer's local date. Histories use UTC.

## Design decisions and limits

- Bind only to 127.0.0.1; intended for a single trusted workstation. Do not expose this demonstration to a network or production users.
- Generated passwords are hashed in the database; sessions and request tokens are checked server-side. Sessions expire after eight hours or a restart. There is no identity-provider integration, password recovery, login throttling, TLS deployment or comprehensive security review.
- Server-side permissions restrict enquiry reads and updates. Temporary cover can be revoked while a session is active. Previously viewed information cannot be withdrawn from a browser.
- BR-01 transfer is supervisor-only; confirmation is a recorded supervisor assertion, not independent approval by the receiving person. Transfer is immediate. Remove active temporary cover before transfer; the application rejects that ambiguous combination instead of silently changing cover. These implementation choices require review.
- Missing-information and action fields are free text; follow-up is a calendar date, not a scheduled notification. Concurrent edits are serialised in database transactions but stale edits are not detected; multi-user conflict resolution remains a limitation.
- History cannot be edited through application routes. Someone with direct database access can alter it; it is not tamper-proof audit storage.
- Automated HTTP results do not replace browser usability checks or business acceptance. Prototype results do not verify municipal capability or remove the publication hold.

## Azure DevOps

Keep source and versioned evidence in the private GitHub repository. Link requirements, tests and defects from Azure Boards. An optional pipeline definition is supplied separately; no pipeline is configured or executed by starting this application. Test Plans licensing and project permissions must be checked before using that service.

