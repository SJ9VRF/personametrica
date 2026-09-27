from __future__ import annotations
import json
from pathlib import Path

def pct(x): return f'{100*x:.1f}%'

def main():
    d=json.loads(Path('data/eval_results.json').read_text()); s=d['systems']; b=d['benchmark']
    full=s['full_temporal_os']['metrics']; stale=s['no_temporal_update']['metrics']; conflict=s['no_contradiction_resolution']['metrics']; proactive=s['uncalibrated_proactivity']['metrics']; conf=s['no_confidence_tracking']['metrics']; verify=s['no_outcome_verification']['metrics']
    text=f'''# Reproducible Result Summary\n\nGenerated from `data/eval_results.json`. Benchmark: **{b['users']} synthetic users × {b['turns']} turns**, plus **{b['proactivity_scenarios']} proactivity scenarios**. These are controlled synthetic results, not human or frontier-model performance claims.\n\n## Main findings\n\n- **Temporal updating:** full system personalization accuracy {pct(full['personalization_accuracy'])}, stale-memory rate {pct(full['stale_memory_rate'])}; disabling temporal update yields {pct(stale['personalization_accuracy'])} accuracy and {pct(stale['stale_memory_rate'])} stale memory.\n- **Conflict resolution:** full system contradiction rate {pct(full['contradiction_rate'])}; disabling conflict resolution yields {pct(conflict['contradiction_rate'])}.\n- **Proactivity calibration:** calibrated policy decision accuracy {pct(full['proactive_decision_accuracy'])} with autonomy-violation rate {pct(full['autonomy_violation_rate'])}; uncalibrated policy yields {pct(proactive['proactive_decision_accuracy'])} and {pct(proactive['autonomy_violation_rate'])}.\n- **Confidence tracking:** memory-confidence Brier error {full['memory_confidence_brier']:.3f}; disabling confidence tracking yields {conf['memory_confidence_brier']:.3f}. Lower is better.\n- **Outcome verification:** failure detection {pct(full['failure_detection_rate'])}; disabling verification yields {pct(verify['failure_detection_rate'])}.\n\n## Interpretation boundary\n\nThe benchmark intentionally tests mechanisms the repository implements. It demonstrates that the mechanisms behave as specified under controlled conditions. It does **not** establish generalization to natural human behavior, production traffic, or frontier language models. The human-study protocol in `reports/HUMAN_STUDY_PROTOCOL.md` defines the next validation layer.\n'''
    Path('reports/RESULTS.md').write_text(text)
    print('reports/RESULTS.md')
if __name__=='__main__': main()
