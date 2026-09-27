from __future__ import annotations
import argparse, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
LOG=ROOT/'data'/'reproduction_logs'
LOG.mkdir(parents=True,exist_ok=True)

COMMANDS=[
    ([sys.executable,'-m','pytest','-q'], False),
    # Paper-first PersonaMetrica-Bench track. Hyperparameters are selected on dev seeds,
    # then all reported statistics use held-out seeds.
    ([sys.executable,'scripts/tune_belief_state.py'], True),
    ([sys.executable,'scripts/run_belief_benchmark.py'], True),
    ([sys.executable,'scripts/belief_statistics.py'], True),
    ([sys.executable,'scripts/belief_long_horizon_statistics.py'], True),
    ([sys.executable,'scripts/belief_risk_coverage.py'], True),
    ([sys.executable,'scripts/belief_sensitivity.py'], True),
    ([sys.executable,'scripts/export_belief_dataset.py'], True),
    ([sys.executable,'scripts/build_personalbench_x_metadata.py'], False),
    ([sys.executable,'scripts/build_annotation_pack.py'], False),
    ([sys.executable,'scripts/build_paper_figures.py'], False),
    ([sys.executable,'scripts/pbs_component_ablations.py'], True),
    ([sys.executable,'scripts/belief_stress_grid.py'], True),
    ([sys.executable,'scripts/belief_paired_tests.py'], False),
    ([sys.executable,'scripts/calibrated_baseline_eval.py'], True),
    ([sys.executable,'scripts/calibration_protocol_analysis.py'], False),
    ([sys.executable,'scripts/protocol_stability_matrix.py'], True),
    ([sys.executable,'scripts/leaderboard_stability_audit.py'], True),
    ([sys.executable,'scripts/protocol_grid_robustness.py'], False),
    ([sys.executable,'scripts/leaderboard_seed_uncertainty.py'], True),
    ([sys.executable,'scripts/external_horizonbench_smoke.py'], False),
    ([sys.executable,'scripts/benchmark_health_audit.py'], False),
    ([sys.executable,'scripts/validate_protocol_registry.py'], False),
    ([sys.executable,'scripts/freeze_protocol_registry.py'], False),
    ([sys.executable,'scripts/benchmark_integrity_audit.py'], False),
    ([sys.executable,'scripts/build_v31_figures.py'], False),
    ([sys.executable,'scripts/prepare_neurips_2026_submission.py'], False),
    ([sys.executable,'scripts/agent_trajectory_eval.py'], False),
    ([sys.executable,'scripts/build_trace_failure_data.py'], False),
    ([sys.executable,'scripts/reward_hacking_eval.py'], False),
    ([sys.executable,'scripts/grader_reliability_eval.py'], False),
    ([sys.executable,'scripts/heldout_grader_attacks.py'], False),
    ([sys.executable,'scripts/counterfactual_belief_eval.py'], False),
    ([sys.executable,'scripts/build_grader_disagreement_queue.py'], False),
    ([sys.executable,'scripts/audit_trace_failure_data.py'], False),
    ([sys.executable,'scripts/build_trajectory_annotation_pack.py'], False),
    ([sys.executable,'scripts/build_grader_fingerprint.py'], False),
    ([sys.executable,'scripts/build_paper.py'], False),
    # Existing systems substrate and regression suite.
    ([sys.executable,'evals/run_eval.py','--users','100','--turns','60','--seed','7'], True),
    ([sys.executable,'scripts/regression_gate.py'], False),
    ([sys.executable,'data/generate_dataset.py','--users','100','--turns','60'], False),
    ([sys.executable,'experiments/build_preference_data.py'], False),
    ([sys.executable,'scripts/audit_training_data.py'], False),
    ([sys.executable,'scripts/train_reward_baseline.py'], True),
    ([sys.executable,'scripts/reward_generalization_eval.py'], True),
    ([sys.executable,'experiments/run_ablations.py'], True),
    ([sys.executable,'scripts/robustness.py'], False),
    ([sys.executable,'scripts/statistical_analysis.py'], True),
    ([sys.executable,'scripts/failure_analysis.py'], False),
    ([sys.executable,'scripts/scaling_benchmark.py'], True),
    ([sys.executable,'scripts/build_v12_reports.py'], False),
    ([sys.executable,'dashboard/build_dashboard.py'], False),
    ([sys.executable,'scripts/build_summary.py'], False),
    ([sys.executable,'scripts/build_release_summary.py'], False),
    ([sys.executable,'scripts/build_app.py'], False),
    ([sys.executable,'scripts/build_assets.py'], False),
    ([sys.executable,'scripts/humanize_project_page.py'], False),
    ([sys.executable,'scripts/project_page_qa.py'], False),
    ([sys.executable,'scripts/build_demo_video.py'], False),
    ([sys.executable,'scripts/build_anonymous_submission.py'], False),
    ([sys.executable,'scripts/reviewer_demo.py'], False),
    ([sys.executable,'scripts/cold_start_audit.py'], False),
    ([sys.executable,'scripts/hiring_surface_audit.py'], False),
    ([sys.executable,'scripts/submission_format_audit.py'], False),
    ([sys.executable,'scripts/validate_neurips_ed_submission.py'], False),
    ([sys.executable,'scripts/build_manifest.py'], False),
    ([sys.executable,'scripts/release_check.py'], False),
]

parser=argparse.ArgumentParser(description="Reproduce all checked-in research artifacts.")
parser.add_argument('--start',type=int,default=1,help='resume at this 1-indexed pipeline step')
args=parser.parse_args()
if args.start < 1 or args.start > len(COMMANDS):
    raise SystemExit(f'--start must be between 1 and {len(COMMANDS)}')

for i,(cmd,verbose_to_log) in enumerate(COMMANDS,1):
    if i < args.start:
        continue
    print(f"[{i:02d}/{len(COMMANDS):02d}] $ {' '.join(cmd)}", flush=True)
    if verbose_to_log:
        name=Path(cmd[1]).stem if len(cmd)>1 and cmd[1].endswith('.py') else f'step_{i}'
        log_path=LOG/f'{i:02d}_{name}.log'
        with log_path.open('w',encoding='utf-8') as fh:
            subprocess.run(cmd,cwd=ROOT,stdout=fh,stderr=subprocess.STDOUT,check=True)
        print(f"  ↳ full output: {log_path.relative_to(ROOT)}", flush=True)
    else:
        subprocess.run(cmd,cwd=ROOT,check=True)
print('\nReproduction complete.')
