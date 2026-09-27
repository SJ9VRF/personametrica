# NeurIPS research-readiness audit

- **Threshold-free selective risk:** AURC remains lower for PBS (0.0107 vs. 0.0208), motivating joint reporting of state accuracy, calibration, risk–coverage, and operating-point utility.

## Best submission framing

**Evaluations & Datasets / evaluation framework** is currently more defensible than a General-track claim of a new frontier personalization method. The contribution is an evaluation insight plus reusable executable framework: state accuracy can disagree with calibrated action-level quality.

## Evidence already executed locally

- PersonaMetrica-Bench standard + four distribution shifts.
- 500-user exported standard benchmark: 27,133 observations / 13,500 queries.
- Six executable baselines.
- Ten-seed paired PBS vs trusted-latest statistics.
- Threshold-free risk–coverage analysis.
- Utility-threshold/defer-cost sensitivity sweep.
- Existing OS ablations, privacy, recovery, failure analysis, robustness, and reward-data audits.
- Human annotation task pack and UI (protocol complete; labels not fabricated).
- External-model evaluator (contract complete; model results not fabricated).

## Findings worth centering

1. **Evaluation-protocol reversal:** under 800-turn histories, native-confidence fixed-threshold utility favors PBS, but giving every tracker the same development-only post-hoc calibration flips the utility ordering in favor of time-aware-latest. This makes confidence calibration part of the evaluation protocol, not an implementation footnote.
2. **Metric sensitivity:** utility ranking is not universal across arbitrary action thresholds; risk–coverage is therefore the more defensible primary metric.
3. **Temporary-scope failure:** latest-memory baselines degrade sharply when temporary exceptions are common.
4. **Long-horizon result:** trusted-latest remains highly accurate but poorly calibrated as an action substrate; PBS preserves high selective accuracy.

## External evidence still required for a strong conference submission

These cannot be honestly completed without real model calls or participants:

1. Evaluate actual LLM/memory stacks on HorizonBench, PrefEval, LongMemEval, and preferably PerMemBench.
2. Obtain independent human labels for at least a statistically meaningful subset of belief/proactivity tasks; report agreement and adjudication.
3. Replace structured evidence with model-extracted evidence in the end-to-end primary table.
4. Add real downstream tasks (recommendation/planning/tool use) where wrong personalization has measurable consequence.
5. If targeting a method paper rather than E&D: train a learned updater/write policy or personalized action policy and compare it to strong learned baselines.

## Submission integrity

Do not convert protocol artifacts into “results.” Keep human/model columns marked `not run` until executed. For a double-blind submission, anonymize project URLs, author metadata, and release identifiers.


## v3.8 measurement hardening

The release adds `reports/LEADERBOARD_STABILITY_AUDIT.md` and `reports/BENCHMARK_HEALTH_AUDIT.md`. The former expands protocol sensitivity from one pair to all six baselines; the latter release-gates identity overlap, full-history overlap, duplicate histories, query balance, temporary-scope coverage, answer skew, and saturation. These strengthen controlled-evaluation validity but do not replace external model or human validation.

## v3.9 statistical robustness hardening

The release now adds two uncertainty checks around the central protocol-sensitivity result. `reports/LEADERBOARD_SEED_UNCERTAINTY.md` resamples complete long-horizon simulator seeds as paired units on a separate 10-user-per-seed diagnostic cohort; the 2,000-bootstrap interval for winner-change probability is 0.507–0.538, and every bootstrap replicate remains above 0.40. `reports/PROTOCOL_GRID_ROBUSTNESS.md` removes each calibration family, threshold, and deferral-cost level in turn; all 13 perturbed grids still contain multiple winners.

These checks reduce two obvious objections—seed accident and dependence on one grid level—but they do **not** create external validity. The bootstrap interval quantifies variation under the synthetic generator only, and the grid perturbations are sensitivity analyses rather than a probability distribution over deployment protocols.

An executable HorizonBench result adapter is also included. It follows the public per-item result schema and is smoke-tested only with synthetic fixtures. No HorizonBench or frontier-model score is claimed until real result JSONL files are provided.
