# Robustness across random seeds

Evaluated 5 seeds × 100 synthetic users × 60 turns. These are controlled synthetic results, not human or frontier-model claims.

| Effect | Mean difference |
|---|---:|
| temporal update personalization gain | 0.568 |
| temporal update stale memory reduction | 0.568 |
| contradiction resolution reduction | 0.784 |
| calibrated proactivity accuracy gain | 0.709 |
| verification failure detection gain | 1.000 |

## Full-system stability

| Metric | Mean | Std | Min | Max |
|---|---:|---:|---:|---:|
| personalization_accuracy | 1.000 | 0.000 | 1.000 | 1.000 |
| stale_memory_rate | 0.000 | 0.000 | 0.000 | 0.000 |
| contradiction_rate | 0.000 | 0.000 | 0.000 | 0.000 |
| goal_capture_rate | 1.000 | 0.000 | 1.000 | 1.000 |
| proactive_decision_accuracy | 0.875 | 0.017 | 0.860 | 0.900 |
| autonomy_violation_rate | 0.000 | 0.000 | 0.000 | 0.000 |
| high_stakes_confirmation_rate | 0.975 | 0.034 | 0.933 | 1.000 |
| low_confidence_clarification_rate | 0.949 | 0.017 | 0.925 | 0.967 |
| failure_detection_rate | 1.000 | 0.000 | 1.000 | 1.000 |
| memory_confidence_brier | 0.000 | 0.000 | 0.000 | 0.000 |
