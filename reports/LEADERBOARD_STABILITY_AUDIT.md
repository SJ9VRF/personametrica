# Leaderboard Stability Audit

## Question

Does protocol sensitivity persist when all six released baselines are ranked together, rather than only comparing the two strongest structured systems?

We replay the same long-horizon histories for every method across the frozen 75-cell protocol family: three confidence treatments, five action thresholds, and five deferral costs. Calibration is fit only on development seeds 1-3. Long-horizon labels from seeds 30-39 are not used to select a protocol.

## Result

| Quantity | Value |
|---|---:|
| Protocol cells | 75 |
| Probability two protocol cells choose different winners | 0.516 |
| Mean Kendall tau across complete rankings | 0.699 |
| Minimum Kendall tau | 0.200 |
| Methods that win at least one cell | 3 / 6 |

### Winner counts

| Method | Winning cells | Mean rank | Best | Worst | Rank variance |
|---|---:|---:|---:|---:|---:|
| time-aware-latest | 45 | 1.67 | 1 | 3 | 0.76 |
| personal-belief-state | 27 | 2.12 | 1 | 3 | 0.83 |
| first-mention | 3 | 3.43 | 1 | 4 | 0.94 |
| latest-observation | 0 | 5.27 | 5 | 6 | 0.20 |
| sliding-window-40 | 0 | 5.73 | 5 | 6 | 0.20 |
| trusted-latest | 0 | 2.79 | 2 | 4 | 0.70 |

## Interpretation

The important object is not which method wins the most cells. It is that the identity and ordering of the leaderboard are not invariant to defensible operating-point choices. A weak or stale baseline winning any cell is a warning that coverage/confidence economics can dominate state quality if the protocol is poorly matched to the intended deployment decision.

This audit therefore supports a measurement claim: report threshold-free state/risk metrics together with any utility leaderboard, freeze calibration on development data, and expose ranking stability across plausible deployment costs. It does **not** establish an overall SOTA personal agent.
