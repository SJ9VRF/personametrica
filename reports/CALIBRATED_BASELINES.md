# Development-Calibrated Baseline Evaluation

All trackers receive the same post-hoc opportunity: raw confidence is mapped to Laplace-smoothed empirical correctness on development seeds 1–3 only. The mapping is frozen before held-out seeds 10–19 and long-horizon seeds 30–39. This test asks whether the paper's decision-quality findings survive simple baseline calibration.

## Standard held-out means

| Method | Accuracy | Coverage | Selective acc. | Utility | Brier ↓ |
|---|---:|---:|---:|---:|---:|
| first-mention | 0.629 | 0.000 | 0.000 | -0.100 | 0.233 |
| latest-observation | 0.478 | 0.000 | 0.000 | -0.100 | 0.250 |
| sliding-window-40 | 0.245 | 0.000 | 0.000 | -0.100 | 0.142 |
| trusted-latest | 0.861 | 0.934 | 0.912 | 0.763 | 0.072 |
| time-aware-latest | 0.914 | 1.000 | 0.914 | 0.828 | 0.067 |
| personal-belief-state | 0.937 | 0.916 | 0.965 | 0.844 | 0.048 |

## 800-turn held-out means

| Method | Accuracy | Coverage | Selective acc. | Utility | Brier ↓ |
|---|---:|---:|---:|---:|---:|
| first-mention | 0.662 | 0.000 | 0.000 | -0.100 | 0.224 |
| latest-observation | 0.347 | 0.000 | 0.000 | -0.100 | 0.245 |
| sliding-window-40 | 0.167 | 0.000 | 0.000 | -0.100 | 0.117 |
| trusted-latest | 0.818 | 0.967 | 0.843 | 0.660 | 0.121 |
| time-aware-latest | 0.844 | 1.000 | 0.844 | 0.687 | 0.122 |
| personal-belief-state | 0.829 | 0.750 | 0.908 | 0.588 | 0.119 |

## Interpretation

This calibration is intentionally low-capacity and uses no test labels. It is not a substitute for learned confidence models, but it removes the easiest objection that structured baselines were forced to act with their raw generator confidence.
