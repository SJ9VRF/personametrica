# Evidence Layer — Real Evaluation Tables

These tables are assembled from checked-in run artifacts. Rows with different scopes are labeled explicitly; they are not merged into a single pseudo-score.

## Mechanism ablations

| Variant | Measure | Result | Seeds / N | Scope |
|---|---|---:|---|---|
| Full temporal state vs first-mention memory | Personalization gain | 58.2 pp (95% CI 55.8–60.3) | 10 seeds | controlled synthetic mechanism benchmark |
| Calibrated vs uncalibrated proactivity | Proactivity accuracy gain | 70.9 pp (95% CI 69.1–72.6) | 10 seeds | deterministic generated scenarios |
| Outcome verifier vs no verifier | Failure-detection gain | 100.0 pp | 10 seeds | sandbox verification benchmark |

## Protocol-sensitive personal-agent evaluation

| Comparison | Metric | Result | N / seeds | Interpretation |
|---|---|---:|---|---|
| PBS vs time-aware, native confidence | long-horizon utility delta | +0.284 | seeds 30–39 | diagnostic only; confidence scales unmatched |
| PBS vs time-aware, shared dev calibration | long-horizon utility delta | -0.099 | dev 1–3; test 30–39 | ranking reverses after equal calibration |
| PBS vs time-aware | AURC ↓ | 0.0107 vs 0.0208 | checked-in benchmark | threshold-free confidence ordering |
| Six-system leaderboard | winner change between protocol pairs | 51.6% | 75 protocol cells | leaderboard is protocol-sensitive |
| Six-system leaderboard | mean / min Kendall τ | 0.699 / 0.20 | all protocol pairs | complete ranking can move materially |
| Seed bootstrap | winner-change probability | 0.516 [0.507, 0.538] | 2,000 resamples, 10 long-horizon seeds | synthetic-seed uncertainty only |

## Evaluator and counterfactual robustness

| Variant | Success / failure metric | Result | N | Notes |
|---|---|---:|---:|---|
| End-state-only grader | false accept ↓ | 100.0% | 75 held-out attacks | final state alone misses invalid trajectories |
| Frozen robust trajectory grader | false accept ↓ | 96.0% | 75 held-out attacks | evaluator overfit exposed |
| Causal trajectory grader | false accept ↓ | 0.0% | 75 held-out attacks | authored held-out set only |
| PBS | nuisance invariance | 98.0% | 540 paired interventions | ~2% contamination retained as failure |
| PBS | explicit-update sensitivity | 99.3% | 540 paired interventions | responds to current explicit preference |

## Negative-control / data-quality results

| Experiment | Metric | Result | Why it matters |
|---|---|---:|---|
| Lexical reward baseline | ordinary held-out accuracy | 100.0% | looks deceptively strong |
| Lexical reward baseline | lexically matched contrast accuracy | 50.0% | exposes semantic shortcut failure |
| Local scaling | largest checked run | 15,000 interactions | deterministic local substrate, not frontier serving |
| Local scaling | external API cost | $0.00 | default release makes no external inference calls |

## Cost / latency boundary

The release reports measured local deterministic runtime only. It does **not** report frontier-model latency, token cost, or model-size scaling until a model-backed adapter run is actually executed.
