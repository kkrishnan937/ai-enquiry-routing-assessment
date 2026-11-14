# Local AI feasibility check

Date: November 14, 2026  
Status: Installation and single-example execution verified; no scored AI evaluation

Ollama 0.40.16 was installed from the official package using winget. Qwen2.5 3B was downloaded and verified by the runner. The local service detected the NVIDIA RTX 4050 Laptop GPU with approximately 6 GiB VRAM. No cloud inference, paid service or external API credentials were used.

The draft classification prompt and structured-output request were tested twice on the same known first development example. Only enquiry text, task instructions and schema were sent to the local model; expected labels were compared afterwards.

| Check | Result | Evidence |
|---|---|---|
| First request, including load/warmup | Valid output: missed_collection, review_required false; matched known development label. Wall time 139.31 seconds. | [First smoke record](local-smoke-20261114T195744467139Z.json) |
| Repeat of identical input while warm | Same valid output; wall time 0.48 seconds. | [Warm smoke record](local-smoke-20261114T195811677271Z.json) |

The identical warm request can benefit from prompt caching and is not a general steady-state benchmark. Neither two matching responses nor one known example establishes classification accuracy, superiority over rules or broad repeatability. Raw records retain model digest, prompt hash, settings, runner/GPU residency information and response timings. No held-out examples were generated or used.

## Next step

Run one documented AI development pass over the reviewed twenty examples, inspect failures and usability, and record any prompt/rule changes before freezing. Keep one baseline and one model; no extra application or model search is needed. Only then prepare and review the planned held-out set under the agreed controls.
