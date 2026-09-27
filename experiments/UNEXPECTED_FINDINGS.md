# Unexpected Findings

## U-001 — Equal calibration reversed the apparent long-horizon winner
We expected PBS's native-confidence utility advantage to shrink under equal calibration, not reverse. It changed from **+0.284** PBS-vs-time-aware to **-0.099** after development-only calibration. This finding changed the paper's central claim from “PBS improves utility” to “fixed-threshold utility is protocol-sensitive.”

## U-002 — A weak stale baseline can win under some protocols
Across the 75-cell full leaderboard, **first-mention** wins 3 cells. This was not treated as evidence that first-mention is good; it exposed how coverage/confidence economics can elevate a poor state estimator.

## U-003 — The “robust” grader was the thing that failed
The v3.4 trajectory grader looked strong on known perturbations but false-accepted **96%** of held-out evaluator attacks. The evaluator, not the agent, became the main failure object.

## U-004 — Perfect reward-baseline test accuracy hid zero semantic margin
A local lexical ranker scored **100%** on the group-aware test split but only **50%** on a lexically matched contrast set. The negative result was more informative than the perfect headline score.

## U-005 — More exact-unique correction pairs did not mean more semantic diversity
The failure-to-data pipeline produced **254 exact-unique** pairs, but only **4 semantic templates**. Exact deduplication alone would have overstated training-data diversity.

## U-006 — Low-weight irrelevant evidence can still matter
PBS ignored other-person distractors in **98%** of paired cases, but the remaining ~2% showed that even low-reliability evidence can move a close belief competition across a decision boundary.

## U-007 — Removing native confidence stabilizes the leaderboard more than most threshold changes
In leave-one-level-out analysis, dropping the native-confidence protocol reduced winner-change probability to **0.327**, the strongest stabilization among the checked grid perturbations. This reinforced the decision to treat cross-system raw confidence as non-comparable.
