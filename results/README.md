# Evidence index

## Final classification evidence

- [Frozen final report](classification/held-out-final/report.md).
- [Predictions, metrics, versions and hashes](classification/held-out-final/predictions.json).
- [Interpretation and recommendation](../docs/06-evaluation/classification-results-and-recommendation.md).

This is the single scored comparison on 38 retained synthetic texts. It remains at its original path. No evaluation was rerun during repository packaging.

## Supporting tracking evidence

- Latest version 0.1.1 automated evidence: [20261112T224218784803Z report](archive/tracking-prototype/20261112T224218784803Z/report.md), [results](archive/tracking-prototype/20261112T224218784803Z/results.json). Eight automated groups passed. This is local HTTP evidence, not Azure execution or full manual sign-off.
- Clean assisted TC-01 repeat: [before](tracking-prototype/TC01-clean-2026-11-12-before.json), [after and outcome](tracking-prototype/TC01-clean-2026-11-12-after.json).
- [Consolidated test summary](../docs/06-evaluation/tracking-prototype-test-summary.md) retains the manual deviations, targeted checks and limits.
- [Tracking execution overview](tracking-prototype/README.md) explains initial environment failures and later successful runs.

The dated run folder is archived for organisation, not superseded by a new run. The summary and clean repeat must be read with it. Local prototype evidence does not verify municipal operation or release held guidance.

## Development history

| Run | Purpose | Evidence |
|---|---|---|
| development-20261114T194628045453Z | Keyword checks on known development examples | [Report](archive/classification/development-20261114T194628045453Z/report.md) |
| ai-development-20261114T200027864720Z | Original prompt on development examples | [Report](archive/classification/ai-development-20261114T200027864720Z/report.md) |
| ai-development-20261114T200233209487Z | Single revised prompt on development examples | [Report](archive/classification/ai-development-20261114T200233209487Z/report.md) |
| 20261111T214527349490Z | Tracking startup attempt; environment connection/cleanup errors | [Report](archive/tracking-prototype/20261111T214527349490Z/report.md) |
| 20261111T214623165290Z | Tracking startup attempt; environment connection errors | [Report](archive/tracking-prototype/20261111T214623165290Z/report.md) |
| 20261111T214650602254Z | Original successful tracking baseline; seven groups passed | [Report](archive/tracking-prototype/20261111T214650602254Z/report.md) |

Development outcomes are not unseen evaluation results. Failed environment attempts remain failures. [Prompt revision review](classification/prompt-revision-review.md) and [local setup](classification/local-setup-summary.md) retain their qualifications. [Configuration inspection](local-configuration-inspection.md) checks file declarations only. The [acceptance-message dry run](acceptance-message-dry-run/report.md) is a simulation, not a staff workload measurement or actual message delivery.

## Preservation and historical paths

Frozen evaluation data, snapshots and the final held-out report remain unchanged. Every archived `predictions.json` and `results.json` retains its original bytes. Embedded historical path strings are records of the original execution and were not rewritten. Relative links in editable Markdown were updated for the move.

Two original links in frozen snapshots do not resolve from the snapshot directory. They remain unchanged under the preservation rule:

| Protected snapshot | Original link target | Current readable destination |
|---|---|---|
| `data/classification-evaluation/frozen-approach/classification-evaluation-plan.md` | `../../data/labelling-guide.md` | [Labelling guide](../data/labelling-guide.md) |
| `data/classification-evaluation/frozen-approach/labelling-guide.md` | `../docs/04-options/classification-source-check.md` | [Source check](../docs/04-options/classification-source-check.md) |
