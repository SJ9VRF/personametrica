from __future__ import annotations
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from external_benchmarks.horizonbench_adapter import load_results,compare_models,utility

def main():
    fx=ROOT/'external_benchmarks'/'fixtures'
    models={
      'fixture-model-a':load_results(fx/'horizonbench_results_model_a.jsonl'),
      'fixture-model-b':load_results(fx/'horizonbench_results_model_b.jsonl'),
    }
    summaries=compare_models(models)
    for name,rows in models.items():
        summaries[name]['utility_t070_c010']=utility(rows,.70,.10)
    out={'version':'4.2.0','status':'schema-smoke-test-only','source_schema':'HorizonBench official evaluate.py JSONL result schema','fixture_is_synthetic':True,'models':summaries,
         'claim_boundary':'These fixture scores are not HorizonBench model results. The adapter is executable infrastructure awaiting real official result JSONL files.'}
    (ROOT/'data'/'horizonbench_adapter_smoke.json').write_text(json.dumps(out,indent=2)+'\n')
    report=['# HorizonBench External-Result Adapter Smoke Test','',
      'PersonaMetrica includes an adapter for the official HorizonBench `evaluate.py` per-item result schema: `id`, `generator`, `has_evolved`, `correct_letter`, `predicted_letter`, and `correct`. An optional `confidence` field enables PersonaMetrica operating-point analyses without changing the required HorizonBench fields.','',
      '**Important:** the checked-in rows are synthetic schema fixtures, not HorizonBench benchmark examples and not model results. This runtime could verify the public schema but could not retrieve the Hugging Face parquet or run paid/frontier inference. No external score is claimed.','',
      '## Executed fixture result','', '| Fixture | N | Accuracy | Evolved | Static | Utility (t=.70,c=.10) |','|---|---:|---:|---:|---:|---:|']
    for name,s in summaries.items():
        report.append(f"| {name} | {s['n']} | {s['accuracy']:.3f} | {s['evolved_accuracy']:.3f} | {s['static_accuracy']:.3f} | {s['utility_t070_c010']:.3f} |")
    report += ['', '## Why this exists','',
      'External validation should not require rewriting the evaluator around a new benchmark. Given real HorizonBench result JSONL files for multiple models or memory systems, this adapter verifies item alignment, reproduces overall/evolved/static accuracy slices, and can apply confidence-gated utility only when confidence is actually supplied. Missing confidence is an explicit error rather than an invented value.']
    (ROOT/'reports'/'HORIZONBENCH_ADAPTER_SMOKE.md').write_text('\n'.join(report)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
