# PersonaMetrica — frontier research brief

**Aura Yavary · sole researcher / engineer**

## Research thesis

Personal-agent quality is not a scalar property of a model. In long-horizon settings, the apparent winner can depend on how confidence is calibrated, when the system is allowed to act, what cost is assigned to deferral, and whether the evaluator itself generalizes. PersonaMetrica treats those choices as first-class experimental variables rather than invisible benchmark plumbing.

## Strongest evidence

- **75 frozen evaluation protocols × six systems.** The winner changes materially across the grid; three methods win at least one cell.
- **Full-ranking instability.** Mean pairwise Kendall tau is 0.699, with a minimum of 0.20 across released protocols.
- **Seed uncertainty.** 2,000 paired resamples retain a winner-change estimate around 0.516; the 95% simulator-seed interval is [0.507, 0.538].
- **Grid robustness.** All 13 leave-one-level-out perturbations still contain multiple winners.
- **Evaluator validity.** A frozen grader false-accepts 96% of five new attack families; a causal-contract grader rejects all released attacks while preserving the original gold-suite labels.
- **Negative result kept visible.** PBS nuisance invariance is 98.0%, not 100%: high-confidence other-person evidence can still flip close decisions.

## What this demonstrates as research work

1. **Agenda formation:** moved from “build a better personal memory” to the harder measurement question after stronger baselines and calibration invalidated an early utility claim.
2. **Experimental discipline:** development-only tuning/calibration, held-out seeds, protocol fingerprinting, bootstrap uncertainty, perturbation audits, and negative results.
3. **Evaluator engineering:** trace contracts, abstention on missing evidence, OOD grader attacks, disagreement routing, fingerprints, and failure-to-data conversion.
4. **Systems execution:** installable Python package, deterministic tool sandbox, verification/recovery, runtime traces, CI-style release gates, static reviewer site, and anonymous submission bundle.
5. **Research restraint:** external adapters and human-annotation infrastructure exist, but no model/human result is claimed until it is actually run.

## Why this is relevant to frontier labs

Current frontier research roles emphasize owning research agendas, robust evaluations, model behavior, post-training/data loops, agent trajectories, and debugging research stacks. PersonaMetrica is deliberately organized around that workflow: identify a behavioral bottleneck → build an eval → attack the eval → turn failures into structured data → gate regressions → narrow claims when evidence changes.

Public role descriptions reviewed September 2026:
- OpenAI Personal AGI, Proactivity: https://openai.com/careers/research-engineer-research-scientist-personal-agi-proactivity-san-francisco/
- OpenAI Personal AGI, North Stars: https://openai.com/careers/research-engineerresearch-scientist-personal-agi-north-stars-san-francisco/
- Anthropic agent-eval engineering guidance: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents

## Fastest way to inspect

```bash
python scripts/reviewer_demo.py
```

Then read `reports/REVIEWER_DEMO.md` and `docs/EVIDENCE_LEDGER.md`.
