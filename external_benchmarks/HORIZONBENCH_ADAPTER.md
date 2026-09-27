# HorizonBench adapter

`horizonbench_adapter.py` consumes the per-item JSONL schema documented by the official HorizonBench `evaluate.py` workflow.

Required fields:

- `id`
- `generator`
- `has_evolved`
- `correct_letter`
- `predicted_letter`
- `correct`

Optional field:

- `confidence` in `[0,1]`

The adapter never invents confidence. Accuracy/evolved/static summaries work on standard HorizonBench output. PersonaMetrica operating-point utility requires an explicit confidence value for every item.

The files under `fixtures/` are synthetic schema fixtures only. They are not copied HorizonBench data and must never be reported as external benchmark performance.
