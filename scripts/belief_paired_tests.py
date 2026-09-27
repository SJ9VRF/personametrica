from __future__ import annotations
import json,itertools,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def signflip_p(vals):
    obs=abs(sum(vals)/len(vals)); n=len(vals); hit=0; tot=0
    for signs in itertools.product([-1,1], repeat=n):
        m=abs(sum(v*s for v,s in zip(vals,signs))/n); hit += m >= obs-1e-15; tot+=1
    return hit/tot

def sign_test(vals):
    n=len(vals); k=sum(v>0 for v in vals); k=min(k,n-k)
    # exact two-sided binomial around 0.5
    prob=sum(math.comb(n,i) for i in range(k+1))/2**n
    return min(1.0,2*prob)

def main():
    standard=json.load(open(ROOT/'data/belief_statistics.json'))['runs']
    long=json.load(open(ROOT/'data/belief_long_horizon_statistics.json'))['runs']
    specs={
      'standard_utility':[r['utility_gain_vs_time_aware'] for r in standard],
      'standard_accuracy':[r['accuracy_delta_vs_time_aware'] for r in standard],
      'long_utility':[r['utility_gain'] for r in long],
      'long_accuracy':[r['accuracy_delta'] for r in long],
      'long_brier':[r['brier_reduction'] for r in long],
    }
    out={k:{'n':len(v),'mean':sum(v)/len(v),'positive':sum(x>0 for x in v),'negative':sum(x<0 for x in v),'exact_sign_test_p':sign_test(v),'paired_signflip_p':signflip_p(v)} for k,v in specs.items()}
    (ROOT/'data/belief_paired_tests.json').write_text(json.dumps(out,indent=2))
    lines=['# Paired held-out significance tests','', 'Exact paired tests over the ten pre-specified held-out simulator seeds. These quantify stability across simulator seeds; they are not human-population inferential statistics.','', '| Comparison | n | Mean Δ | + / − seeds | sign-test p | sign-flip p |','|---|---:|---:|---:|---:|---:|']
    for k,r in out.items(): lines.append(f"| {k.replace('_',' ')} | {r['n']} | {r['mean']:+.4f} | {r['positive']} / {r['negative']} | {r['exact_sign_test_p']:.4f} | {r['paired_signflip_p']:.4f} |")
    (ROOT/'reports/BELIEF_PAIRED_TESTS.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
