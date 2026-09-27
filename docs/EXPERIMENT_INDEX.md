# Experiment Index

This is the shortest path from a research claim to its executable command and checked-in evidence.

| Experiment | Question | Command | Primary evidence |
|---|---|---|---|
| Temporal-memory ablation | Does temporal updating reduce stale personalization? | `python experiments/run_ablations.py` | `data/ablation_results.json` |
| Multi-seed robustness | Are effects stable across simulator seeds? | `python scripts/robustness.py` | `reports/ROBUSTNESS.md` |
| Paired statistics | What are repeated-run effect sizes? | `python scripts/statistical_analysis.py` | `reports/STATISTICAL_ANALYSIS.md` |
| Failure slices | Where does proactivity still fail? | `python scripts/failure_analysis.py` | `reports/FAILURE_ANALYSIS.md` |
| Adversarial language | Does state updating survive difficult language? | `python scripts/build_v12_reports.py` | `reports/ADVERSARIAL_EVAL.md` |
| Training-data audit | Is preference data valid and deduplicated? | `python scripts/audit_training_data.py` | `reports/TRAINING_DATA_AUDIT.md` |
| Learned reward baseline | Can preference data train a real scorer? | `python scripts/train_reward_baseline.py` | `reports/LEARNED_REWARD_BASELINE.md` |
| Regression gate | Would a behavioral regression block release? | `python scripts/regression_gate.py` | `configs/regression_gates.json` |

For scope boundaries and non-claims, use `docs/EVIDENCE_LEDGER.md` rather than inferring broader conclusions from a metric.

## Reward generalization and leakage audit

```bash
python scripts/reward_generalization_eval.py
```

Outputs: `data/reward_generalization_results.json`, `reports/REWARD_GENERALIZATION.md`. Measures canonical response-pair overlap, bidirectional calibration, leave-one-family-out accuracy, and unseen response-paraphrase accuracy.
