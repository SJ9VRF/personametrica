# Scaling and Runtime Profile

Scope: local deterministic default stack; measured on the release-build environment, excludes electricity/hardware amortization and external model-backed adapters

| Users | Turns | Interactions | Median wall time | µs / interaction | External API cost |
|---:|---:|---:|---:|---:|---:|
| 10 | 20 | 200 | 0.017s | 87.15 | $0.00 |
| 25 | 60 | 1500 | 0.061s | 40.94 | $0.00 |
| 100 | 60 | 6000 | 0.240s | 39.97 | $0.00 |
| 100 | 120 | 12000 | 0.393s | 32.71 | $0.00 |
| 250 | 60 | 15000 | 0.551s | 36.76 | $0.00 |

## Interpretation

- These numbers describe the deterministic local research substrate, not an LLM-backed production deployment.
- External model latency/cost is intentionally excluded until a real model adapter is connected and measured.
- The architecture is model-agnostic; the default release uses deterministic extraction plus a sparse linear reward baseline.
- The sandbox exposes three tool primitives: task storage, notes, and reminders.
