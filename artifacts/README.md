# Raw Research Artifacts

This directory is the evidence layer behind the polished project page. Files are copied from the actual checked-in evaluation outputs; they are not illustrative mock results.

- `experiment_logs/` — per-experiment concise records (generated from the experiment journal)
- `eval_runs/` — raw JSON outputs for calibration, leaderboard, grader, counterfactual, benchmark-health, reward, ablation, and scaling runs
- `failure_examples/` — concrete failure rows and grader attacks
- `plots/` — checked-in figures generated from released results
- `configs/` — frozen protocol/default/regression configs
- `qualitative_cases/` — representative trajectories and demo outputs
- `ablations/` — raw ablation results

The canonical interpretation still lives in the corresponding `reports/` files so raw outputs are not mistaken for broader claims.
