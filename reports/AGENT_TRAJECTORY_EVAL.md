# Agent trajectory evaluation

PersonaMetrica-Bench trajectory extension separates task success from the path used to obtain it. It is a synthetic grader benchmark, not a frontier-model performance result.

## Setup

- Tasks: 80
- Trials: 800
- Tool domains: reminders, notes, tasks
- Perturbations: clean, recoverable_mismatch, unsafe_shortcut, missing_verification, wrong_tool, wrong_action, partial_state, redundant_loop, false_claim, forged_verification

## Grader reliability against scenario gold labels

| Grader | Accuracy | False accept | False reject |
|---|---:|---:|---:|
| end_state_only | 0.682 | 0.443 | 0.000 |
| trajectory_policy | 0.900 | 0.139 | 0.000 |
| composite_agent | 0.900 | 0.139 | 0.000 |
| robust_trajectory | 1.000 | 0.000 | 0.000 |
| causal_trajectory | 1.000 | 0.000 | 0.000 |

## Adversarial false-accept rate

| Grader | FAR on all gold-failing perturbations, including permission, tool/action, verification, partial-state, loop, false-claim, and forged-verification failures |
|---|---:|
| end_state_only | 0.443 |
| trajectory_policy | 0.139 |
| composite_agent | 0.139 |
| robust_trajectory | 0.000 |
| causal_trajectory | 0.000 |

## Interpretation

An end-state-only grader can accept trajectories that reach the requested state by violating permission, skipping required verification, or using an excessively long loop. The trajectory-aware grader makes those intermediate constraints explicit. This result validates the evaluation harness, not the behavior of a frontier model.

## Boundary

- Gold labels are scenario-authored and deterministic.
- No LLM-as-judge claim is made.
- The suite is designed to calibrate future trace graders against explicit assertions and, later, independent human labels.
