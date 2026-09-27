# 8–10 Minute Research Talk: PersonaMetrica

## 1 — Problem
Personal assistants should improve with repeated interaction, but naive personalization can make them stale, intrusive, or overconfident.

## 2 — Research question
Can longitudinal utility improve while stale memory, incorrect personalization, and autonomy violations remain controlled?

## 3 — System
Interaction → temporal user state → memory/goals → proactivity → planning/tools → verification → feedback/reward → eval/training data.

## 4 — Temporal memory
Every retained belief carries provenance, confidence, stability, and time. Preference reversal supersedes the older state while preserving history.

## 5 — Proactivity
The policy chooses ask/suggest/remind/wait/none using goal relevance, urgency, confidence, stakes, reversibility, user autonomy preference, historical acceptance, and interruptibility.

## 6 — PersonalBench
Seeded synthetic users exhibit stable, conditional, and drifting preferences. Deterministic graders make regression testing cheap and reproducible.

## 7 — Baseline result
On the bundled controlled benchmark, the temporal system avoids the stale-memory failure that appears in a first-mention memory baseline. This is mechanism evidence, not a human-product claim.

## 8 — Tools and verification
All actions run in a safe deterministic sandbox; expected state is compared with observed state before success is accepted.

## 9 — Feedback to training
Failures and corrections produce structured preference pairs suitable for a later GPU-backed SFT/DPO/RL stage.

## 10 — Limitations and next research step
Replace rule-based extraction with a model-based structured estimator, calibrate learned graders against humans, and execute the preregistered longitudinal human study.
