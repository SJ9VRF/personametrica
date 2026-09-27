# Counterfactual belief-state checks

Paired interventions test whether a tracker is invariant to irrelevant evidence yet sensitive to a genuinely relevant current update. This is a controlled causal diagnostic over structured evidence, not a natural-language or human-validity result.

| Tracker | Pairs | Nuisance invariance | Weak-conflict invariance | Explicit-update sensitivity |
|---|---:|---:|---:|---:|
| time-aware-latest | 540 | 100.0% | 10.0% | 100.0% |
| personal-belief-state | 540 | 98.0% | 64.4% | 99.3% |

The three rates intentionally measure different desiderata. A system that is invariant to everything is not adaptive; a system that flips on every weak cue is not robust. These checks therefore complement, rather than replace, state accuracy and calibration.
