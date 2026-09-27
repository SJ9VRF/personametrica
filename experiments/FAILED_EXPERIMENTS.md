# What Did Not Work

These are released failures or revised hypotheses with checked-in evidence. They are not invented “messy research” anecdotes.

## F-001 — Native fixed-threshold utility did not survive equal calibration
**Initial hypothesis.** PBS's native-confidence long-horizon utility advantage reflected a better acting state representation.  
**What failed.** Once every tracker received the same development-only calibration opportunity, the long-horizon ordering reversed: native PBS gain +0.284 became -0.099 after shared calibration.  
**Why.** Raw confidence scales were not comparable across systems, so a common threshold implicitly favored one scale.  
**Change.** The paper demoted native-confidence utility, added shared calibration, AURC, and a 75-cell protocol audit.  
**Evidence.** `data/calibration_protocol_analysis.json`.

## F-002 — The “robust” trajectory grader failed on unseen attack families
**Initial hypothesis.** Trace-aware verification plus self-reported success checks generalized beyond the development perturbations.  
**What failed.** The frozen robust grader false-accepted 96% of five held-out attack families.  
**Why.** It verified the presence/content of trace events but not the causal relationship between permission, action, payload, timing, and observed state.  
**Change.** Added `CausalTrajectoryGrader`, recomputed verification from evidence, checked permission at action time, and required verification after the action.  
**Evidence.** `data/heldout_grader_attacks.json`.

## F-003 — A perfect lexical reward-model test score was misleading
**Initial hypothesis.** Group-aware held-out accuracy near 100% meant the exported preference pairs supported useful learned preference semantics.  
**What failed.** A lexically matched contrast set dropped to 50.0% accuracy.  
**Why.** The sparse ranker exploited lexical cues that survived the original split.  
**Change.** Kept the baseline as an end-to-end training smoke test, added negative controls/generalization audits, and removed semantic-learning claims.  
**Evidence.** `data/reward_baseline_results.json`.

## F-004 — Failure-derived text corrections were too templated
**Initial hypothesis.** Hundreds of exact-unique correction pairs were a sufficiently rich post-training substrate.  
**What failed.** 254 exact-unique pairs collapsed to only 4 semantic templates (98.4% template duplication).  
**Why.** The generator diversified identifiers and task instances more than correction semantics.  
**Change.** Added structured correction records, task-disjoint splits, data-quality audit, and kept actual post-training gain unclaimed.  
**Evidence.** `data/trajectory_failure_data_audit.json`.

## F-005 — Irrelevant “other person” evidence still contaminated PBS in a small slice
**Initial hypothesis.** Low-reliability other-person evidence could not change the active personal belief.  
**What failed.** PBS nuisance invariance was 98.0%, not 100%; a small set of minimal pairs crossed the decision boundary.  
**Why.** Low-weight evidence can still matter when competing beliefs are close.  
**Change.** Kept the 2% contamination rate as a known limitation and made counterfactual invariance a release-visible evaluation.  
**Evidence.** `data/counterfactual_belief_eval.json`.

## F-006 — A single leaderboard operating point was not a stable scientific summary
**Initial hypothesis.** One carefully chosen threshold/cost/calibration setting could summarize model selection.  
**What failed.** Across 75 defensible cells, three different systems win and protocol-pair winner change is 51.6%.  
**Why.** Coverage, confidence calibration, threshold, and defer economics interact with system behavior.  
**Change.** Report full ranking stability, Kendall tau, winner counts, bootstrap uncertainty, and grid perturbations.  
**Evidence.** `data/leaderboard_stability_audit.json`, `data/protocol_grid_robustness.json`.

## F-007 — Narrow perfect mechanism scores were not credible evidence of broad capability
**Initial hypothesis.** Deterministic 100% local mechanism scores were sufficient as the project's main proof.  
**What failed.** They did not test paraphrase robustness, distribution shift, evaluator gaming, or external models.  
**Why.** Narrow mechanisms and their test generator shared too much structure.  
**Change.** Added baselines, adversarial language, held-out grader attacks, external-result adapters, uncertainty audits, and explicit scope labels.  
**Evidence.** `experiments/RESEARCH_LOG.md`, `reports/ADVERSARIAL_EVAL.md`, `reports/HORIZONBENCH_ADAPTER_SMOKE.md`.
