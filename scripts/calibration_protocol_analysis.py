from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
raw=json.loads((ROOT/'data'/'belief_long_horizon_statistics.json').read_text())
cal=json.loads((ROOT/'data'/'calibrated_baseline_results.json').read_text())
aurc=json.loads((ROOT/'data'/'belief_risk_coverage.json').read_text())

def mean(xs): return sum(xs)/len(xs)
raw_gain=raw['summary']['utility_gain']['mean']
cal_t=cal['methods']['time-aware-latest']['long_horizon']
cal_p=cal['methods']['personal-belief-state']['long_horizon']
cal_gain=cal_p['decision_utility']-cal_t['decision_utility']
res={
 'raw_long_horizon_utility_gain_pbs_vs_time_aware':raw_gain,
 'dev_calibrated_long_horizon_utility_gain_pbs_vs_time_aware':cal_gain,
 'ranking_flip': raw_gain>0 and cal_gain<0,
 'calibrated_long_horizon':{'time-aware-latest':cal_t,'personal-belief-state':cal_p},
 'aurc':{'time-aware-latest':aurc['time-aware-latest']['aurc'],'personal-belief-state':aurc['personal-belief-state']['aurc']},
 'calibration_protocol':'Laplace-smoothed empirical correctness per raw-confidence bucket, fit on seeds 1-3 only; frozen on seeds 10-19 and 30-39.',
 'interpretation':'Fixed-threshold utility is not protocol-invariant. Equal post-hoc dev calibration reverses the long-horizon utility ordering; AURC remains a threshold-free ranking of confidence ordering and favors PBS in the checked-in benchmark.'
}
(ROOT/'data'/'calibration_protocol_analysis.json').write_text(json.dumps(res,indent=2))
lines=['# Calibration Protocol Analysis','',
'## Why this analysis exists','',
'The earlier benchmark compared trackers using their native confidence values. Because downstream utility uses a fixed confidence threshold, unequal confidence calibration can itself determine which system acts. We therefore give **every tracker the same low-capacity post-hoc calibration opportunity on development seeds 1–3 only** and freeze that mapping before evaluation.','',
'## Long-horizon result','',
'| Protocol | Time-aware latest utility | PBS utility | PBS − baseline | Ranking |','|---|---:|---:|---:|---|',
f"| Native confidence | — | — | {raw_gain:+.3f} | PBS higher |",
f"| Dev-calibrated confidence | {cal_t['decision_utility']:.3f} | {cal_p['decision_utility']:.3f} | {cal_gain:+.3f} | time-aware latest higher |",'',
'**The ordering flips.** This invalidates any broad claim that the fixed-threshold utility result by itself proves PBS is the better long-horizon decision substrate. Instead, the result demonstrates that utility at a fixed action threshold is partly a property of the calibration protocol.','',
'## Threshold-free confidence ordering','',
f"AURC (lower is better): time-aware latest = **{res['aurc']['time-aware-latest']:.4f}**, PBS = **{res['aurc']['personal-belief-state']:.4f}**. Post-hoc monotone calibration does not change the ordering of confidence scores, so AURC is the cleaner primary comparison for selective risk in this controlled setting.",'',
'## Reporting recommendation','',
'Personal-agent evaluations that let confidence control action should report at least: (1) state accuracy, (2) calibration quality, (3) risk–coverage/AURC, and (4) utility only under an explicitly specified and equally calibrated decision protocol. Reporting fixed-threshold utility from native confidence values can create a ranking that disappears or reverses after fair calibration.','',
'## Boundary','',
'This is a controlled simulator result. The calibrator is intentionally simple (Laplace-smoothed empirical correctness by raw-confidence bucket); it does not establish that the same reversal occurs for learned frontier-model confidence. It establishes a concrete evaluation confound that future model-backed studies should control.']
(ROOT/'reports'/'CALIBRATION_PROTOCOL_ANALYSIS.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(res,indent=2))
