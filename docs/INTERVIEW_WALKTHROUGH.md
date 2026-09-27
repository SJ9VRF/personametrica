# 8-minute technical walkthrough

## 0:00–1:00 — Problem
Personalization is not retrieval. A long-lived assistant must decide what to infer, remember, update, forget, and when to intervene—without turning stale, intrusive, or overconfident.

## 1:00–2:00 — Architecture
Walk through `docs/architecture.svg`: interaction → personal state → memory/goals → proactivity → plan/tool → verification → feedback → eval/training data.

## 2:00–3:00 — Temporal world model
Show a preference reversal. Explain provenance, confidence, supersession history, conditional preferences, and cross-session persistence.

## 3:00–4:00 — Proactivity as judgment
Explain `act / ask / suggest / remind / wait / none`, stakes, reversibility, uncertainty, autonomy preference, and why high-stakes actions require confirmation.

## 4:00–5:00 — Evaluation design
Show real feature-toggle ablations, adversarial language cases, user-control tests, and multi-seed robustness. Emphasize that synthetic results are scoped as mechanism validation.

## 5:00–6:00 — Failure analysis
Open `reports/FAILURE_ANALYSIS.md`; discuss low-value and ordinary cases as current research surfaces instead of hiding them.

## 6:00–7:00 — ML-system boundary
Show `personalagi/adapters/`: deterministic local inference is replaceable by a learned model. All downstream behavior, privacy, memory and eval infrastructure remains identical.

## 7:00–8:00 — Research loop
Failure → structured feedback → preference pair → post-training interface → PersonalBench → regression gate. End with the next empirical step: real model adaptation and longitudinal human evaluation.
