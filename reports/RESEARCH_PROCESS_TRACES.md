# Research Process Traces

## Trace A — The result that changed the paper

```text
Native long-horizon utility: PBS appears +0.284 better
↓
Question comparability of confidence scales
↓
Fit the same development-only calibration protocol for every tracker
↓
Held-out calibrated utility: PBS becomes -0.099 vs time-aware-latest
↓
Reject the original “PBS wins utility” interpretation
↓
Add AURC / risk–coverage and freeze a 75-cell protocol grid
↓
Three systems win at least one cell; protocol-pair winner change = 51.6%
↓
Run 2,000 paired seed bootstraps
↓
Winner-change = 0.516 [0.507, 0.538]
↓
Final claim: model selection itself is protocol-sensitive
```

## Trace B — The evaluator became the failure

```text
Trajectory-aware grader looks strong on known perturbations
↓
Freeze the evaluator
↓
Author five attack families not used during grader development
↓
Frozen “robust” grader false-accepts 96%
↓
Inspect failure: it trusts trace structure without causal action evidence
↓
Require live permission at action time + action/payload evidence + post-action full verification
↓
Causal grader false-accepts 0% of the authored held-out set
↓
Keep the old 96% failure in the release as evidence of evaluator overfitting
```

## Trace C — More failure data was not actually more diversity

```text
Trajectory failures → 254 exact-unique correction pairs
↓
Audit semantic templates rather than exact strings
↓
Only four correction templates; 98.4% semantic-template duplication
↓
Reject “post-training-ready diversity” interpretation
↓
Add structured correction records + task-disjoint train/dev/test split
↓
Do not claim post-training improvement until a real model is trained
```
