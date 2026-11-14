# Waste-enquiry classification experiment

Current implementation: keyword baseline, local Qwen2.5 3B inference and a completed frozen synthetic evaluation. See the [final experiment results](../../docs/06-evaluation/classification-results-and-recommendation.md) for the trade-off and limitations. No further model or prompt tuning is proposed.

Run from the repository root:

```powershell
python prototype/classification/run_development.py
```

No additional packages are needed. The classifier receives text only; the runner separately compares predictions with expected labels. Output includes matched patterns for explanation, not calibrated confidence.

The baseline searches three groups of lexical patterns. One matching group produces a type; none or multiple groups produce human review. It deliberately makes no claim of semantic interpretation: negation, historical context and distinct versus contextual requests are known limitations. Do not call this an optimised production rules engine or treat predictable weaknesses as proof AI is superior.

Development evidence is saved under results/classification with input/code hashes and per-example predictions. Any refinements are development work and must be recorded before evaluation freeze. Do not tune against future held-out results. See the experiment brief, labelling guide and evaluation plan for the actual task definition and success measures.

## Local AI setup

On November 14, the user authorised installation of the official Ollama Windows package and download of `qwen2.5:3b`. Ollama version 0.40.16 was installed through the winget package Ollama.Ollama. The model download passed the runner's digest check. GPU detected: RTX 4050 Laptop, approximately 6 GiB VRAM. These facts establish installation, not inference quality.

The model service listens locally on port 11434. No cloud model, account sign-in, API key or paid service was used. Keep model weights in the user's local model store, not this repository. Model terms are supplied with the model; no broad commercial-licensing claim is made here.

The draft prompt is `classification-prompt.txt`. To check one already-known development example:

```powershell
python prototype/classification/smoke_local_model.py
```

The script uses the documented Ollama chat API with a JSON schema, temperature 0, seed 42 and context 2048. Only the development example's text goes to the model; the runner compares its result with the known label afterwards. It retains version/digest metadata, settings, raw response, schema checks, first-call wall time and GPU residency evidence when available. Matching one known example does not establish accuracy, baseline superiority, repeatability or held-out performance. First-call model load/warmup time is not steady-state latency.

References: [Ollama Windows documentation](https://docs.ollama.com/windows), [model listing](https://ollama.com/library/qwen2.5:3b), [chat API](https://docs.ollama.com/api/chat), [structured outputs](https://docs.ollama.com/capabilities/structured-outputs).

## Recorded runs and reproducibility

- `run_ai_development.py`: paired diagnostics on the twenty reviewed development examples. Raw responses and source/settings hashes are retained per run.
- The original prompt is preserved in prompts/classification-v0.1.txt; classification-prompt.txt is the single revised working prompt.
- `prepare_evaluation.py` created approach snapshots and forty candidate evaluation examples once. It refuses overwrite. Do not regenerate these files to improve results.
- `run_held_out.py` performed the single scored run after label review and two exclusions. It checks model/source/dataset hashes and refuses to overwrite results/classification/held-out-final.
- [Frozen approach](../../data/classification-evaluation/frozen-approach/manifest.json), [dataset freeze](../../data/classification-evaluation/evaluation-freeze.json) and [raw final results](../../results/classification/held-out-final/predictions.json) retain provenance. Later editorial documentation changes may differ from source hashes; use the retained snapshots to inspect the evaluated version, not the latest prose.
- The runner uses local HTTP requests to Ollama. If the execution environment blocks localhost, authorised local connectivity is required. No cloud fallback or hidden retries exist.
- The twenty development examples and the thirty-eight evaluated examples are now seen evidence. Any future result-informed refinement needs a new evaluation design/set for a fresh unseen-performance claim.
