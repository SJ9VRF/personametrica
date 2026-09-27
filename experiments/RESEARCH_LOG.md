# Research Log

## H1 — Temporal supersession reduces stale personalization
**Experiment:** compare a temporal state model against first-mention memory under seeded preference drift.  
**Result:** supported on the synthetic controlled benchmark.  
**Caveat:** generator and extractor share intentionally simple linguistic structure; broader paraphrase robustness remains untested.

## H2 — Risk-aware intervention avoids high-stakes direct action
**Experiment:** low-risk deadline, uncertain intent, high-stakes irreversible action, low-value interruption.  
**Result:** deterministic policy routes uncertainty/high-stakes cases to `ask` and deadline case to a helpful intervention.  
**Next:** expand scenarios and calibrate against human preferences.

## Failed/limited assumptions
- A perfect score on narrow deterministic scenarios is not meaningful evidence of broad capability; baseline comparison and explicit scope labels were added.
- Heavy learned post-training cannot be honestly demonstrated without model weights/compute; the project instead exports auditable preference data and keeps a clean training interface.
