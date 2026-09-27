# PersonaMetrica Experiment Journal

This journal records experiments that have checked-in executable evidence. It is intentionally not a reconstructed day-by-day lab notebook. Entries are tied to released artifacts, commands, and measured outputs.

## EXP-001 — Temporal supersession versus first-mention memory
**Hypothesis.** A state model that supersedes stale preferences should outperform a first-mention memory under preference drift.  
**Setup.** Controlled synthetic personas; compare `full_temporal_os` with `no_temporal_update`.  
**Result.** Personalization accuracy 100.0% vs 37.1%; stale-memory rate 0.0% vs 62.9% on the local mechanism benchmark.  
**Interpretation.** Temporal replacement is necessary in this controlled setting, but the result is not a frontier-model or human-population claim.  
**Next decision.** Move from binary stale-state tests to probabilistic belief updating and long-horizon calibration.  
**Evidence.** `data/ablation_results.json`, `experiments/run_ablations.py`.

## EXP-002 — Calibrated proactivity versus uncalibrated intervention
**Hypothesis.** Confidence/stakes/reversibility-aware intervention should reduce over-autonomy.  
**Setup.** Compare `full_temporal_os` with `uncalibrated_proactivity`.  
**Result.** Proactivity accuracy 86.5% vs 17.0%; high-stakes confirmation 94.1% vs 0%; autonomy violation 0.0% vs 5.9%.  
**Interpretation.** Explicit decision boundaries matter more than simply increasing intervention frequency.  
**Next decision.** Keep uncertainty and permission boundaries explicit in the action policy and evaluation protocol.  
**Evidence.** `data/ablation_results.json`, `reports/FAILURE_ANALYSIS.md`.

## EXP-003 — Learned lexical reward baseline
**Hypothesis.** Exported preference pairs are learnable by a small ranking model.  
**Setup.** Sparse pairwise linear ranker; group-aware train/validation/test split; randomized-label negative control; lexically matched contrast set.  
**Result.** Train/validation/test accuracy reached 100%, but the lexically matched contrast set collapsed to 50.0%; randomized-label control was 49.3%.  
**Interpretation.** The apparent held-out success was largely compatible with lexical shortcuts and did not demonstrate semantic preference learning.  
**Next decision.** Preserve the negative result, restrict claims, and treat the scorer as a pipeline smoke test rather than a strong reward model.  
**Evidence.** `data/reward_baseline_results.json`, `reports/LEARNED_REWARD_BASELINE.md`.

## EXP-004 — Equal-opportunity confidence calibration
**Hypothesis.** PBS remains the better acting system when every tracker receives the same development-only confidence calibration opportunity.  
**Setup.** Fit Laplace-smoothed empirical correctness on development seeds 1–3; freeze before held-out seeds 10–19 and long-horizon seeds 30–39.  
**Result.** Native long-horizon utility favored PBS by +0.284, but development-calibrated utility favored time-aware-latest by 0.099. The ranking flipped.  
**Interpretation.** Fixed-threshold utility is not protocol-invariant.  
**Next decision.** Demote unmatched native-confidence utility to a diagnostic; promote shared calibration and threshold-free risk/coverage analysis.  
**Evidence.** `data/calibration_protocol_analysis.json`, `reports/CALIBRATION_PROTOCOL_ANALYSIS.md`.

## EXP-005 — Threshold-free risk–coverage audit
**Hypothesis.** Confidence ordering may remain useful even when one fixed action threshold changes the winner.  
**Setup.** Compare risk–coverage and AURC for time-aware-latest and PBS.  
**Result.** AURC: PBS 0.0107 vs time-aware-latest 0.0208 (lower is better).  
**Interpretation.** Calibration-sensitive utility and threshold-free confidence ordering answer different questions and should be reported separately.  
**Next decision.** Keep AURC as a primary confidence-quality diagnostic rather than forcing a single operating point.  
**Evidence.** `data/belief_risk_coverage.json`, `reports/BELIEF_RISK_COVERAGE.md`.

## EXP-006 — Held-out grader attack audit
**Hypothesis.** The v3.4 robust trajectory grader generalizes beyond the perturbations used while developing it.  
**Setup.** Freeze the prior evaluator, then introduce five held-out attack families: verification subset, payload mismatch with external repair, unlogged action, revoked permission, and verification-before-action.  
**Result.** End-state grader false accept 100%; frozen robust-trajectory grader 96%; causal-trajectory grader 0% on the authored held-out set.  
**Interpretation.** A trace-aware grader can still overfit its known failure taxonomy. Verification must be causal, permission-aware, and independently recomputed.  
**Next decision.** Replace self-reported success checks with a causal action/permission/verification contract.  
**Evidence.** `data/heldout_grader_attacks.json`, `reports/HELDOUT_GRADER_ATTACKS.md`.

## EXP-007 — Counterfactual belief interventions
**Hypothesis.** A useful personalized state should ignore irrelevant evidence, resist weak contradictory behavior, and still react to explicit current updates.  
**Setup.** 540 minimal-pair interventions over 180 synthetic users.  
**Result.** PBS nuisance invariance 98.0%, weak-conflict invariance 64.4%, explicit-update sensitivity 99.3%.  
**Interpretation.** PBS is not perfectly isolated from irrelevant evidence; about 2% of nuisance interventions still flip the decision.  
**Next decision.** Keep other-person contamination as an explicit failure mode instead of presenting perfect robustness.  
**Evidence.** `data/counterfactual_belief_eval.json`, `reports/COUNTERFACTUAL_BELIEF_EVAL.md`.

## EXP-008 — Full-leaderboard protocol stability
**Hypothesis.** Protocol sensitivity is not limited to one pair of systems.  
**Setup.** Rank all six released baselines over 75 frozen protocol cells (3 confidence protocols × 5 thresholds × 5 defer costs).  
**Result.** Time-aware-latest wins 45/75 cells, PBS 27/75, first-mention 3/75. Winner-change probability across protocol pairs is 51.6%; mean Kendall tau 0.699; worst-case tau 0.20.  
**Interpretation.** The leaderboard itself is an instrument-dependent object.  
**Next decision.** Report leaderboard stability, not only one chosen operating point.  
**Evidence.** `data/leaderboard_stability_audit.json`, `reports/LEADERBOARD_STABILITY_AUDIT.md`.

## EXP-009 — Paired seed-bootstrap uncertainty
**Hypothesis.** The leaderboard-instability result is not a fragile artifact of one synthetic seed sample.  
**Setup.** 2,000 paired bootstrap resamples over 10 long-horizon test seeds on a separate 10-user-per-seed diagnostic cohort.  
**Result.** Winner-change probability 0.516, 95% seed-bootstrap interval [0.507, 0.538]; mean Kendall tau 0.702 [0.692, 0.720]. In all bootstraps winner-change probability remained > 0.40.  
**Interpretation.** The effect is stable to synthetic-seed resampling, not established for humans or frontier models.  
**Next decision.** Keep simulator-seed uncertainty distinct from population uncertainty.  
**Evidence.** `data/leaderboard_seed_uncertainty.json`, `reports/LEADERBOARD_SEED_UNCERTAINTY.md`.

## EXP-010 — Leave-one-level-out protocol-grid robustness
**Hypothesis.** Ranking instability should not disappear when one calibration family, threshold, or defer-cost level is removed.  
**Setup.** 13 leave-one-level-out perturbations of the 75-cell frozen grid.  
**Result.** All 13 perturbations retain multiple winners; winner-change probability ranges 0.327–0.564.  
**Interpretation.** The headline is not driven by one grid level, though native confidence is a major destabilizer.  
**Next decision.** Keep native-confidence comparisons diagnostic and preserve the frozen grid registry.  
**Evidence.** `data/protocol_grid_robustness.json`, `reports/PROTOCOL_GRID_ROBUSTNESS.md`.

## EXP-011 — Benchmark health and leakage audit
**Hypothesis.** Development/test identities and full evolving histories should be disjoint, and the benchmark should not be trivially saturated or imbalanced.  
**Setup.** Hash complete user histories with identifiers removed; inspect query/domain balance and temporary-scope coverage.  
**Result.** Identity overlap 0; full-stream overlap 0; duplicate full histories 0; 13,500 standard queries; 144 temporary-scope queries; maximum answer skew 54.5%; best standard state accuracy 93.2%.  
**Interpretation.** The checked-in benchmark avoids the obvious leakage path, while finite-schema sub-record repetition remains expected.  
**Next decision.** Seed-scope identities and gate benchmark-health checks in releases.  
**Evidence.** `data/benchmark_health_audit.json`, `reports/BENCHMARK_HEALTH_AUDIT.md`.

## EXP-012 — Failure-derived correction-data audit
**Hypothesis.** Converting trajectory failures into correction pairs is sufficient evidence of useful post-training data.  
**Setup.** Audit 254 failure-derived pairs for semantic-template diversity and split leakage.  
**Result.** 254 exact-unique pairs but only 4 semantic templates; semantic-template duplication 98.4%. Task overlap between train/dev/test is 0.  
**Interpretation.** The pipeline works, but the current text supervision is too templated to support a meaningful post-training improvement claim.  
**Next decision.** Add structured correction records and task-disjoint splits; keep model-training improvement explicitly unclaimed.  
**Evidence.** `data/trajectory_failure_data_audit.json`, `reports/TRACE_FAILURE_DATA.md`.

## EXP-013 — Local scaling and cost audit
**Hypothesis.** The deterministic research substrate remains cheap enough to reproduce locally as horizon/user count grows.  
**Setup.** Scale from 200 to 15,000 interactions on the release environment.  
**Result.** 15,000 interactions completed in median 0.551 s (36.8 µs/interaction) with zero external API calls/cost in the default stack.  
**Interpretation.** This establishes local mechanism reproducibility, not frontier-model latency or serving economics.  
**Next decision.** Report external-model latency/cost only after measured adapter runs.  
**Evidence.** `data/scaling_results.json`, `reports/SCALING.md`.
