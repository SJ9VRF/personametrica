# Reproducibility

## Environment

Python 3.11 or newer. Runtime code has no third-party dependency. Tests require `pytest>=8`.

## Full reproduction

From repository root:

```bash
python scripts/reproduce.py
```

The script is fail-fast and sequentially executes tests, benchmark, dataset generation, preference-pair generation, ablations, dashboard generation, result-summary generation, and app metric refresh.

## Fixed benchmark configuration

- synthetic users: 100
- turns per user: 60
- seed: 7
- proactivity scenarios: 200

## Expected generated files

- `data/eval_results.json`
- `data/ablation_results.json`
- `data/personalbench.jsonl`
- `data/preference_pairs.jsonl`
- `dashboard/index.html`
- `reports/RESULTS.md`
- `app/index.html`

## Determinism

Persona construction and background utterance selection use fixed/local seeded PRNGs. `tests/test_ablations.py::test_benchmark_reproducible` asserts equality across repeated same-seed runs.

## Verification

```bash
python -m pytest -q
```

Current suite: 16 unit/integration/ablation/reproducibility tests.

## Additional diagnostics

```bash
python scripts/statistical_analysis.py
python scripts/failure_analysis.py
```

These generate `reports/STATISTICAL_ANALYSIS.md` and `reports/FAILURE_ANALYSIS.md` from deterministic benchmark seeds/scenarios.
