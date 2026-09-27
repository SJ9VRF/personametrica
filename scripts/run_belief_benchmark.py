from __future__ import annotations
import json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personalbench.belief_benchmark import run_distribution_shifts

out=run_distribution_shifts()
path=ROOT/'data'/'belief_benchmark_results.json'
path.write_text(json.dumps(out,indent=2),encoding='utf-8')

lines=["# Personal Belief State Benchmark", "", "Controlled structured-evidence benchmark. This isolates belief updating from natural-language extraction; it does not constitute frontier-model evaluation.", ""]
for split,row in out.items():
    lines += [f"## {split.replace('_',' ').title()}", "", "| Method | State accuracy | Coverage | Selective accuracy | Decision utility | Brier ↓ |", "|---|---:|---:|---:|---:|---:|"]
    for method,m in row['results'].items():
        lines.append(f"| {method} | {m['accuracy']:.3f} | {m['coverage']:.3f} | {m['selective_accuracy']:.3f} | {m['decision_utility']:.3f} | {m['brier']:.3f} |")
    lines.append("")
(ROOT/'reports'/'BELIEF_STATE_BENCHMARK.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps(out['standard']['results'],indent=2))
print(f"Wrote {path.relative_to(ROOT)} and reports/BELIEF_STATE_BENCHMARK.md")
