# Risk–Coverage Analysis

Lower area under the risk–coverage curve (AURC) is better. Unlike a single action threshold, AURC evaluates confidence ordering across the full coverage range.

| Method | Full accuracy | AURC ↓ |
|---|---:|---:|
| first-mention | 0.634 | 0.368 |
| latest-observation | 0.481 | 0.517 |
| sliding-window-40 | 0.249 | 0.616 |
| trusted-latest | 0.853 | 0.054 |
| time-aware-latest | 0.906 | 0.021 |
| personal-belief-state | 0.932 | 0.011 |
