# Reviewer Guide — where to spend your time — PersonaMetrica v1.3

If you have **5 minutes**, inspect these in order:

1. `README.md` — problem, architecture, controlled results, evidence boundaries.
2. `docs/architecture.svg` — closed-loop system at a glance.
3. `reports/RESULTS.md` — generated benchmark results.
4. `docs/EVIDENCE_LEDGER.md` — every important claim mapped to evidence and scope.
5. `reports/FAILURE_ANALYSIS.md` — where the system still fails.

If you have **15 minutes**, additionally inspect:

6. `personalagi/agent/core.py` — orchestration and user-control precedence.
7. `personalagi/memory/store.py` — temporal update, supersession, forgetting and audit.
8. `personalagi/proactivity/policy.py` — calibrated intervention policy.
9. `personalbench/runner.py` — benchmark implementation and real feature-toggle ablations.
10. `scripts/regression_gate.py` + `configs/regression_gates.json` — release quality gates.

## What is novel in the artifact

The project treats personal intelligence as a **closed-loop control and learning problem**, rather than as a vector database. It explicitly models temporal state, uncertainty, conflicting preferences, intervention judgment, user control, tool outcomes, evaluation regressions, and feedback-to-training interfaces.

## Model boundary

The local release uses a transparent deterministic inference adapter so every checked-in result is reproducible without a network or GPU. The runtime is not coupled to that estimator: `personalagi/adapters/` defines a structured inference contract, and `ReplayInferenceAdapter` can replay outputs from any external learned model through the *same* memory, privacy, goal, evaluation and regression infrastructure.

This is deliberate claim discipline: the repository does **not** report a learned-model result that was not actually executed.

## Strongest evidence

- real temporal-update ablation
- real contradiction-resolution ablation
- calibrated-vs-uncalibrated proactivity ablation
- outcome-verification ablation
- privacy-guard ablation
- 10-seed paired effect analysis
- adversarial preference-language stress suite
- 1,000-scenario failure slicing
- regression gates that fail the release if core behavioral metrics degrade

## Known boundary

The benchmark population is synthetic. A human longitudinal study protocol is included but intentionally not represented as completed evidence.
