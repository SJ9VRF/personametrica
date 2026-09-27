# Related-work positioning

The submission should not be positioned as “another memory system.” Its strongest distinction is an evaluation claim: **state correctness and action quality are not interchangeable objectives for personal agents**.

| Work | Primary question | Scale / evidence emphasized | What PersonaMetrica-Bench adds |
|---|---|---|---|
| LongMemEval (ICLR 2025) | Can assistants retrieve/reason over long-term interactive memory? | 500 curated questions; extraction, multi-session reasoning, temporal reasoning, updates, abstention | Couples state belief to action coverage, selective risk, and calibrated downstream utility |
| PrefEval (ICLR 2025 Oral) | Do LLMs infer/remember/follow explicit and implicit preferences? | 3,000 curated preference/query pairs; 10 open/proprietary models; prompting/RAG/SFT | Focuses on evolving evidence and whether confidence should permit action |
| HorizonBench (2026) | Can models track preferences that evolve over six-month histories? | 4,245 items, 360 users, ~4,300 turns/user, 25 frontier models | Complementary metric thesis: current-state accuracy can still mis-rank action substrates |
| PerMemBench (2026) | What should personalized memory systems store? | Multi-year/multi-domain histories; personalized storage gating | Studies belief competition after evidence is available; write policy remains external future work |
| Proactive Agent / ProactiveBench (ICLR 2025) | When should an agent proactively offer help? | 6,790 events, human accept/reject labels, learned reward model | Connects uncertainty in evolving personal state to whether the agent should act or defer |
| UserVille / PPP (2025) | Can RL jointly improve productivity, proactivity, personalization? | LLM user simulators; multi-objective RL on agent tasks | Provides state-estimation/evaluation substrate; does not claim to replace PPP training evidence |
| MemoryBank (AAAI 2024) | Can long-term memory improve persistent assistants? | Long-term memory + forgetting curve + simulated/real dialogue analysis | Uses explicit provenance/source/scope competition and risk-aware readout |
| Generative Agents (UIST 2023) | How can memory/reflection/planning support believable agents? | Interactive simulation with memory, reflection, planning | Narrower personal-assistant evaluation with calibrated state/action metrics |

## Defensible novelty statement

> Prior work has established that long-context assistants forget preferences, fail to update evolving user state, and benefit from retrieval, storage policies, or fine-tuning. PersonaMetrica-Bench studies a different failure surface: even when a memory system has high current-state accuracy, it can be a worse substrate for action if its confidence does not track correctness. We therefore evaluate personalization as **belief updating plus risk-sensitive decision-making**, using risk–coverage, calibration, and decision utility in addition to state accuracy.

## Claims not to make

- “First benchmark for evolving preferences” — HorizonBench and PERMA already study evolving preferences.
- “First personalized memory policy” — PerMemBench studies personalized storage gating.
- “First proactive personalization benchmark” — PrefEval, ProactiveBench, and UserVille cover important parts of this space.
- “Frontier-model improvement” — not until external model outputs are actually collected.
- “Human-aligned proactivity” — not until the annotation study is executed.

## September 2026 re-audit: what is no longer a novelty claim

Recent work further narrows the claim boundary. **BLINDSPOT** studies trajectory-level safety/refusal calibration over 22 attack families and more than 2,500 long-horizon trajectories; **Long-Horizon Agent Trajectory Attribution** studies fine-grained trajectory attribution and attack-chain recovery; **On the Stability of Prompt Ranking** studies rank instability under seeds/subsets; **STABLEVAL** studies disagreement-aware stable system ranking; and **Rank Reversal in Multilingual LLM Judges** demonstrates evaluator-backbone rank reversals across prompt languages.

PersonaMetrica therefore does **not** claim novelty from any of these ingredients in isolation: long-horizon attacks, trajectory analysis, ranking instability, disagreement-aware evaluation, or evaluator calibration. The narrower contribution is their joint application to a distinct measurement problem in **evolving personal agents**: user-state confidence gates action, calibration changes coverage, operating-point costs affect utility, and the supporting grader can itself fail under distribution shift.

The v3.8 protocol audit makes this concrete at the **whole-leaderboard** level. Across 75 frozen protocol cells, time-aware-latest wins 45, PBS 27, and first-mention 3. Two randomly chosen protocol cells select different winners with probability 0.516; mean complete-ranking Kendall tau is 0.699 and the most discordant pair falls to 0.20. These are synthetic mechanism diagnostics, not population estimates or external leaderboard claims.
