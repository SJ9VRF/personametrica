from __future__ import annotations
import json, math, os, re, subprocess, sys, tomllib
from pathlib import Path
required=['scripts/humanize_project_page.py','project/base_template.html','docs/HIRING_MANAGER_README.md','README.md','LICENSE','CITATION.cff','paper/PAPER.md','reports/RESULTS.md','reports/ROBUSTNESS.md','reports/STATISTICAL_ANALYSIS.md','reports/FAILURE_ANALYSIS.md','reports/ADVERSARIAL_EVAL.md','reports/PRIVACY_USER_CONTROL.md','reports/SYSTEM_DESIGN.md','reports/DATASET_CARD.md','reports/MODEL_SYSTEM_CARD.md','reports/TRAINING_DATA_AUDIT.md','reports/LEARNED_REWARD_BASELINE.md','reports/REWARD_GENERALIZATION.md','docs/architecture.svg','docs/results.svg','docs/EVIDENCE_LEDGER.md','docs/REVIEWER_GUIDE.md','docs/INTERVIEW_WALKTHROUGH.md','docs/EXPERIMENT_INDEX.md','docs/PORTFOLIO_ONE_PAGER.md','docs/BLOG_POST.md','docs/BENCHMARK_SPEC.md','docs/THREAT_MODEL.md','configs/regression_gates.json','examples/replay_model_outputs.py','CHANGELOG.md','data/eval_results.json','data/robustness_results.json','data/statistical_analysis.json','data/failure_analysis.json','data/training_data_audit.json','data/reward_baseline_results.json','data/reward_generalization_results.json','data/release_summary.json','docs/FINAL_RELEASE_SUMMARY.md','app/index.html','dashboard/index.html','project/index.html','project/assets/trajectory.json','project/assets/personal_agi_os_demo.mp4','project/assets/video_poster.png','project/site.webmanifest','project/robots.txt','project/assets/favicon.svg','project/assets/social_card.svg','reports/SCALING.md','data/scaling_results.json','reports/PROJECT_PAGE_QA.md','data/project_page_qa.json','docs/PROJECT_PAGE_DEPLOYMENT.md','docs/PROJECT_PAGE_SPEC.md','docs/PROJECT_PAGE_COMPLIANCE.md','docs/GITHUB_RELEASE.md',
'paper/personalbench_x_anonymous.pdf','paper/main.tex','paper/references.bib','paper/SUBMISSION_CHECKLIST.md','paper/AUTHOR_METADATA.md',
'paper/figures/accuracy_vs_utility.png','paper/figures/risk_coverage.png','paper/figures/distribution_shifts.png',
'reports/BELIEF_STATE_BENCHMARK.md','reports/BELIEF_STATE_STATISTICS.md','reports/BELIEF_LONG_HORIZON.md','reports/BELIEF_RISK_COVERAGE.md','reports/BELIEF_SENSITIVITY.md','reports/BELIEF_TUNING.md','reports/RELATED_WORK_POSITIONING.md',
'docs/NEURIPS_READINESS.md','data/belief_benchmark_results.json','data/belief_statistics.json','data/belief_long_horizon_statistics.json','data/belief_risk_coverage.json','data/belief_sensitivity.json','data/belief_tuning.json',
'data/personalbench_x.jsonl','data/PERSONALBENCH_X_CARD.md','data/personalbench_x_croissant.json',
'annotation/index.html','annotation/tasks.json','annotation/README.md','evals/external_model_eval.py','external_benchmarks/README.md','experiments/MODEL_BACKED_PLAN.md',
'submission/personalbench_x_anonymous_bundle.zip','paper/APPENDIX_CHECKLIST.md','paper/main_neurips_2026.tex','paper/NEURIPS_2026_TEMPLATE_STATUS.md','paper/OFFICIAL_STYLE_REQUIRED.txt','reports/PBS_COMPONENT_ABLATIONS.md','reports/BELIEF_STRESS_GRID.md','reports/BELIEF_PAIRED_TESTS.md','reports/BENCHMARK_INTEGRITY_AUDIT.md','reports/COMPUTE_RESOURCES.md','reports/NEURIPS_ED_SUBMISSION_READINESS.md','data/pbs_component_ablations.json','data/belief_stress_grid.json','data/belief_paired_tests.json','data/benchmark_integrity_audit.json','data/neurips_ed_submission_readiness.json','paper/figures/pbs_component_ablations.png','paper/figures/belief_stress_grid.png','reports/CALIBRATED_BASELINES.md','reports/CALIBRATION_PROTOCOL_ANALYSIS.md','data/calibrated_baseline_results.json','data/calibration_protocol_analysis.json','reports/SUBMISSION_FORMAT_AUDIT.md','data/submission_format_audit.json',
'reports/AGENT_TRAJECTORY_EVAL.md','data/agent_trajectory_eval.json','docs/AGENT_EVAL_SPEC.md','reports/TRACE_FAILURE_DATA.md','data/agent_trajectories.jsonl','data/trajectory_failure_pairs.jsonl','data/trajectory_corrections.jsonl','data/trajectory_failure_splits.json','reports/TRACE_FAILURE_DATA_AUDIT.md','data/trajectory_failure_data_audit.json','reports/REWARD_HACKING_EVAL.md','data/reward_hacking_eval.json','reports/GRADER_RELIABILITY.md','data/grader_reliability.json','reports/GRADER_DISAGREEMENT_QUEUE.md','data/grader_disagreement_queue.jsonl','docs/GRADER_CALIBRATION_PROTOCOL.md','docs/FRONTIER_EVAL_CHECKLIST.md','annotation/trajectory_grading/index.html','annotation/trajectory_grading/tasks.json','annotation/trajectory_grading/README.md','reports/GRADER_FINGERPRINT.md','data/grader_fingerprint.json','reports/OPENAI_ANTHROPIC_RESEARCH_READINESS.md','reports/HELDOUT_GRADER_ATTACKS.md','data/heldout_grader_attacks.json','reports/COUNTERFACTUAL_BELIEF_EVAL.md','data/counterfactual_belief_eval.json','reports/NOVELTY_SOTA_AUDIT.md','reports/NOVELTY_SOTA_AUDIT_ANON.md','reports/PROTOCOL_STABILITY_MATRIX.md','data/protocol_stability_matrix.json','reports/LEADERBOARD_STABILITY_AUDIT.md','data/leaderboard_stability_audit.json','reports/LEADERBOARD_SEED_UNCERTAINTY.md','data/leaderboard_seed_uncertainty.json','reports/PROTOCOL_GRID_ROBUSTNESS.md','data/protocol_grid_robustness.json','reports/HORIZONBENCH_ADAPTER_SMOKE.md','data/horizonbench_adapter_smoke.json','external_benchmarks/horizonbench_adapter.py','external_benchmarks/HORIZONBENCH_ADAPTER.md','external_benchmarks/fixtures/horizonbench_results_model_a.jsonl','external_benchmarks/fixtures/horizonbench_results_model_b.jsonl','reports/BENCHMARK_HEALTH_AUDIT.md','data/benchmark_health_audit.json','configs/protocol_registry.json','data/protocol_registry_fingerprint.json','paper/figures/protocol_stability_matrix.svg','paper/figures/protocol_stability_matrix.png','paper/personametrica_anonymous.pdf','data/personametrica_bench.jsonl','data/PERSONAMETRICA_BENCH_CARD.md','data/personametrica_bench_croissant.json','submission/personametrica_anonymous_bundle.zip','scripts/reviewer_demo.py','scripts/cold_start_audit.py','scripts/hiring_surface_audit.py','reports/REVIEWER_DEMO.md','data/reviewer_demo.json','reports/COLD_START_AUDIT.md','data/cold_start_audit.json','reports/HIRING_SURFACE_AUDIT.md','data/hiring_surface_audit.json','docs/FRONTIER_RESEARCH_BRIEF.md','docs/HIRING_PACKET.md']
missing=[p for p in required if not Path(p).exists()]
if missing: raise SystemExit('Missing required release artifacts: '+', '.join(missing))

# Single-source-of-truth version consistency.
version=tomllib.loads(Path('pyproject.toml').read_text(encoding='utf-8'))['project']['version']

project_meta=tomllib.loads(Path('pyproject.toml').read_text(encoding='utf-8'))['project']
authors=[a.get('name') for a in project_meta.get('authors',[])]
if authors != ['Aura Yavary']:
    raise SystemExit(f'Public authorship metadata mismatch: {authors}')
citation=Path('CITATION.cff').read_text(encoding='utf-8')
m=re.search(r'^version:\s*([^\s]+)\s*$',citation,re.M)
if not m or m.group(1)!=version: raise SystemExit(f'CITATION version mismatch: expected {version}')
manifest=json.loads(Path('MANIFEST.json').read_text(encoding='utf-8'))
if manifest.get('version')!=version: raise SystemExit(f'Manifest version mismatch: {manifest.get("version")} != {version}')
if f'v{version}' not in Path('CHANGELOG.md').read_text(encoding='utf-8'):
    raise SystemExit(f'CHANGELOG missing v{version}')
if not manifest.get('files'): raise SystemExit('Manifest empty')

# Agent-evaluation hardening artifacts.
agent_eval=json.loads(Path('data/agent_trajectory_eval.json').read_text(encoding='utf-8'))
agm=agent_eval['grader_metrics']
end_far=agm['end_state_only']['false_accept_rate']; robust_far=agm['robust_trajectory']['false_accept_rate']
if end_far < .35 or (end_far-robust_far) < .35:
    raise SystemExit(f'Agent trajectory suite no longer exposes a material end-state vs robust false-accept gap: {end_far:.3f} vs {robust_far:.3f}')
if robust_far != 0.0:
    raise SystemExit('Robust trajectory grader false-accept regression')
trace_pairs=sum(1 for _ in Path('data/trajectory_failure_pairs.jsonl').open(encoding='utf-8'))
if trace_pairs < 200:
    raise SystemExit(f'Too few failure-derived trajectory correction pairs: {trace_pairs}')
reliability=json.loads(Path('data/grader_reliability.json').read_text())
mm=reliability['mutation_metrics']
for key in ('benign_invariance_rate','forged_flag_invariance_rate','redacted_evidence_abstention_rate','late_confirmation_detection_rate','tool_loop_detection_rate'):
    if mm.get(key) != 1.0: raise SystemExit(f'Grader reliability regression: {key}={mm.get(key)}')
audit=json.loads(Path('data/trajectory_failure_data_audit.json').read_text())
if any(audit['task_overlap'].values()): raise SystemExit('Trajectory failure-data splits are not task-disjoint')
if audit['semantic_template_duplication_rate'] < .90: raise SystemExit('Expected templated-data diagnostic changed; re-review training-data claim')
fp=json.loads(Path('data/grader_fingerprint.json').read_text())
if len(fp.get('grader_bundle_sha256','')) != 64: raise SystemExit('Missing/invalid grader fingerprint')


held=json.loads(Path('data/heldout_grader_attacks.json').read_text())
if held['metrics']['causal_trajectory']['false_accept_rate'] != 0.0:
    raise SystemExit('Causal grader held-out false-accept regression')
if held['metrics']['robust_trajectory']['false_accept_rate'] < .75:
    raise SystemExit('Held-out grader attacks no longer expose the frozen robust-grader gap; re-review benchmark')
cf=json.loads(Path('data/counterfactual_belief_eval.json').read_text())
pbs_cf=cf['results']['personal-belief-state']
if pbs_cf['explicit_update_sensitivity'] < .95 or pbs_cf['nuisance_invariance'] < .95:
    raise SystemExit('PBS counterfactual behavior regression')


novelty=Path('reports/NOVELTY_SOTA_AUDIT.md').read_text(encoding='utf-8')
for phrase in ('PerMemBench','PersonaLens','HorizonBench','BeliefShift','PERMA','π-Bench','BLINDSPOT','STABLEVAL','not an overall SOTA claim'):
    if phrase not in novelty:
        raise SystemExit(f'Novelty/SOTA audit missing required positioning: {phrase}')
if 'Aura Yavary' not in Path('README.md').read_text(encoding='utf-8') or 'family-names: "Yavary"' not in citation or 'given-names: "Aura"' not in citation:
    raise SystemExit('Public Aura Yavary authorship missing')

# Protocol-stability and release-level protocol-lock integrity.
prot=json.loads(Path('data/protocol_stability_matrix.json').read_text())
ps=prot['summary']
if prot['protocol_grid']['cells'] != 75:
    raise SystemExit('Protocol Stability Matrix no longer has 75 frozen cells')
if ps['pbs_wins'] == 0 or ps['time_aware_wins'] == 0:
    raise SystemExit('Protocol sweep no longer demonstrates protocol-dependent system selection')
if ps['pairwise_protocol_rank_reversal_rate'] < .30:
    raise SystemExit('Protocol rank-reversal diagnostic weakened materially; re-review central claim')
reg=Path('configs/protocol_registry.json').read_bytes()
regfp=json.loads(Path('data/protocol_registry_fingerprint.json').read_text())
import hashlib
if hashlib.sha256(reg).hexdigest() != regfp.get('sha256'):
    raise SystemExit('Protocol registry fingerprint mismatch; refreeze protocol registry')
if regfp.get('status') != 'frozen-release-protocol':
    raise SystemExit('Protocol registry is not marked frozen-release-protocol')

# Full-leaderboard stability and benchmark-health release gates.
leader=json.loads(Path('data/leaderboard_stability_audit.json').read_text())
ls=leader['summary']
if leader.get('protocol_cells') != 75:
    raise SystemExit('Full leaderboard audit no longer has 75 protocol cells')
if ls.get('winner_change_probability',0) < .40 or ls.get('mean_pairwise_kendall_tau',1) > .90:
    raise SystemExit('Full leaderboard audit no longer demonstrates material protocol sensitivity')
if ls.get('minimum_pairwise_kendall_tau',1) > .50:
    raise SystemExit('Worst-case complete-ranking disagreement weakened materially; re-review central claim')
if sum(1 for v in ls.get('winner_counts',{}).values() if v>0) < 3:
    raise SystemExit('Expected at least three methods to win a protocol cell in the checked-in audit')
health=json.loads(Path('data/benchmark_health_audit.json').read_text())
if not health.get('all_pass') or not all(health.get('checks',{}).values()):
    raise SystemExit('Benchmark health audit failed')
if health['counts'].get('identity_overlap') != 0 or health['counts'].get('full_stream_overlap') != 0 or health['counts'].get('standard_duplicate_full_streams') != 0:
    raise SystemExit('Benchmark split/history leakage regression')
seedu=json.loads(Path('data/leaderboard_seed_uncertainty.json').read_text())
if seedu.get('bootstrap_replicates',0) < 2000 or seedu.get('diagnostic_users_per_seed') != 10:
    raise SystemExit('Seed-uncertainty diagnostic configuration regression')
if seedu['bootstrap_95_ci']['winner_change_probability'][0] <= .40 or seedu['bootstrap_claim_support']['p_winner_change_gt_0_40'] < .99:
    raise SystemExit('Seed-bootstrap support for protocol sensitivity weakened materially')
grid=json.loads(Path('data/protocol_grid_robustness.json').read_text())
gr=grid['robustness_summary']
if gr.get('perturbations') != 13 or gr.get('perturbations_with_multiple_winners') != 13 or gr.get('min_winner_change_probability',0) < .30:
    raise SystemExit('Protocol-grid robustness regression')
hb=json.loads(Path('data/horizonbench_adapter_smoke.json').read_text())
if hb.get('status') != 'schema-smoke-test-only' or not hb.get('fixture_is_synthetic'):
    raise SystemExit('External HorizonBench adapter claim boundary regression')

# Paper-first artifact integrity.
paper_md=Path('paper/PAPER.md').read_text(encoding='utf-8')
if 'Aura Yavary' in paper_md:
    raise SystemExit('Anonymous paper contains author name')
for key in ('PersonaMetrica','PersonaMetrica-Bench','risk–coverage','time-aware-latest','75 protocol cells','Kendall'):
    if key not in paper_md:
        raise SystemExit(f'Paper missing expected research element: {key}')
if 'fixed-threshold decision utility is not protocol-invariant' not in paper_md:
    raise SystemExit('Paper missing calibrated-utility protocol finding')
cal=json.loads(Path('data/calibration_protocol_analysis.json').read_text())
if not cal.get('ranking_flip') or not (cal['raw_long_horizon_utility_gain_pbs_vs_time_aware']>0 and cal['dev_calibrated_long_horizon_utility_gain_pbs_vs_time_aware']<0):
    raise SystemExit('Calibration protocol analysis no longer exhibits the checked-in ranking flip')
fmt=json.loads(Path('data/submission_format_audit.json').read_text())
if not fmt.get('generic_draft_content_within_9_pages') or fmt.get('paper_identity_leaks') or fmt.get('bundle_identity_leaks'):
    raise SystemExit('Submission format/anonymity audit failed')
try:
    belief=json.loads(Path('data/belief_benchmark_results.json').read_text(encoding='utf-8'))
    std=belief['regimes']['standard'] if 'regimes' in belief else belief['standard']
except Exception as exc:
    raise SystemExit(f'Invalid PersonaMetrica-Bench benchmark artifact: {exc}')
meta=json.loads(Path('data/personalbench_x_croissant.json').read_text(encoding='utf-8'))
if meta.get('version')!=version:
    raise SystemExit(f'PersonaMetrica-Bench metadata version mismatch: {meta.get("version")} != {version}')
if Path('paper/personalbench_x_anonymous.pdf').stat().st_size < 10000:
    raise SystemExit('Anonymous paper PDF appears unexpectedly small')
if '27,133' not in paper_md:
    raise SystemExit('Paper standard observation count is stale')
checklist=Path('paper/APPENDIX_CHECKLIST.md').read_text(encoding='utf-8')
if not all(f'{i}.' in checklist for i in range(1,16)):
    raise SystemExit('NeurIPS checklist is incomplete')
integrity=json.loads(Path('data/benchmark_integrity_audit.json').read_text())
if integrity.get('observations') != 27133 or integrity.get('queries') != 13500 or not integrity.get('deterministic_replay'):
    raise SystemExit('Benchmark integrity audit mismatch')

# Reviewer-trust gates added in v4.0.
reviewer=json.loads(Path('data/reviewer_demo.json').read_text())
if reviewer.get('status')!='PASS' or not all(reviewer.get('checks',{}).values()):
    raise SystemExit('Reviewer demo evidence gate failed')
cold=json.loads(Path('data/cold_start_audit.json').read_text())
if cold.get('status')!='PASS' or not all(cold.get('checks',{}).values()):
    raise SystemExit('Cold-start execution audit failed')
hiring=json.loads(Path('data/hiring_surface_audit.json').read_text())
if hiring.get('status')!='PASS' or not all(hiring.get('checks',{}).values()):
    raise SystemExit('Hiring-surface audit failed')
subprocess.run([sys.executable,'scripts/reviewer_demo.py'],check=True,stdout=subprocess.DEVNULL)
subprocess.run([sys.executable,'scripts/hiring_surface_audit.py'],check=True,stdout=subprocess.DEVNULL)

subprocess.run([sys.executable,'-m','pytest','-q'],check=True)
subprocess.run([sys.executable,'scripts/regression_gate.py'],check=True)
# The full reproduction pipeline executes the expensive reward-generalization audit.
# Release validation checks the resulting artifact by default to avoid recomputing the
# same multi-split training workload a second time. Set FULL_RELEASE_RECHECK=1 to rerun it.
reward_path=Path('data/reward_generalization_results.json')
try:
    reward=json.loads(reward_path.read_text(encoding='utf-8'))
    para=reward['unseen_paraphrase_set']['overall']['accuracy']
    ece=reward['standard_split']['metrics']['calibration_test_bidirectional']['ece']
    if not (math.isfinite(float(para)) and 0.0 <= float(para) <= 1.0 and math.isfinite(float(ece)) and 0.0 <= float(ece) <= 1.0):
        raise ValueError('reward metrics out of range')
except Exception as exc:
    raise SystemExit(f'Invalid reward-generalization artifact: {exc}')
if os.environ.get('FULL_RELEASE_RECHECK')=='1':
    subprocess.run([sys.executable,'scripts/reward_generalization_eval.py'],stdout=subprocess.DEVNULL,check=True)
subprocess.run([sys.executable,'scripts/project_page_qa.py'],check=True)
print(f"Release check passed: v{version}; {len(required)} required artifacts, {len(manifest['files'])} manifested files.")
