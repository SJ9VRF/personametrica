# Building a Personal AI That Knows When to Change Its Mind

**Aura Yavary · 2026**

Most personal-assistant demos answer a simple question: can the model respond usefully right now? Personal intelligence creates a harder question: can the system become more useful over weeks of interaction without becoming stale, intrusive, overconfident, or wrong?

That is the problem behind **PersonaMetrica**, a reproducible research platform for longitudinal personalized agents. The project is intentionally not another chat UI wrapped around a vector database. It treats personalization as an evolving state-estimation and control problem.

## The central failure mode: people change

Suppose a user says they prefer working in the evening. A week later they say mornings work better now. A retrieval-only memory system can surface both facts; it does not automatically know which one should govern current behavior. Worse, a personal agent may act on the stale preference at exactly the wrong moment.

PersonaMetrica represents memories with time, provenance, confidence, stability, and supersession. The goal is not merely to remember more. It is to maintain a usable model of what is *currently true*.

## Memory is only one part of personal intelligence

The system connects temporal memory to goals and a calibrated proactivity policy. For each opportunity to intervene, the policy reasons over goal relevance, urgency, confidence, stakes, reversibility, interruptibility, historical acceptance, and the user's autonomy preference. The action space includes acting, asking, suggesting, reminding, waiting, or doing nothing.

That last option matters. A useful personal agent needs a model of when *not* to help.

## Tools are not trusted until outcomes are verified

Long-horizon agents often make a tool call and implicitly treat the call as success. PersonaMetrica separates execution from verification. The local sandbox produces observable state, and an outcome verifier compares that state with the expected result. A bounded recovery primitive can then correct a mismatched payload, retry once, and verify the second outcome.

This is deliberately small and transparent. It is a research substrate for studying failure and recovery, not a claim of open-world autonomous reliability.

## Evaluation is built around mechanisms

PersonalBench tests different failure surfaces independently: temporal preference drift, active contradictions, explicit forgetting, privacy-sensitive persistence, goal lifecycle, calibrated proactivity, tool-result verification, conditional preferences, and adversarial language.

The checked-in main benchmark uses 100 synthetic users over 60 turns plus 200 proactivity scenarios. A 10-seed paired analysis estimates the temporal-personalization gain at about 58 percentage points relative to a first-mention memory baseline. Removing contradiction resolution produces active conflicting state for a large fraction of synthetic users. Removing the verifier drops injected failure detection from 100% to zero.

These are controlled synthetic results. They validate mechanisms inside the research environment; they are not measurements of human satisfaction or frontier-model quality.

## The most useful result was a failure

The project also includes a local learned pairwise reward baseline. Its standard held-out accuracy looks perfect—but a leakage audit shows that most test rows reuse canonical response-pair wording seen in training. On genuinely unseen paraphrases, accuracy falls to roughly 67%.

That gap is more useful than the perfect headline. It shows that a lexical scorer can prove the training path works without proving semantic reward modeling. The release keeps that failure visible and makes it part of the next research question.

## What I wanted the artifact to demonstrate

The project is designed so that a reviewer can trace each claim to an implementation and an evaluation. Memory update has an ablation. Proactivity calibration has an ablation. Privacy has an ablation. Verification has an ablation. Failure slices are preserved. Regression gates prevent a release from quietly improving one behavior while degrading another.

The result is less a single assistant than a compact research program: user modeling, memory, proactivity, tools, verification, feedback, post-training data, evaluation, failure analysis, and release engineering all live in one reproducible loop.

## What comes next

The strongest next step is not another local feature. It is to replace transparent rule-based components with real model-backed extractors and reward models, then run the exact same leakage, calibration, failure, autonomy, and longitudinal evaluations. After that, the decisive test is a real multi-day human study.

Until those experiments exist, the project draws a strict boundary around what it claims. PersonaMetrica demonstrates an end-to-end architecture and a reproducible method for asking whether an AI system is actually learning a person over time—not evidence that the full problem is solved.
