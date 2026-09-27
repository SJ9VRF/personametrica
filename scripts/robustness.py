from __future__ import annotations
import json, math, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from personalbench.runner import run_detailed_comparison

SEEDS = [1, 7, 19, 42, 73]
METRICS = [
    'personalization_accuracy','stale_memory_rate','contradiction_rate','goal_capture_rate',
    'proactive_decision_accuracy','autonomy_violation_rate','high_stakes_confirmation_rate',
    'low_confidence_clarification_rate','failure_detection_rate','memory_confidence_brier'
]

def mean(xs): return sum(xs)/len(xs) if xs else 0.0

def std(xs):
    if len(xs) < 2: return 0.0
    m=mean(xs); return math.sqrt(sum((x-m)**2 for x in xs)/(len(xs)-1))

def main():
    runs=[]
    for seed in SEEDS:
        runs.append(run_detailed_comparison(n_users=100, turns=60, seed=seed))
    systems=runs[0]['systems'].keys(); summary={}
    for system in systems:
        summary[system]={}
        for metric in METRICS:
            vals=[r['systems'][system]['metrics'][metric] for r in runs]
            summary[system][metric]={'mean':mean(vals),'std':std(vals),'min':min(vals),'max':max(vals)}
    effects={
        'temporal_update_personalization_gain': summary['full_temporal_os']['personalization_accuracy']['mean'] - summary['no_temporal_update']['personalization_accuracy']['mean'],
        'temporal_update_stale_memory_reduction': summary['no_temporal_update']['stale_memory_rate']['mean'] - summary['full_temporal_os']['stale_memory_rate']['mean'],
        'contradiction_resolution_reduction': summary['no_contradiction_resolution']['contradiction_rate']['mean'] - summary['full_temporal_os']['contradiction_rate']['mean'],
        'calibrated_proactivity_accuracy_gain': summary['full_temporal_os']['proactive_decision_accuracy']['mean'] - summary['uncalibrated_proactivity']['proactive_decision_accuracy']['mean'],
        'verification_failure_detection_gain': summary['full_temporal_os']['failure_detection_rate']['mean'] - summary['no_outcome_verification']['failure_detection_rate']['mean'],
    }
    out={'seeds':SEEDS,'users_per_seed':100,'turns':60,'summary':summary,'effects':effects}
    Path('data/robustness_results.json').write_text(json.dumps(out,indent=2))
    lines=['# Robustness across random seeds','',f"Evaluated {len(SEEDS)} seeds × 100 synthetic users × 60 turns. These are controlled synthetic results, not human or frontier-model claims.",'', '| Effect | Mean difference |','|---|---:|']
    for k,v in effects.items(): lines.append(f"| {k.replace('_',' ')} | {v:.3f} |")
    lines += ['', '## Full-system stability', '', '| Metric | Mean | Std | Min | Max |','|---|---:|---:|---:|---:|']
    for metric,stat in summary['full_temporal_os'].items():
        lines.append(f"| {metric} | {stat['mean']:.3f} | {stat['std']:.3f} | {stat['min']:.3f} | {stat['max']:.3f} |")
    Path('reports/ROBUSTNESS.md').write_text('\n'.join(lines)+'\n')
    print('data/robustness_results.json')
    print('reports/ROBUSTNESS.md')

if __name__=='__main__': main()
