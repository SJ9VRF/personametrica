# Frontier agent-eval checklist

A compact release checklist for research-quality agent evaluation.

- [x] Task, trial, trajectory, grader are separate objects.
- [x] Multiple trials per task are supported and uncertainty is reported.
- [x] Final-state and trajectory-level graders are compared.
- [x] Tool **and action** constraints are graded.
- [x] Permission boundaries are graded before the first consequential action.
- [x] Verification is recomputed from expected/observed state rather than trusting a success bit.
- [x] Missing evidence can yield `Unknown` / abstention.
- [x] Grader mutation tests cover benign noise, forged success, missing observations, late confirmation, and tool loops.
- [x] Grader threshold drift is reported.
- [x] Grader code is content-fingerprinted.
- [x] Grader disagreements are exported to a human-review queue.
- [x] A blinded trajectory-annotation pack is included.
- [x] Failure-derived correction data is task-disjoint and audited for template duplication.
- [x] Reward-proxy stress tests expose sycophancy/autonomy failure modes.
- [x] Regression gates block known behavior regressions.
- [ ] Independent human grader calibration executed.
- [ ] Frontier/open-weight agent trials executed.
- [ ] Post-training on failure-derived data executed and evaluated on held-out naturalistic failures.

Unchecked items are external evidence requirements, not claimed results.
