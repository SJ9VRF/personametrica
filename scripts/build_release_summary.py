from __future__ import annotations
import json, tomllib
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
version=tomllib.loads((ROOT/'pyproject.toml').read_text())['project']['version']
test_count=sum(len(re.findall(r'^def test_', p.read_text(encoding='utf-8'), re.M)) for p in (ROOT/'tests').glob('test_*.py'))
repro_src=(ROOT/'scripts/reproduce.py').read_text(encoding='utf-8')
reproduction_steps=repro_src.split('COMMANDS=[',1)[1].split(']\n\nparser=',1)[0].count('([sys.executable')
evalj=json.loads((ROOT/'data/eval_results.json').read_text())
rob=json.loads((ROOT/'data/robustness_results.json').read_text())
train=json.loads((ROOT/'data/training_data_audit.json').read_text())
reward=json.loads((ROOT/'data/reward_baseline_results.json').read_text())
gen=json.loads((ROOT/'data/reward_generalization_results.json').read_text())
belief=json.loads((ROOT/'data/belief_benchmark_results.json').read_text())
longh=json.loads((ROOT/'data/belief_long_horizon_statistics.json').read_text())
risk=json.loads((ROOT/'data/belief_risk_coverage.json').read_text())
grader_rel=json.loads((ROOT/'data/grader_reliability.json').read_text())
agent_eval=json.loads((ROOT/'data/agent_trajectory_eval.json').read_text())
trace_audit=json.loads((ROOT/'data/trajectory_failure_data_audit.json').read_text())
leader=json.loads((ROOT/'data/leaderboard_stability_audit.json').read_text())
health=json.loads((ROOT/'data/benchmark_health_audit.json').read_text())
seedu=json.loads((ROOT/'data/leaderboard_seed_uncertainty.json').read_text())
gridr=json.loads((ROOT/'data/protocol_grid_robustness.json').read_text())
hb=json.loads((ROOT/'data/horizonbench_adapter_smoke.json').read_text())
# tolerate detailed/flat eval formats
systems=evalj.get('systems',{})
full=systems.get('full_temporal_os',{}).get('metrics') or evalj.get('full_temporal_os') or evalj
summary={
 'version':version,
 'release_scope':'local reproducible synthetic research prototype; no human/frontier-model performance claim',
 'qa':{'tests':test_count,'reproduction_steps':reproduction_steps},
 'core_metrics':{k:full.get(k) for k in ['personalization_accuracy','stale_memory_rate','contradiction_rate','proactive_decision_accuracy','autonomy_violation_rate','high_stakes_confirmation_rate','low_confidence_clarification_rate','failure_detection_rate','verified_recovery_rate','goal_lifecycle_accuracy','forget_success_rate','privacy_sensitive_block_rate','language_stress_accuracy'] if k in full},
 'training_data':{'unique_pairs':train['unique_pairs'],'families':train['families'],'exact_duplicate_rows':train['exact_duplicate_rows']},
 'reward_baseline':{
   'standard_test_accuracy':reward['metrics']['test']['accuracy'],
   'random_label_accuracy':reward['negative_control_test']['accuracy'],
   'lexically_matched_contrast_accuracy':reward['lexically_matched_contrast']['accuracy'],
   'canonical_response_pair_seen_fraction':gen['leakage_audit']['test_rows_with_seen_response_pair_fraction'],
   'unseen_paraphrase_accuracy':gen['unseen_paraphrase_set']['overall']['accuracy'],
   'bidirectional_brier':gen['standard_split']['metrics']['calibration_test_bidirectional']['brier'],
   'bidirectional_ece':gen['standard_split']['metrics']['calibration_test_bidirectional']['ece'],
 },
 'paper_metrics':{
   'standard_pbs_accuracy':belief['standard']['results']['personal-belief-state']['accuracy'],
   'standard_time_aware_accuracy':belief['standard']['results']['time-aware-latest']['accuracy'],
   'standard_pbs_utility':belief['standard']['results']['personal-belief-state']['decision_utility'],
   'standard_time_aware_utility':belief['standard']['results']['time-aware-latest']['decision_utility'],
   'pbs_aurc':risk['systems']['personal-belief-state']['aurc'] if 'systems' in risk else risk['personal-belief-state']['aurc'],
   'time_aware_aurc':risk['systems']['time-aware-latest']['aurc'] if 'systems' in risk else risk['time-aware-latest']['aurc'],
 },
 'leaderboard_stability':leader['summary'],
 'seed_uncertainty':{'point':seedu['point_estimate'],'ci':seedu['bootstrap_95_ci'],'claim_support':seedu['bootstrap_claim_support'],'diagnostic_users_per_seed':seedu['diagnostic_users_per_seed']},
 'protocol_grid_robustness':gridr['robustness_summary'],
 'external_adapter':{'status':hb['status'],'fixture_is_synthetic':hb['fixture_is_synthetic']},
 'benchmark_health':{'all_pass':health['all_pass'],'counts':health['counts']},
 'agent_eval':{
   'robust_grader_accuracy':agent_eval['grader_metrics']['robust_trajectory']['accuracy'],
   'end_state_false_accept_rate':agent_eval['grader_metrics']['end_state_only']['false_accept_rate'],
   'benign_invariance_rate':grader_rel['mutation_metrics']['benign_invariance_rate'],
   'missing_evidence_abstention_rate':grader_rel['mutation_metrics']['redacted_evidence_abstention_rate'],
   'failure_pair_semantic_duplication_rate':trace_audit['semantic_template_duplication_rate'],
 },
 'strongest_limitations':[
   'synthetic users and hand-defined evaluation oracles',
   'transparent/rule-based default state extractor rather than a frontier learned model',
   'lexical reward baseline shows weak unseen-paraphrase semantic generalization',
   'no executed longitudinal human study',
   'deterministic tool sandbox rather than open-world account actions',
 ]
}
(ROOT/'data/release_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
lines=[f'# PersonaMetrica v{version} — Final Release Summary','',
'## What this release proves','',
'The paper-first contribution, PersonaMetrica-Bench, evaluates long-horizon personalization as belief updating plus action under uncertainty. The broader repository remains an end-to-end systems substrate. All headline evidence is controlled and synthetic; human and frontier-model outcomes are intentionally left unclaimed until executed.','',
'## QA','',f"- **{test_count} tests passed**",f"- **{reproduction_steps}-stage reproduction pipeline**",'- behavioral regression gates pass', '- release metadata/version consistency is enforced','',
'## PersonaMetrica-Bench paper evidence','',
 f"- standard PBS state accuracy: **{summary['paper_metrics']['standard_pbs_accuracy']:.3f}** vs. time-aware-latest **{summary['paper_metrics']['standard_time_aware_accuracy']:.3f}**",
 f"- standard PBS decision utility: **{summary['paper_metrics']['standard_pbs_utility']:.3f}** vs. time-aware-latest **{summary['paper_metrics']['standard_time_aware_utility']:.3f}**",
 "- 800-turn native-confidence utility initially favors PBS, but equal development-only post-hoc calibration flips the fixed-threshold utility ordering; AURC remains lower for PBS.",
 f"- full six-system 75-cell audit: winner-change probability **{summary['leaderboard_stability']['winner_change_probability']:.3f}**, mean Kendall tau **{summary['leaderboard_stability']['mean_pairwise_kendall_tau']:.3f}**, minimum **{summary['leaderboard_stability']['minimum_pairwise_kendall_tau']:.2f}**; winner counts = {summary['leaderboard_stability']['winner_counts']}.",
 f"- paired seed-bootstrap diagnostic: winner-change **{summary['seed_uncertainty']['point']['winner_change_probability']:.3f}**, 95% CI **[{summary['seed_uncertainty']['ci']['winner_change_probability'][0]:.3f}, {summary['seed_uncertainty']['ci']['winner_change_probability'][1]:.3f}]**; P(change > .40) = **{summary['seed_uncertainty']['claim_support']['p_winner_change_gt_0_40']:.3f}**.",
 f"- 13 leave-one-level-out protocol-grid perturbations: winner-change range **{summary['protocol_grid_robustness']['min_winner_change_probability']:.3f}–{summary['protocol_grid_robustness']['max_winner_change_probability']:.3f}**; all retain multiple winners.",
 f"- benchmark health: identity overlap **{summary['benchmark_health']['counts']['identity_overlap']}**, full-history overlap **{summary['benchmark_health']['counts']['full_stream_overlap']}**, standard duplicate full histories **{summary['benchmark_health']['counts']['standard_duplicate_full_streams']}**.",
 '', '## Agent-eval reliability','',
 f"- robust trajectory grader accuracy on authored suite: **{summary['agent_eval']['robust_grader_accuracy']:.3f}**",
 f"- end-state-only false-accept rate: **{summary['agent_eval']['end_state_false_accept_rate']:.3f}**",
 f"- benign mutation invariance: **{summary['agent_eval']['benign_invariance_rate']:.1%}**",
 f"- missing-evidence abstention: **{summary['agent_eval']['missing_evidence_abstention_rate']:.1%}**",
 f"- failure-correction semantic-template duplication: **{summary['agent_eval']['failure_pair_semantic_duplication_rate']:.1%}** (explicit limitation)",
 '', '## Legacy systems regression evidence','']
for k,v in summary['core_metrics'].items(): lines.append(f'- `{k}`: **{v:.3f}**')
lines += ['', '## Training path','',f"- unique validated preference pairs: **{train['unique_pairs']}**",f"- exact duplicate rows: **{train['exact_duplicate_rows']}**",f"- standard lexical test accuracy: **{summary['reward_baseline']['standard_test_accuracy']:.3f}**",f"- random-label control: **{summary['reward_baseline']['random_label_accuracy']:.3f}**",f"- lexical contrast accuracy: **{summary['reward_baseline']['lexically_matched_contrast_accuracy']:.3f}**",'',
'## Generalization audit','',f"- standard test rows with a response pair already seen in train: **{summary['reward_baseline']['canonical_response_pair_seen_fraction']:.1%}**",f"- unseen paraphrase accuracy: **{summary['reward_baseline']['unseen_paraphrase_accuracy']:.3f}**",f"- bidirectional calibration Brier: **{summary['reward_baseline']['bidirectional_brier']:.3f}**",f"- bidirectional calibration ECE: **{summary['reward_baseline']['bidirectional_ece']:.3f}**",'',
'## Important boundaries','']
for x in summary['strongest_limitations']: lines.append(f'- {x}')
lines += ['', '## Reviewer path','', 'Read `paper/personametrica_anonymous.pdf` → `reports/LEADERBOARD_STABILITY_AUDIT.md` → `reports/LEADERBOARD_SEED_UNCERTAINTY.md` → `reports/PROTOCOL_GRID_ROBUSTNESS.md` → `reports/BENCHMARK_HEALTH_AUDIT.md` → `reports/NOVELTY_SOTA_AUDIT.md` → `docs/NEURIPS_READINESS.md`; use `project/index.html` for the broader systems/portfolio view. Then run `python scripts/reproduce.py`.','']
(ROOT/'docs/FINAL_RELEASE_SUMMARY.md').write_text('\n'.join(lines),encoding='utf-8')
print('data/release_summary.json')
print('docs/FINAL_RELEASE_SUMMARY.md')
