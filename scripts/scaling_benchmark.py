from __future__ import annotations
import json, time, statistics, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from personalbench.runner import evaluate_config
from personalagi.config import AgentConfig

CASES=[
    {"users":10,"turns":20},
    {"users":25,"turns":60},
    {"users":100,"turns":60},
    {"users":100,"turns":120},
    {"users":250,"turns":60},
]
rows=[]
for c in CASES:
    samples=[]
    for rep in range(2):
        t0=time.perf_counter()
        evaluate_config('full_scaling',AgentConfig.full(),c['users'],c['turns'],7+rep)
        samples.append(time.perf_counter()-t0)
    median=statistics.median(samples)
    interactions=c['users']*c['turns']
    rows.append({
        **c,
        'interactions':interactions,
        'wall_seconds_median':round(median,4),
        'microseconds_per_interaction':round(median/interactions*1e6,2),
        'external_api_calls':0,
        'external_inference_cost_usd':0.0,
    })
out={
  'scope':'local deterministic default stack; measured on the release-build environment, excludes electricity/hardware amortization and external model-backed adapters',
  'model_size':'model-agnostic architecture; default state extractor is deterministic and reward baseline is a sparse linear ranker',
  'tool_primitives':3,
  'tool_names':['task_store','notes','reminders'],
  'cases':rows,
}
(ROOT/'data/scaling_results.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
md=['# Scaling and Runtime Profile','','Scope: '+out['scope'],'',
    '| Users | Turns | Interactions | Median wall time | µs / interaction | External API cost |',
    '|---:|---:|---:|---:|---:|---:|']
for r in rows:
    md.append(f"| {r['users']} | {r['turns']} | {r['interactions']} | {r['wall_seconds_median']:.3f}s | {r['microseconds_per_interaction']:.2f} | $0.00 |")
md += ['', '## Interpretation','',
       '- These numbers describe the deterministic local research substrate, not an LLM-backed production deployment.',
       '- External model latency/cost is intentionally excluded until a real model adapter is connected and measured.',
       '- The architecture is model-agnostic; the default release uses deterministic extraction plus a sparse linear reward baseline.',
       '- The sandbox exposes three tool primitives: task storage, notes, and reminders.',
       '']
(ROOT/'reports/SCALING.md').write_text('\n'.join(md),encoding='utf-8')
print(json.dumps(out,indent=2))
