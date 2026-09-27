# PersonaMetrica — Novelty & SOTA Positioning Audit

**Audit date:** 2026-09-26  
**Public author:** Aura Yavary  
**Scope:** long-horizon personalization, evolving preferences, memory, proactive agents, calibration/selective risk, and agent-evaluator reliability.

## Bottom line

PersonaMetrica is **not novel merely because it studies personalized memory, evolving preferences, belief revision, or proactive personal assistants**. Those areas are already active and well represented by 2025–2026 work. The defensible contribution is narrower and more evaluation-centric:

> **PersonaMetrica stress-tests whether conclusions about long-horizon personal agents remain stable when confidence calibration, action policy, and evaluator assumptions change; it then treats the evaluator itself as a fallible system subject to held-out attacks, causal-contract checks, abstention, versioning, and disagreement review.**

This is a credible novelty claim as a **combination and evaluation protocol**, not a “first personalization benchmark” claim. A search of current public literature found close components separately, including 2026 work on ranking stability, disagreement-aware aggregation, trajectory attribution, and long-horizon safety calibration. The narrower delta is the joint study of (1) protocol-induced ranking changes for evolving user-state systems, (2) confidence-calibrated action gating and risk–coverage, (3) counterfactual user-state interventions, and (4) evaluator validity under held-out distribution shift inside the same personal-agent evaluation artifact.

The full-leaderboard audit strengthens the first point: across 75 frozen protocol cells, time-aware-latest wins 45, PBS 27, and first-mention 3; two protocol cells select different winners with probability **0.516**. Mean complete-ranking Kendall tau is **0.699** and the minimum is **0.20**. v3.9 adds two anti-cherry-picking checks: a 2,000-replicate paired bootstrap over long-horizon simulator seeds on a separate 10-user-per-seed diagnostic cohort gives winner-change **0.516 [0.507, 0.538]**, and 13 leave-one-level-out protocol-grid perturbations all retain multiple winners. These are evidence of measurement fragility in the controlled benchmark, not evidence that any system is globally better or that the same rates hold for frontier models.

## Closest work and what it already owns

| Work | What it establishes | Why PersonaMetrica must not duplicate the claim | PersonaMetrica's narrower delta |
|---|---|---|---|
| **PrefEval** (ICLR 2025) | Long-context explicit/implicit preference following | Preference following is not new | Evaluates ranking stability once belief confidence gates action |
| **PersonaLens** (ACL Findings 2025) | Task-oriented personalization with simulated users + LLM judge | Personalized assistant evaluation is not new | Audits the judge/evaluator itself and protocol sensitivity |
| **HorizonBench** (2026) | Evolving preferences over ~6-month histories; stale-belief failures | Long-horizon evolving user state is not new | Adds confidence calibration, selective risk, action utility, and ranking reversals |
| **BeliefShift** (2026) | Temporal belief consistency, contradiction detection, evidence-driven revision | Belief update/drift is not new | Focuses on evaluation-protocol validity and action gating, not only belief revision accuracy |
| **PERMA** (2026) | Event-driven preference formation and realistic temporal tasks | Event-driven preference evolution is not new | Tests whether system selection is robust to calibration/metric/evaluator changes |
| **PerMemBench** (2026) | Personalized memory-storage policies over multi-year histories | Personalized memory policy is not new | Evaluates the downstream measurement protocol rather than proposing storage policy as the headline contribution |
| **PAHF** (2026) | Continual personalization using clarification + post-action feedback | Feedback-driven adaptation is not new | Uses transparent state estimators to isolate evaluation confounds rather than claim a new continual-learning policy |
| **π-Bench** (2026) | Proactive personal assistants with hidden intents and persistent workflows | Long-horizon proactivity is not new | Adds evaluator reliability/causal verification and protocol-sensitivity analysis |
| **OP-Bench** (2026) | Over-personalization: irrelevance, repetition, sycophancy | “Personalization can hurt” is not new | Measures when confidence/action protocols change comparative conclusions |
| **iOSWorld** (2026) | Persistent-user, cross-app personalized mobile agents | Personalized tool agents are not new | Smaller controlled environment, but deeper evaluator/calibration diagnostics |
| **BLINDSPOT** (Sep 2026) | Trajectory-level safety/refusal calibration with 22 attack families and >2,500 long-horizon trajectories | Long-horizon trajectory safety calibration and adaptive attacks are not new | PersonaMetrica does not claim novelty from trajectory attacks alone; it uses them to validate the evaluator supporting a personalization-protocol study |
| **Long-Horizon Agent Trajectory Attribution** (Aug 2026) | Fine-grained attribution and attack-chain recovery over >1,300 trajectories | Trajectory attribution/localization is not new | PersonaMetrica focuses on protocol-induced model-selection instability and grader validity rather than attribution |
| **On the Stability of Prompt Ranking** (Jun 2026) | Prompt rankings change under seeds/subsets; stability-aware selection | Ranking instability in AI evaluation is not new in general | PersonaMetrica instantiates ranking instability in long-horizon personal agents where confidence directly gates action |
| **STABLEVAL** (May 2026) | Disagreement-aware human-evaluation aggregation for stable system rankings | Ranking stability/disagreement-aware evaluation is not new in general | PersonaMetrica targets protocol/calibration/action-policy sensitivity plus evaluator OOD validity in personal agents |
| **Rank Reversal in Multilingual LLM Judges** (Aug 2026) | Judge rankings reverse across prompt languages; post-hoc calibration improves consistency | Judge rank reversal under evaluator context is not new | Supports the measurement-validity framing; PersonaMetrica studies a different mechanism: confidence/action protocols for personal agents |

## Current SOTA landscape

“SOTA” is not a single number in this area. Different benchmarks test different targets and use different model stacks. HorizonBench evaluates 25 frontier models and reports that the best reaches 52.8% on its evolving-preference benchmark. π-Bench evaluates proactivity/completeness over persistent workflows. iOSWorld evaluates cross-app personalized action. PerMemBench focuses on personalized storage policies. Therefore PersonaMetrica should **not** claim an overall state-of-the-art personal-agent score without running those official external benchmarks under comparable model settings.

This is **not an overall SOTA claim**. The project can legitimately claim **SOTA-oriented evaluation methodology** only in the descriptive sense that it incorporates current best practices: held-out splits, explicit calibration protocols, threshold-free selective-risk metrics, adversarial grader tests, causal state verification, abstention under missing evidence, evaluator fingerprints, and negative-result reporting. That is different from claiming a leaderboard SOTA result.

## Defensible novelty statement

Use this wording in paper/recruiter-facing material:

> Existing benchmarks separately study preference following, evolving user state, personalized memory, proactivity, over-personalization, and personalized tool use. PersonaMetrica studies a different failure surface: **evaluation conclusions themselves can be unstable**. It measures when system rankings change across a frozen grid of confidence calibration and action protocols, tests counterfactual state robustness, and then stress-tests the supporting grader with held-out trajectory attacks and causal verification. The contribution is an evaluation methodology for long-horizon personal agents, not a claim to be the first personalization benchmark, the first trajectory-safety benchmark, or the universally best memory system.

## Claims to avoid

Do **not** write any of the following without new external evidence:

- “first benchmark for evolving user preferences”
- “first personalized memory benchmark”
- “first proactive personal-agent benchmark”
- “state of the art personalized agent”
- “best personal memory system”
- “human-aligned personalization”
- “frontier-model improvement”
- “production-ready Personal AGI”

## What would upgrade this to a true SOTA result

1. Run the same model-backed system on **HorizonBench, PrefEval, PerMemBench, π-Bench**, and at least one interactive personalized-agent benchmark such as iOSWorld/Persona2Web where practical.
2. Compare multiple current frontier and open-weight models under a frozen protocol.
3. Collect independent human labels for grader calibration and report agreement, abstention coverage, and disagreement slices.
4. Replace structured evidence with natural-language extraction and show that the protocol-sensitivity finding survives extraction error.
5. Train on the failure-derived data and show held-out improvement without benchmark leakage.
6. Register the evaluation protocol before final external runs so grader/threshold choices cannot be tuned on test outcomes.
7. Feed real official benchmark outputs through the checked-in HorizonBench adapter and report those scores separately from PersonaMetrica's synthetic mechanism studies.

## Name audit

Candidate names were searched against current AI/agent literature and public repositories. `PersonaLens`, `BeliefShift`, `ContinuityBench`, `Calibra`, `PersonaTrace`, and `Anamnesis` are already in use. No established AI benchmark or research paper named **PersonaMetrica** was found in the current search. The name is therefore substantially cleaner for release, while normal trademark/domain due diligence would still be required before commercial use.

## Sources checked

- PrefEval — https://arxiv.org/abs/2502.09597
- PersonaLens — https://aclanthology.org/2025.findings-acl.927/
- HorizonBench — https://arxiv.org/abs/2604.17283
- BeliefShift — https://arxiv.org/abs/2603.23848
- PERMA — https://arxiv.org/abs/2603.23231
- PerMemBench — https://arxiv.org/abs/2605.25535
- PAHF — https://arxiv.org/abs/2602.16173
- π-Bench — https://arxiv.org/abs/2605.14678
- OP-Bench — https://arxiv.org/abs/2601.13722
- LongMemEval — https://arxiv.org/abs/2410.10813

- BLINDSPOT — https://arxiv.org/abs/2609.16305
- Long-Horizon Agent Trajectory Attribution — https://arxiv.org/abs/2608.06909
- On the Stability of Prompt Ranking in Large Language Model Evaluation — https://arxiv.org/abs/2606.24381
- STABLEVAL — https://arxiv.org/abs/2605.02122
- Rank Reversal in Multilingual LLM Judges — https://arxiv.org/abs/2608.22432
