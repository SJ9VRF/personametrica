# Personal Belief State Benchmark

Controlled structured-evidence benchmark. This isolates belief updating from natural-language extraction; it does not constitute frontier-model evaluation.

## Standard

| Method | State accuracy | Coverage | Selective accuracy | Decision utility | Brier ↓ |
|---|---:|---:|---:|---:|---:|
| first-mention | 0.634 | 1.000 | 0.634 | 0.269 | 0.366 |
| latest-observation | 0.481 | 1.000 | 0.481 | -0.039 | 0.519 |
| sliding-window-40 | 0.249 | 0.580 | 0.429 | -0.125 | 0.331 |
| trusted-latest | 0.853 | 0.631 | 0.908 | 0.478 | 0.129 |
| time-aware-latest | 0.906 | 0.611 | 1.000 | 0.572 | 0.080 |
| personal-belief-state | 0.932 | 0.824 | 0.977 | 0.768 | 0.060 |

## High Noise

| Method | State accuracy | Coverage | Selective accuracy | Decision utility | Brier ↓ |
|---|---:|---:|---:|---:|---:|
| first-mention | 0.572 | 1.000 | 0.572 | 0.143 | 0.428 |
| latest-observation | 0.250 | 1.000 | 0.250 | -0.500 | 0.750 |
| sliding-window-40 | 0.182 | 0.801 | 0.227 | -0.457 | 0.619 |
| trusted-latest | 0.858 | 0.616 | 0.913 | 0.471 | 0.127 |
| time-aware-latest | 0.908 | 0.598 | 1.000 | 0.558 | 0.081 |
| personal-belief-state | 0.922 | 0.806 | 0.969 | 0.736 | 0.069 |

## Implicit Heavy

| Method | State accuracy | Coverage | Selective accuracy | Decision utility | Brier ↓ |
|---|---:|---:|---:|---:|---:|
| first-mention | 0.625 | 1.000 | 0.625 | 0.250 | 0.375 |
| latest-observation | 0.555 | 1.000 | 0.555 | 0.111 | 0.445 |
| sliding-window-40 | 0.369 | 0.699 | 0.528 | 0.009 | 0.330 |
| trusted-latest | 0.821 | 0.368 | 0.896 | 0.229 | 0.161 |
| time-aware-latest | 0.855 | 0.346 | 1.000 | 0.280 | 0.130 |
| personal-belief-state | 0.875 | 0.846 | 0.926 | 0.705 | 0.089 |

## Temporary Heavy

| Method | State accuracy | Coverage | Selective accuracy | Decision utility | Brier ↓ |
|---|---:|---:|---:|---:|---:|
| first-mention | 0.621 | 1.000 | 0.621 | 0.242 | 0.379 |
| latest-observation | 0.448 | 1.000 | 0.448 | -0.104 | 0.552 |
| sliding-window-40 | 0.239 | 0.596 | 0.401 | -0.159 | 0.357 |
| trusted-latest | 0.757 | 0.688 | 0.748 | 0.309 | 0.222 |
| time-aware-latest | 0.920 | 0.630 | 1.000 | 0.593 | 0.073 |
| personal-belief-state | 0.935 | 0.826 | 0.978 | 0.773 | 0.059 |

## Long Horizon

| Method | State accuracy | Coverage | Selective accuracy | Decision utility | Brier ↓ |
|---|---:|---:|---:|---:|---:|
| first-mention | 0.678 | 1.000 | 0.678 | 0.356 | 0.322 |
| latest-observation | 0.355 | 1.000 | 0.355 | -0.291 | 0.645 |
| sliding-window-40 | 0.174 | 0.509 | 0.343 | -0.209 | 0.334 |
| trusted-latest | 0.820 | 0.297 | 0.905 | 0.170 | 0.161 |
| time-aware-latest | 0.844 | 0.280 | 1.000 | 0.207 | 0.138 |
| personal-belief-state | 0.831 | 0.618 | 0.937 | 0.503 | 0.121 |

