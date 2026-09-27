# PersonaMetrica Evidence Ledger

This is the claim contract for the repository. A headline claim belongs on the public surface only if it has an executable evidence path and an explicit boundary.

| Claim | Checked evidence | Fast executable check | Boundary |
|---|---|---|---|
| The six-system leaderboard is protocol-sensitive | `data/leaderboard_stability_audit.json`, `reports/LEADERBOARD_STABILITY_AUDIT.md` | `python scripts/reviewer_demo.py` | Controlled synthetic long-horizon histories; not a frontier-model leaderboard |
| Two random protocol cells disagree on the winner about 51.6% of the time in the frozen 75-cell grid | `data/leaderboard_stability_audit.json` | `python scripts/leaderboard_stability_audit.py` | Probability is over the released protocol grid, not all possible evaluation protocols |
| The ranking-instability conclusion survives seed resampling | `data/leaderboard_seed_uncertainty.json` | `python scripts/leaderboard_seed_uncertainty.py` | Bootstrap unit is simulator seed; interval is not human-population uncertainty |
| The conclusion survives one-level-at-a-time grid perturbations | `data/protocol_grid_robustness.json` | `python scripts/protocol_grid_robustness.py` | Tests the released grid neighborhood, not arbitrary metric families |
| Native-confidence utility and shared-calibration utility can select different systems | `data/calibration_protocol_analysis.json` | `python scripts/calibration_protocol_analysis.py` | Demonstrates protocol sensitivity, not universal superiority of either estimator |
| A frozen trajectory grader can fail badly OOD | `data/heldout_grader_attacks.json` | `python scripts/heldout_grader_attacks.py` | Authored synthetic attack families, not production agent traces |
| The causal-contract grader rejects all released held-out attacks | `data/heldout_grader_attacks.json` | `python scripts/reviewer_demo.py` | 0% false accept is only on the constructed released attack set |
| Counterfactual user-state tests expose both robustness and residual failure | `data/counterfactual_belief_eval.json` | `python scripts/counterfactual_belief_eval.py` | Structured synthetic evidence; no natural-language extraction claim |
| Benchmark split identities and full histories are disjoint | `data/benchmark_health_audit.json` | `python scripts/benchmark_health_audit.py` | Finite-schema event fragments can still repeat |
| The release protocol is frozen and fingerprinted | `configs/protocol_registry.json`, `data/protocol_registry_fingerprint.json` | `python scripts/validate_protocol_registry.py` | Repository-level lock; not externally timestamped preregistration |
| The runtime handles a live temporal preference update | `personalagi/` runtime | `python scripts/reviewer_demo.py` | Deterministic local mechanism check |
| Package imports and CLI run from a clean interpreter | `data/cold_start_audit.json`, `reports/COLD_START_AUDIT.md` | `python scripts/cold_start_audit.py` | In this runtime, build-backend installation may fall back to fresh-venv `.pth` isolation; report states which path ran |
| Repository release surfaces agree on author/version/claim boundaries | `data/hiring_surface_audit.json` | `python scripts/hiring_surface_audit.py` | Presentation consistency check, not scientific validation |

## Claims intentionally not made

- No completed human longitudinal study.
- No independent human grader-calibration result.
- No frontier/open-weight model leaderboard result.
- No claim of successful frontier-model post-training from the failure-derived correction data.
- No production deployment or live user-account action.
- No overall-SOTA claim for personal agents.
