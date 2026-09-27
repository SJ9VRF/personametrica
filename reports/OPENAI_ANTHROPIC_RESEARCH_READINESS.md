# OpenAI / Anthropic research-readiness audit

This audit asks whether the artifact supports the workflows expected in frontier agent research, not whether it imitates any internal system.

## Evidence surfaces now present

- **Long-horizon state evaluation:** PersonaMetrica-Bench evaluates evolving user state, calibration, risk–coverage, and decision utility.
- **Task / trial / grader / trajectory decomposition:** agent-level tasks have multiple controlled trials and inspectable graders.
- **State verification:** action success is checked against environment state rather than response text alone.
- **Trace grading:** permission, tool/action choice, verification, and bounded execution are scored separately.

- **Evaluator generalization:** five held-out attack families are evaluated separately from the original perturbations; the stricter causal-contract grader closes failures exposed only after the first evaluator was frozen.
- **Counterfactual personalization diagnostics:** paired interventions separately test nuisance invariance, weak-evidence robustness, and sensitivity to relevant explicit updates.
- **Evaluator reliability as a first-class target:** grader mutation tests, missing-evidence abstention, score calibration, threshold drift, and repeated-trial uncertainty are measured explicitly.
- **Disagreement routing:** incompatible grader verdicts are exported to a prioritized review queue instead of silently averaged.
- **Evaluator provenance:** checked-in results are content-bound to the exact grader/task implementation through a SHA-256 fingerprint.
- **Multi-tool contract checking:** reminders, notes, and tasks require correct tool+action pairs rather than tool-name-only grading.
- **Grader-gaming control:** forged self-reported verification success is rejected by recomputing expected-vs-observed state.
- **Failure-driven data flywheel:** false-accepted trajectories become explicit correction pairs.
- **Regression gates:** behavioral changes can block a release.
- **Negative results:** utility ranking reverses under equal calibration; reward baseline fails on semantic paraphrases; PBS is not uniformly best across stress cells.
- **Claim discipline:** human/frontier-model results remain unclaimed until executed.

## Remaining external evidence

1. Run real open-weight/frontier agents through the trace schema with multiple stochastic trials per task.
2. Execute the included blinded trajectory-calibration pack with independent human labels and report inter-rater reliability / human-vs-grader agreement.
3. Train a real model or policy on the failure-derived data and measure held-out improvement/regressions.
4. Run longitudinal human evaluation under an appropriate review/consent process.

These are execution dependencies, not missing interfaces: the schemas, graders, datasets, and scoring paths are already present.
