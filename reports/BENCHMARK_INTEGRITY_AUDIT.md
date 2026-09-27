# PersonaMetrica-Bench integrity audit

Standard generator: 500 users × 240 turns; 27,133 observations; 13,500 queries.

- Deterministic replay: **True**
- Users with queries: **500/500**
- Exact structured observation fingerprint duplicates across users: **13,712** (expected because the benchmark is generated from a finite structured schema; user histories/sequences differ).

## Evidence-source counts

- `explicit`: 8,123
- `implicit_behavior`: 6,660
- `hypothetical`: 5,933
- `other_person`: 5,792
- `implicit_choice`: 625

## Query contexts

- `general`: 13,356
- `temporary`: 144

## Audit boundary

This audit checks generator determinism, coverage, and structured duplication. It does **not** establish natural-language novelty because PersonaMetrica-Bench v3.x begins after evidence extraction.
