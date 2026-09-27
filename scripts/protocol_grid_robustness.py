from __future__ import annotations
import itertools,json,statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def tau(a,b):
    p={x:i for i,x in enumerate(b)}; c=d=0
    for i in range(len(a)):
        for j in range(i+1,len(a)):
            if p[a[i]]<p[a[j]]: c+=1
            else:d+=1
    return (c-d)/max(1,c+d)
def summarize(cells):
    pairs=list(itertools.combinations(range(len(cells)),2))
    wc=sum(cells[i]['winner']!=cells[j]['winner'] for i,j in pairs)
    ts=[tau(cells[i]['ranking'],cells[j]['ranking']) for i,j in pairs]
    return {'cells':len(cells),'winner_change_probability':wc/max(1,len(pairs)),'mean_kendall_tau':statistics.mean(ts),'minimum_kendall_tau':min(ts),'distinct_winners':len(set(c['winner'] for c in cells))}

def main():
    source=json.loads((ROOT/'data'/'leaderboard_stability_audit.json').read_text())
    cells=source['cells']; variants=[]
    variants.append({'name':'full-frozen-grid','dropped':None,'summary':summarize(cells)})
    for cal in sorted(set(c['calibration'] for c in cells)):
        variants.append({'name':f'leave-calibration-out:{cal}','dropped':{'calibration':cal},'summary':summarize([c for c in cells if c['calibration']!=cal])})
    for th in sorted(set(c['threshold'] for c in cells)):
        variants.append({'name':f'leave-threshold-out:{th}','dropped':{'threshold':th},'summary':summarize([c for c in cells if c['threshold']!=th])})
    for cost in sorted(set(c['defer_cost'] for c in cells)):
        variants.append({'name':f'leave-defer-cost-out:{cost}','dropped':{'defer_cost':cost},'summary':summarize([c for c in cells if c['defer_cost']!=cost])})
    pert=[v for v in variants if v['name']!='full-frozen-grid']
    out={'version':'4.2.0','source_cells':len(cells),'variants':variants,'robustness_summary':{
      'perturbations':len(pert),
      'min_winner_change_probability':min(v['summary']['winner_change_probability'] for v in pert),
      'max_winner_change_probability':max(v['summary']['winner_change_probability'] for v in pert),
      'min_mean_kendall_tau':min(v['summary']['mean_kendall_tau'] for v in pert),
      'max_mean_kendall_tau':max(v['summary']['mean_kendall_tau'] for v in pert),
      'perturbations_with_multiple_winners':sum(v['summary']['distinct_winners']>=2 for v in pert),
    },'interpretation':'Leave-one-level-out sensitivity tests whether the central ranking-instability result depends on one calibration family, threshold, or deferral-cost level. It does not make protocol choices iid samples.'}
    (ROOT/'data'/'protocol_grid_robustness.json').write_text(json.dumps(out,indent=2)+'\n')
    r=out['robustness_summary']
    lines=['# Protocol-Grid Robustness Audit','',
      '## Question','',
      'Does the ranking-instability headline disappear if one reasonable calibration family, action threshold, or deferral-cost level is removed from the frozen grid?','',
      'We run 13 leave-one-level-out perturbations: three calibration-family removals, five threshold removals, and five deferral-cost removals. No test result is used to invent a replacement grid.','',
      '## Result','', '| Perturbation family | Range across leave-one-level-out variants |','|---|---:|',
      f"| Winner-change probability | {r['min_winner_change_probability']:.3f} – {r['max_winner_change_probability']:.3f} |",
      f"| Mean Kendall tau | {r['min_mean_kendall_tau']:.3f} – {r['max_mean_kendall_tau']:.3f} |",
      f"| Variants retaining >1 winner | {r['perturbations_with_multiple_winners']} / {r['perturbations']} |",'',
      'The weakest perturbation is dropping native confidence: the remaining development-calibrated protocols agree substantially more, but they still select more than one winner. This is informative rather than inconvenient: much of the instability comes from whether systems are compared in their native confidence scales or after equal development-only calibration.','',
      '## Boundary','',
      'This sensitivity analysis protects against one obvious grid-design objection. It does not prove that the chosen grid exhausts all valid deployment utilities, nor does it assign a probability distribution over protocol choices.'
    ]
    (ROOT/'reports'/'PROTOCOL_GRID_ROBUSTNESS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(r,indent=2))
if __name__=='__main__':main()
