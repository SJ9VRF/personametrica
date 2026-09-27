from __future__ import annotations
import shutil, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'submission'
out.mkdir(exist_ok=True)
readme='''# PersonaMetrica-Bench Anonymous Submission Bundle\n\nThis bundle contains the anonymous paper and the minimum reproducibility artifacts for review.\n\nIncluded: PDF/LaTeX/bibliography/figures, PersonaMetrica-Bench dataset + metadata, belief benchmark implementation, evaluation scripts, and selected reports.\n\nExcluded: author metadata and portfolio-facing pages. Human-participant and frontier-model results are not claimed because they have not been executed in this environment.\n'''
(out/'README.md').write_text(readme,encoding='utf-8')
paths=[
 'paper/personalbench_x_anonymous.pdf','paper/main.tex','paper/main_neurips_2026.tex','paper/APPENDIX_CHECKLIST.md','paper/NEURIPS_2026_TEMPLATE_STATUS.md','paper/references.bib',
 'paper/figures/accuracy_vs_utility.png','paper/figures/risk_coverage.png','paper/figures/distribution_shifts.png','paper/figures/pbs_component_ablations.png','paper/figures/belief_stress_grid.png','paper/figures/protocol_stability_matrix.svg','paper/figures/protocol_stability_matrix.png',
 'data/personalbench_x.jsonl','data/PERSONALBENCH_X_CARD.md','data/personalbench_x_croissant.json',
 'personalagi/user_model/probabilistic_belief.py','personalbench/belief_benchmark.py',
 'scripts/run_belief_benchmark.py','scripts/belief_statistics.py','scripts/belief_long_horizon_statistics.py','scripts/belief_risk_coverage.py','scripts/belief_sensitivity.py','scripts/tune_belief_state.py','scripts/pbs_component_ablations.py','scripts/belief_stress_grid.py','scripts/belief_paired_tests.py','scripts/calibrated_baseline_eval.py','scripts/calibration_protocol_analysis.py','scripts/protocol_stability_matrix.py','scripts/leaderboard_stability_audit.py','scripts/leaderboard_seed_uncertainty.py','scripts/protocol_grid_robustness.py','scripts/external_horizonbench_smoke.py','scripts/benchmark_health_audit.py','scripts/validate_protocol_registry.py','scripts/freeze_protocol_registry.py','scripts/benchmark_integrity_audit.py',
 'reports/BELIEF_STATE_BENCHMARK.md','reports/BELIEF_STATE_STATISTICS.md','reports/BELIEF_LONG_HORIZON.md','reports/BELIEF_RISK_COVERAGE.md','reports/BELIEF_SENSITIVITY.md','reports/CALIBRATED_BASELINES.md','reports/CALIBRATION_PROTOCOL_ANALYSIS.md','reports/PROTOCOL_STABILITY_MATRIX.md','reports/LEADERBOARD_STABILITY_AUDIT.md','reports/LEADERBOARD_SEED_UNCERTAINTY.md','reports/PROTOCOL_GRID_ROBUSTNESS.md','reports/HORIZONBENCH_ADAPTER_SMOKE.md','reports/BENCHMARK_HEALTH_AUDIT.md','reports/RELATED_WORK_POSITIONING.md','reports/PBS_COMPONENT_ABLATIONS.md','reports/BELIEF_STRESS_GRID.md','reports/BELIEF_PAIRED_TESTS.md','reports/BENCHMARK_INTEGRITY_AUDIT.md','reports/COMPUTE_RESOURCES.md','annotation/README.md','annotation/index.html','annotation/tasks.json','evals/external_model_eval.py',
 'docs/NEURIPS_READINESS.md','docs/AGENT_EVAL_SPEC.md','docs/GRADER_CALIBRATION_PROTOCOL.md','docs/FRONTIER_EVAL_CHECKLIST.md',
 'personalbench/agent_evals/__init__.py','personalbench/agent_evals/models.py','personalbench/agent_evals/graders.py','personalbench/agent_evals/suite.py','personalbench/agent_evals/reliability.py','personalbench/agent_evals/heldout_attacks.py',
 'scripts/agent_trajectory_eval.py','scripts/heldout_grader_attacks.py','scripts/counterfactual_belief_eval.py','scripts/build_trace_failure_data.py','scripts/reward_hacking_eval.py','scripts/grader_reliability_eval.py','scripts/build_grader_disagreement_queue.py','scripts/audit_trace_failure_data.py','scripts/build_grader_fingerprint.py',
 'reports/NOVELTY_SOTA_AUDIT_ANON.md','reports/AGENT_TRAJECTORY_EVAL.md','reports/HELDOUT_GRADER_ATTACKS.md','reports/COUNTERFACTUAL_BELIEF_EVAL.md','reports/TRACE_FAILURE_DATA.md','reports/TRACE_FAILURE_DATA_AUDIT.md','reports/REWARD_HACKING_EVAL.md','reports/GRADER_RELIABILITY.md','reports/GRADER_DISAGREEMENT_QUEUE.md','reports/GRADER_FINGERPRINT.md','reports/OPENAI_ANTHROPIC_RESEARCH_READINESS.md',
 'configs/protocol_registry.json','data/protocol_registry_fingerprint.json','data/protocol_stability_matrix.json','data/leaderboard_stability_audit.json','data/leaderboard_seed_uncertainty.json','data/protocol_grid_robustness.json','data/horizonbench_adapter_smoke.json','external_benchmarks/horizonbench_adapter.py','external_benchmarks/HORIZONBENCH_ADAPTER.md','external_benchmarks/fixtures/horizonbench_results_model_a.jsonl','external_benchmarks/fixtures/horizonbench_results_model_b.jsonl','data/benchmark_health_audit.json','data/agent_trajectory_eval.json','data/heldout_grader_attacks.json','data/counterfactual_belief_eval.json','data/agent_trajectories.jsonl','data/trajectory_failure_pairs.jsonl','data/trajectory_corrections.jsonl','data/trajectory_failure_splits.json','data/trajectory_failure_data_audit.json','data/reward_hacking_eval.json','data/grader_reliability.json','data/grader_disagreement_queue.jsonl','data/grader_fingerprint.json',
 'annotation/trajectory_grading/README.md','annotation/trajectory_grading/index.html','annotation/trajectory_grading/tasks.json'
]
zip_path=out/'personalbench_x_anonymous_bundle.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    z.write(out/'README.md','README.md')
    for rel in paths:
        p=ROOT/rel
        if not p.exists(): raise SystemExit(f'Missing submission artifact: {rel}')
        z.write(p,rel)
canonical=out/'personametrica_anonymous_bundle.zip'
shutil.copy2(zip_path,canonical)
print(f'Built {canonical.relative_to(ROOT)} (plus legacy alias) with {len(paths)+1} files')
