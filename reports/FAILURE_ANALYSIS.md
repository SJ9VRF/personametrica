# Failure Analysis

Evaluation over 1,000 deterministic proactivity scenarios. This report is diagnostic evidence for the local policy, not a human-behavior claim.

| Slice | N | Accuracy |
|---|---:|---:|
| high stakes irreversible | 34 | 94.1% |
| low confidence | 477 | 92.2% |
| low value | 32 | 71.9% |
| ordinary | 350 | 80.0% |
| urgent | 107 | 84.1% |

## Representative errors

- `low_confidence` predicted **none**, expected `ask`; relevance=0.24, urgency=0.16, confidence=0.40, stakes=0.16, reversibility=0.41.
- `ordinary` predicted **ask**, expected `wait`; relevance=0.90, urgency=0.28, confidence=0.50, stakes=0.39, reversibility=0.12.
- `ordinary` predicted **wait**, expected `none`; relevance=0.16, urgency=0.37, confidence=0.81, stakes=0.39, reversibility=0.96.
- `ordinary` predicted **ask**, expected `wait`; relevance=0.01, urgency=0.55, confidence=0.87, stakes=0.89, reversibility=0.33.
- `ordinary` predicted **ask**, expected `remind, wait`; relevance=0.68, urgency=0.64, confidence=0.55, stakes=0.64, reversibility=0.33.
- `low_confidence` predicted **none**, expected `ask`; relevance=0.02, urgency=0.21, confidence=0.44, stakes=0.91, reversibility=0.53.
- `high_stakes_irreversible` predicted **wait**, expected `ask`; relevance=0.04, urgency=0.13, confidence=0.85, stakes=0.83, reversibility=0.14.
- `low_confidence` predicted **none**, expected `ask`; relevance=0.01, urgency=0.08, confidence=0.07, stakes=0.27, reversibility=0.99.
- `low_value` predicted **wait**, expected `none`; relevance=0.18, urgency=0.04, confidence=0.77, stakes=0.48, reversibility=0.59.
- `ordinary` predicted **ask**, expected `wait`; relevance=0.33, urgency=0.19, confidence=0.97, stakes=0.79, reversibility=0.09.
- `ordinary` predicted **wait**, expected `none`; relevance=0.07, urgency=0.26, confidence=0.81, stakes=0.37, reversibility=0.93.
- `low_confidence` predicted **none**, expected `ask`; relevance=0.23, urgency=0.15, confidence=0.49, stakes=0.36, reversibility=0.63.

These failures are retained rather than hidden because they define the next policy-learning targets.
