# Grader calibration protocol

The deterministic graders in this repository are **not** treated as universally correct judges. They are reference graders for controlled tasks. Any LLM-based or human-facing extension should be calibrated against independent review before being used for training or headline evaluation.

## Protocol

1. **Freeze the task specification and trace schema.** Do not edit rubrics after seeing test-model outputs.
2. **Use multiple stochastic trials per task.** Report the trial count and task-level uncertainty.
3. **Blind human reviewers.** Human calibration tasks omit simulator gold labels and automatic-grader outputs.
4. **Allow `Unknown`.** Missing evidence should produce abstention rather than a fabricated pass/fail judgment.
5. **Separate dimensions.** Grade final state, tool/action policy, permission, verification, efficiency, and evidence integrity independently before composing a score.
6. **Measure agreement.** Report human-human agreement, human-grader agreement, abstention rate, false accept, and false reject.
7. **Stress the grader.** Include forged success flags, missing observations, irrelevant trace events, late confirmations, wrong actions, partial states, and excessive loops.
8. **Version the evaluator.** Bind results to `data/grader_fingerprint.json`; evaluator changes require regenerated benchmark results.
9. **Route disagreements to review.** Use `data/grader_disagreement_queue.jsonl`; do not silently average incompatible verdicts.
10. **Keep training and evaluation disjoint.** Failure-derived correction records use task-disjoint train/dev/test splits and should not be used to claim semantic generalization without wording-held-out evaluation.

## Acceptance criteria before an LLM judge is trusted

The project intentionally does not fabricate these results. Before replacing the deterministic reference grader with an LLM judge, require independent human labels and report at minimum:

- human-human agreement;
- human-vs-judge accuracy / false-accept / false-reject;
- judge abstention rate;
- calibration (Brier/ECE for graded confidence if available);
- robustness on the mutation suite;
- stability across repeated judge calls or seeds.

This follows the same general principle used in frontier agent evaluation: traces and graders are useful only when the grading process itself is validated and resistant to bypasses.
