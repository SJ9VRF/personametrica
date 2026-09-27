# HorizonBench External-Result Adapter Smoke Test

PersonaMetrica includes an adapter for the official HorizonBench `evaluate.py` per-item result schema: `id`, `generator`, `has_evolved`, `correct_letter`, `predicted_letter`, and `correct`. An optional `confidence` field enables PersonaMetrica operating-point analyses without changing the required HorizonBench fields.

**Important:** the checked-in rows are synthetic schema fixtures, not HorizonBench benchmark examples and not model results. This runtime could verify the public schema but could not retrieve the Hugging Face parquet or run paid/frontier inference. No external score is claimed.

## Executed fixture result

| Fixture | N | Accuracy | Evolved | Static | Utility (t=.70,c=.10) |
|---|---:|---:|---:|---:|---:|
| fixture-model-a | 6 | 0.667 | 0.667 | 0.667 | 0.300 |
| fixture-model-b | 6 | 0.667 | 0.667 | 0.667 | 0.633 |

## Why this exists

External validation should not require rewriting the evaluator around a new benchmark. Given real HorizonBench result JSONL files for multiple models or memory systems, this adapter verifies item alignment, reproduces overall/evolved/static accuracy slices, and can apply confidence-gated utility only when confidence is actually supplied. Missing confidence is an explicit error rather than an invented value.
