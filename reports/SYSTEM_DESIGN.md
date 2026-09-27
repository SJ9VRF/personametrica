# System Design — PersonaMetrica

## Objectives

The system is designed for inspectable longitudinal personalization. Its core engineering requirements are deterministic replay, explicit temporal semantics, modular ablations, safe side-effect-free tool execution, observable decisions, and evaluability without proprietary infrastructure.

## Event layer

Every user message enters as an `InteractionEvent` with user/session IDs, timestamp, context, detected state updates, tool calls, outcomes, and feedback fields. Events are retained so state can be audited against their source.

## Personal world model

Memory records contain a semantic key, value, raw content, source type, confidence, stability, validity interval, context, supersession link, contradiction links, and status. Canonical keys allow preference reversals to update the same latent slot instead of creating unrelated text fragments.

Three update semantics are supported for controlled experiments:

- `latest`: current value supersedes older active values;
- `first`: first value remains active, creating a stale-memory baseline;
- `all`: conflicting observations remain active, creating a contradiction baseline.

Retrieval combines lexical relevance, recency, confidence, and contradiction risk. Confidence decay is stability-dependent.

## Goal model

Explicit goal language is converted into structured `Goal` objects with status, priority, deadline, progress, parent linkage, subtasks, blockers, and dependencies. Deterministic decomposition provides a local fallback without external models. Completion and abandonment messages are matched against active goals so longitudinal evaluation covers lifecycle rather than capture alone.

## Proactivity

The calibrated policy receives goal relevance, urgency, confidence, stakes, reversibility, autonomy preference, historical acceptance, and interruptibility. It applies explicit gates for low-value contexts, uncertainty, and high-stakes irreversible actions before considering lower-risk suggestion/reminder thresholds.

The system exposes structured factors and the selected action. It does not expose hidden chain-of-thought.

## Planning and tools

`HierarchicalPlanner` produces explicit plan steps. `SandboxTools` implements notes, tasks, and reminders entirely in memory so evaluation never creates external side effects. This makes action tests deterministic and safe.

## Outcome verification

Action success is separated from tool-call success. `OutcomeVerifier` compares expected state with observed state and emits discrepancies. Evaluation injects controlled mismatches to measure failure detection.

## Feedback and reward

Feedback is represented by typed categories such as useful, wrong memory, wrong assumption, too proactive, and outdated preference. `MultiObjectiveRewardModel` produces an auditable reward vector rather than hiding tradeoffs in one scalar. It is explicitly a deterministic research substitute, not a learned reward model.

## Evaluation architecture

PersonalBench has four layers:

1. deterministic persona simulation;
2. scenario generation for proactivity/autonomy;
3. mechanism metrics and bootstrap confidence intervals;
4. feature-toggle ablations executed through the production agent class.

## Reproducibility

Randomness is seeded at persona/scenario construction. Background simulator utterances use a per-person/per-turn deterministic PRNG. `scripts/reproduce.py` regenerates all primary artifacts in a fixed order and fails immediately if any stage fails.

## Production extensions

The boundaries are intentionally injectable. A production implementation could replace the rule extractor, memory backend, planner, policy, tools, or reward model while retaining the same schemas and evaluation harness. Persistence, authentication, encryption, rate limiting, distributed execution, and external-tool permission systems are outside the current local-research scope.


## Snapshot persistence
`personalagi.persistence` provides schema-versioned JSON snapshots for cross-session restoration. The snapshot contains user beliefs, active and superseded memory history, goals, interaction-style parameters, and provenance. Restore validates schema version and user identity before mutating state. This is intentionally local and transparent; production storage, encryption, retention, and access-control policies remain outside the scope of this repository.


## Privacy, user control, and auditability
A conservative `PrivacyGuard` blocks obvious credential, financial, and government-ID phrases from persistent memory while leaving ordinary preferences unaffected. It is deliberately narrow and does not claim production PII coverage. Explicit forgetting marks the active record deleted, excludes it from retrieval, and emits an audit event. Memory write, supersession, expiration, and forgetting are inspectable lifecycle events.

## Persistence v2
Schema v2 snapshots restore beliefs, complete temporal memory history, goals, interaction style, interaction events, structured feedback, memory audit events, and deterministic sandbox tool state. Schema v1 remains readable for backward compatibility. User-ID mismatch and unknown schema versions fail closed.

## Adversarial language stress
The benchmark includes a separate pattern-shift suite containing hedges, within-utterance reversals, elliptical multi-turn updates, conditional preferences, likes, and dislikes. It is intentionally distinct from the main persona simulator so parsing quality is not inferred solely from template-matched data.
