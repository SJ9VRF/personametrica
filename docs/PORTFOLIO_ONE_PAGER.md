# PersonaMetrica — Portfolio One-Pager

## Thesis

A personal agent should become more useful over time **without** becoming stale, intrusive, overconfident, privacy-blind, or behaviorally unstable.

## What is implemented

A closed-loop research platform connecting temporal user state, memory reconciliation, goals, calibrated proactivity, planning, tool execution, outcome verification, structured feedback, preference-data generation, learned reward scoring, benchmark evaluation, failure analysis, persistence, privacy controls, and release regression gates.

## What makes it more than a chatbot demo

- Temporal state replaces “vector DB = memory.”
- Explicit supersession distinguishes current beliefs from historical beliefs.
- Proactivity is evaluated as a decision/calibration problem.
- Tool calls are verified against world state.
- User forgetting and privacy have executable mechanisms and ablations.
- Every headline claim maps to an experiment or an explicit limitation.
- Preference supervision flows into a genuinely trained local ranking model.
- Negative controls and contrast tests expose where the learned baseline fails.

## Current evidence

- 36 automated tests.
- 100-user × 60-turn controlled longitudinal benchmark.
- Real mechanism ablations and multi-seed robustness runs.
- 1,000-scenario proactivity failure slicing.
- Adversarial preference-language stress suite.
- 724 unique validated preference pairs after exact deduplication.
- Learned pairwise reward baseline with group-aware holdout, random-label control, and lexical contrast test.
- Behavioral regression gates that fail the release on key degradations.

## Important limitation

The checked-in empirical evidence is synthetic/controlled. The local learned scorer is deliberately small and lexical. The repository does not claim human longitudinal gains, frontier-model reward quality, or foundation-model DPO/RL improvement.

## Next external experiment

Use the existing inference adapter to replay structured outputs from an open-weight or API model, then replace the lexical learned scorer with model-backed reward/preference learning while keeping the same evaluation and regression surfaces.
