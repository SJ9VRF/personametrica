# Dataset Card — PersonalBench Synthetic Longitudinal Data

## Summary

`data/personalbench.jsonl` contains deterministic synthetic longitudinal interactions generated for mechanism-level evaluation of temporal personalization. The default checked-in generation is 100 users × 60 turns = 6,000 rows.

## Fields

Each row contains `user_id`, turn index, message, and ground-truth state including current work-time preference, response-detail preference, and simulated autonomy tendency.

## Generation

Profiles are generated from a fixed seed. Users receive an initial work-time preference, answer-detail preference, an explicit goal, optional preference drift, conditional technical-detail statements, and background productivity utterances. Drift timing varies across profiles.

## Intended uses

- regression tests for temporal state update;
- stale-memory evaluation;
- contradiction-resolution evaluation;
- controlled benchmark development;
- training-data prototyping.

## Non-intended uses

The data must not be used to infer demographic behavior, estimate real user preferences, claim population representativeness, or support conclusions about frontier-model personalization.

## Limitations

Language variety is intentionally narrow and current state extraction is rule-based. Synthetic personas do not capture real interpersonal complexity, ambiguity, privacy preferences, or long-term behavioral change.
