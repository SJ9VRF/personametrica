# External benchmark adapters

The paper distinguishes the **belief-update algorithm** from the **language/model layer**. The local release does not fabricate frontier-model results. Instead it defines a vendor-neutral evaluation contract.

## Model output schema

Each JSONL row supplied to `evals/external_model_eval.py` must contain:

```json
{"id":"item-1","expected":"morning","prediction":"morning","confidence":0.82}
```

This lets any model/provider be evaluated with the same accuracy, Brier, and ECE code after model outputs are collected once.

## Priority external evaluations

1. **HorizonBench** — evolving preferences over six-month histories; use its official split and report accuracy plus pre-evolution distractor errors.
2. **PrefEval** — explicit and implicit preference following; report classification and generation metrics using its official evaluator.
3. **LongMemEval** — extraction, multi-session reasoning, temporal reasoning, knowledge updates, and abstention.
4. **PerMemBench** — personalized storage/write policy under long horizons.
5. **ProactiveBench / UserVille** — independent proactivity labels and productivity/proactivity/personalization trade-offs.

Do not copy or silently modify third-party data into this repository. Download from the original project and retain its license/provenance.

## Executable HorizonBench result adapter

`external_benchmarks/horizonbench_adapter.py` consumes the per-item result schema documented by the official HorizonBench `evaluate.py` workflow. It validates item-level consistency and computes overall, evolved, and static accuracy. If a system explicitly emits a confidence value for every item, the adapter can also apply PersonaMetrica confidence-gated utility. It never invents missing confidence.

Run the local schema smoke test with:

```bash
python scripts/external_horizonbench_smoke.py
```

The checked-in fixture rows are synthetic schema fixtures only. They are not HorizonBench examples and are not external model results.
