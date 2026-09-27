# Belief stress grid

48 cells = 4 distractor-noise rates × 4 behavioral-noise rates × 3 temporary-preference rates. Each cell evaluates 90 users × 240 turns.

PBS wins on decision utility in **46/48** cells and on raw state accuracy in **34/48** cells.
Mean utility delta vs time-aware-latest: **+0.138**. Worst cell: **-0.025**.

## Hardest cells

| distractor noise | behavior noise | temporary rate | Δ accuracy | Δ utility |
|---:|---:|---:|---:|---:|
| 0.45 | 0.55 | 0.60 | +0.018 | -0.025 |
| 0.45 | 0.55 | 0.35 | +0.044 | -0.005 |
| 0.45 | 0.55 | 0.10 | +0.056 | +0.003 |
| 0.30 | 0.55 | 0.10 | +0.070 | +0.023 |
| 0.45 | 0.40 | 0.35 | +0.029 | +0.042 |

This grid is a simulator stress test, not evidence of performance on human interaction distributions.
