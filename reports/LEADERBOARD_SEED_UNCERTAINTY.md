# Leaderboard Seed-Uncertainty Audit

## Question

On a lower-cost 10-user-per-seed diagnostic cohort, does protocol-sensitive ranking survive paired resampling of the same ten long-horizon seeds?

The sampling unit is a complete long-horizon seed. Each bootstrap replicate resamples the same seed indices jointly for every method and every protocol cell, preserving paired comparisons. Calibration remains fit only on development seeds 1–3.

## Result

| Quantity | Point estimate | 95% seed-bootstrap CI |
|---|---:|---:|
| Winner-change probability | 0.516 | [0.507, 0.538] |
| Mean Kendall tau | 0.702 | [0.692, 0.720] |
| Minimum Kendall tau | 0.200 | [0.200, 0.200] |

Across 2,000 paired seed bootstraps, P(winner-change probability > 0.40) = **1.000** and P(mean Kendall tau < 0.90) = **1.000**.

The original per-cell winner is not equally certain: mean bootstrap support is 0.987, while the least stable cell has support 0.619. This is expected and is precisely why PersonaMetrica reports ranking stability rather than presenting every cell winner as ground truth.

## Boundary

This is a lower-cost diagnostic cohort, separate from the 40-user-per-seed primary leaderboard audit. It measures uncertainty under the synthetic generator seeds used by PersonaMetrica. It is **not** a confidence interval over real users, model families, or deployment environments. External model and human validation remain separate evidence requirements.
