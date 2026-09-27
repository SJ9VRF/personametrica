# Grader disagreement review queue

Cases where graders disagree are promoted to an explicit review queue rather than silently averaged away. This is the handoff point for independent human calibration or a separately validated judge model.

- Disagreement cases: 263
- High-priority (priority ≥4): 179

## By failure type

- `redundant_loop`: 84
- `forged_verification`: 83
- `missing_verification`: 81
- `unsafe_shortcut`: 15

The queue intentionally contains gold labels for offline research auditing. A blinded annotation export should remove `gold_*` fields before human evaluation.
