# Reproducible Result Summary

Generated from `data/eval_results.json`. Benchmark: **100 synthetic users × 60 turns**, plus **200 proactivity scenarios**. These are controlled synthetic results, not human or frontier-model performance claims.

## Main findings

- **Temporal updating:** full system personalization accuracy 100.0%, stale-memory rate 0.0%; disabling temporal update yields 37.1% accuracy and 62.9% stale memory.
- **Conflict resolution:** full system contradiction rate 0.0%; disabling conflict resolution yields 82.0%.
- **Proactivity calibration:** calibrated policy decision accuracy 86.5% with autonomy-violation rate 0.0%; uncalibrated policy yields 17.0% and 5.9%.
- **Confidence tracking:** memory-confidence Brier error 0.000; disabling confidence tracking yields 0.070. Lower is better.
- **Outcome verification:** failure detection 100.0%; disabling verification yields 0.0%.

## Interpretation boundary

The benchmark intentionally tests mechanisms the repository implements. It demonstrates that the mechanisms behave as specified under controlled conditions. It does **not** establish generalization to natural human behavior, production traffic, or frontier language models. The human-study protocol in `reports/HUMAN_STUDY_PROTOCOL.md` defines the next validation layer.
