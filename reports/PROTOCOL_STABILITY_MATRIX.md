# Protocol Stability Matrix

## Question

Does the long-horizon utility ranking between the two strongest controlled systems remain stable across plausible evaluation protocols?

The protocol grid is fixed **without using long-horizon diagnostic labels for protocol selection**. We cross three confidence treatments (native, development-only bucket calibration, development-only isotonic calibration) with five action thresholds and five deferral costs, for **75 protocol cells**. Calibrators are fit on a development cohort (60 users per seed, seeds 1–3) and frozen before an independent long-horizon diagnostic cohort (40 users per seed, seeds 30–39). The larger primary benchmark remains unchanged; this smaller cohort exists to make the protocol sweep reproducible within the release budget.

## Result

| Quantity | Value |
|---|---:|
| PBS wins | 30 / 75 |
| Time-aware-latest wins | 45 / 75 |
| Ties | 0 / 75 |
| Pairwise protocol rank-reversal rate | 0.486 |
| Winner entropy | 0.971 bits |

A high reversal rate means that two defensible protocol choices frequently induce opposite pairwise selections. This is a property of the **evaluation protocol**, not evidence that either system is intrinsically best.

## By calibration family

| Calibration | PBS wins | Time-aware wins | Ties | Mean PBS - baseline utility |
|---|---:|---:|---:|---:|
| native | 20 | 5 | 0 | +0.189 |
| bucket-laplace | 5 | 20 | 0 | +0.002 |
| isotonic-laplace | 5 | 20 | 0 | -0.010 |

## Why this is stronger than a single rank flip

The earlier result showed one native-vs-calibrated reversal at a fixed threshold/cost. This matrix asks whether that observation survives a broader set of reasonable protocol choices. It also makes a cherry-picking failure mode visible: selecting a threshold or confidence treatment after inspecting test outcomes can select the preferred system.

## Boundary

The grid is still a controlled synthetic study. Its purpose is measurement diagnosis. It does not establish that the same reversal frequency holds for frontier models or human preference distributions. External model-backed validation is required before making a population or leaderboard claim.
