# Protocol-Grid Robustness Audit

## Question

Does the ranking-instability headline disappear if one reasonable calibration family, action threshold, or deferral-cost level is removed from the frozen grid?

We run 13 leave-one-level-out perturbations: three calibration-family removals, five threshold removals, and five deferral-cost removals. No test result is used to invent a replacement grid.

## Result

| Perturbation family | Range across leave-one-level-out variants |
|---|---:|
| Winner-change probability | 0.327 – 0.564 |
| Mean Kendall tau | 0.653 – 0.895 |
| Variants retaining >1 winner | 13 / 13 |

The weakest perturbation is dropping native confidence: the remaining development-calibrated protocols agree substantially more, but they still select more than one winner. This is informative rather than inconvenient: much of the instability comes from whether systems are compared in their native confidence scales or after equal development-only calibration.

## Boundary

This sensitivity analysis protects against one obvious grid-design objection. It does not prove that the chosen grid exhausts all valid deployment utilities, nor does it assign a probability distribution over protocol choices.
