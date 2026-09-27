# Calibration Protocol Analysis

## Why this analysis exists

The earlier benchmark compared trackers using their native confidence values. Because downstream utility uses a fixed confidence threshold, unequal confidence calibration can itself determine which system acts. We therefore give **every tracker the same low-capacity post-hoc calibration opportunity on development seeds 1–3 only** and freeze that mapping before evaluation.

## Long-horizon result

| Protocol | Time-aware latest utility | PBS utility | PBS − baseline | Ranking |
|---|---:|---:|---:|---|
| Native confidence | — | — | +0.284 | PBS higher |
| Dev-calibrated confidence | 0.687 | 0.588 | -0.099 | time-aware latest higher |

**The ordering flips.** This invalidates any broad claim that the fixed-threshold utility result by itself proves PBS is the better long-horizon decision substrate. Instead, the result demonstrates that utility at a fixed action threshold is partly a property of the calibration protocol.

## Threshold-free confidence ordering

AURC (lower is better): time-aware latest = **0.0208**, PBS = **0.0107**. Post-hoc monotone calibration does not change the ordering of confidence scores, so AURC is the cleaner primary comparison for selective risk in this controlled setting.

## Reporting recommendation

Personal-agent evaluations that let confidence control action should report at least: (1) state accuracy, (2) calibration quality, (3) risk–coverage/AURC, and (4) utility only under an explicitly specified and equally calibrated decision protocol. Reporting fixed-threshold utility from native confidence values can create a ranking that disappears or reverses after fair calibration.

## Boundary

This is a controlled simulator result. The calibrator is intentionally simple (Laplace-smoothed empirical correctness by raw-confidence bucket); it does not establish that the same reversal occurs for learned frontier-model confidence. It establishes a concrete evaluation confound that future model-backed studies should control.
