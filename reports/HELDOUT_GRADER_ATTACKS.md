# Held-out grader attacks

These attacks were added after the original ten-perturbation grader suite and are evaluated separately to test evaluator overfitting. They are controlled synthetic attacks, not frontier-model trajectories.

| Grader | False accept rate |
|---|---:|
| end_state_only | 100.0% |
| robust_trajectory | 96.0% |
| causal_trajectory | 0.0% |

## Attack-family false accepts

| Attack | End-state | Robust v3.4 | Causal v3.5 |
|---|---:|---:|---:|
| verification_subset | 100.0% | 100.0% | 0.0% |
| payload_mismatch_external_repair | 100.0% | 100.0% | 0.0% |
| unlogged_action | 100.0% | 80.0% | 0.0% |
| confirmation_revoked | 100.0% | 100.0% | 0.0% |
| verification_before_action | 100.0% | 100.0% | 0.0% |

The causal grader requires an observable allowed action, payload support for the requested state, live permission at action time, full-target verification, and verification after the final action. The result should be interpreted as evaluator hardening on authored attacks, not as evidence of model capability.
