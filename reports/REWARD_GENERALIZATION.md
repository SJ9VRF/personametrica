# Reward Generalization & Leakage Audit

v1.5 adds stronger tests specifically because the standard synthetic held-out split can share canonical answer wording across train and test. These results are intentionally reported even when they expose failure.

## Standard split

- Test accuracy: **1.000** (n=71)
- Bidirectional Brier: **0.072**
- Bidirectional ECE: **0.260**

## Leakage audit

- Exact response-pair overlap (train ↔ test): **4**
- Test rows whose response pair was seen in train: **98.6%**

## Leave-one-family-out

- Macro accuracy: **1.000**
- Weighted accuracy: **1.000**

- `high_stakes_autonomy`: 1.000 (n=43)
- `low_value_proactivity`: 1.000 (n=18)
- `privacy_control`: 1.000 (n=8)
- `reversible_assistance`: 1.000 (n=283)
- `temporal_memory`: 1.000 (n=16)
- `uncertainty_calibration`: 1.000 (n=356)

## Unseen paraphrase stress set

- Overall accuracy: **0.667** (n=12)

- `high_stakes_autonomy`: 0.500 (n=2)
- `low_value_proactivity`: 0.500 (n=2)
- `privacy_control`: 0.500 (n=2)
- `reversible_assistance`: 1.000 (n=2)
- `temporal_memory`: 0.500 (n=2)
- `uncertainty_calibration`: 1.000 (n=2)

## Interpretation

The standard split is useful for verifying the end-to-end learning path, but it is not a strong generalization claim when canonical response wording overlaps across splits. Leave-one-family-out and unseen-paraphrase evaluations are therefore the more demanding evidence for this lexical baseline. Any weak scores are retained as explicit evidence of the boundary of the baseline rather than tuned away.
