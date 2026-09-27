# Grader reliability and drift audit

This audit treats the evaluator as a system that can itself fail. It stress-tests invariance, missing evidence, threshold drift, score calibration, and the stability of estimates under repeated stochastic trials.

## Metamorphic / evidence tests

| Check | Result |
|---|---:|
| Benign-event invariance | 100.0% |
| Forged success-flag invariance | 100.0% |
| Missing-observation abstention | 100.0% |
| Late-confirmation detection | 100.0% |
| Excess tool-loop detection | 100.0% |

## Score calibration

| Grader | Brier ↓ | ECE ↓ |
|---|---:|---:|
| end_state_only | 0.329 | 0.329 |
| trajectory_policy | 0.379 | 0.505 |
| robust_trajectory | 0.315 | 0.465 |
| evidence_aware_trajectory | 0.315 | 0.465 |
| dense_trajectory_reward | 0.296 | 0.435 |

## Composite-threshold drift

Changing a weighted grader threshold can materially change false accepts; the release therefore reports threshold sensitivity rather than treating one threshold as ground truth.

| Threshold | Accuracy | False accept |
|---:|---:|---:|
| 0.55 | 57.5% | 57.9% |
| 0.65 | 57.5% | 57.9% |
| 0.75 | 67.1% | 44.8% |
| 0.85 | 79.1% | 28.4% |
| 0.95 | 89.6% | 14.1% |
| 1.00 | 89.6% | 14.1% |

## Multi-trial stability

Task-level robust-grader pass rate: **26.6%** (bootstrap 95% CI 25.0–28.1%).

| Trials/task | Mean estimate | Sampling SD |
|---:|---:|---:|
| 1 | 26.7% | 4.13 pp |
| 2 | 26.6% | 2.92 pp |
| 4 | 26.7% | 2.12 pp |
| 8 | 26.6% | 1.54 pp |

## Interpretation

- A benign logging event should not change a verdict.
- A forged success flag should not override state evidence.
- If critical observation evidence is missing, the evidence-aware grader abstains rather than inventing certainty.
- One stochastic trial per task yields a noisier estimate than repeated trials; trial count is therefore part of the eval protocol, not a cosmetic choice.

These are controlled synthetic tests of grader behavior, not human-grader calibration results. Independent human calibration remains an external-evidence requirement.
