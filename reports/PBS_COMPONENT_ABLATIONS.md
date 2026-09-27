# PBS component ablations

Held-out seeds 10–19; 160 users × 240 turns per seed. Full PBS hyperparameters remain frozen from development tuning.

| Variant | State acc. | Coverage | Utility | Brier ↓ |
|---|---:|---:|---:|---:|
| full | 0.937 | 0.831 | 0.779 | 0.058 |
| no_recency | 0.787 | 0.858 | 0.572 | 0.149 |
| no_provenance_reliability | 0.537 | 0.830 | 0.070 | 0.376 |
| no_temporary_expiry | 0.932 | 0.821 | 0.765 | 0.061 |
| no_context_scope | 0.928 | 0.829 | 0.761 | 0.065 |
| no_evidence_aggregation | 0.479 | 0.121 | 0.033 | 0.150 |

Interpretation: these ablations isolate which parts of PBS matter under the controlled generator. They do not establish causal importance for natural human conversations.
