# PersonaMetrica — reviewer demo

**Status: PASS**

This is the shortest executable path through the repository. It validates checked-in evidence and also runs two live mechanisms: the held-out causal grader suite and a temporal-preference update.

## What it verifies

- **75 protocol cells:** winners = time-aware-latest 45, personal-belief-state 27, first-mention 3.
- **Winner-change probability:** 51.6%; complete-ranking mean Kendall tau = 0.699, minimum = 0.20.
- **Seed-bootstrap support:** winner-change 95% interval = [0.507, 0.538].
- **Grid robustness:** all 13 leave-one-level-out variants retain multiple winners.
- **Held-out grader attacks, rerun live:** frozen robust grader false-accept = 96.0%; causal grader = 0.0%.
- **Counterfactual personalization:** PBS nuisance invariance = 98.0% (kept imperfect on purpose).
- **Benchmark health:** split identity overlap, full-history overlap, and standard full-history duplicates are all zero.
- **Protocol lock:** registry SHA-256 matches the frozen fingerprint.
- **Live runtime:** an explicit evening→morning preference update leaves `morning` active.

## Boundaries

- Controlled synthetic mechanism study; not a frontier-model leaderboard claim.
- Bootstrap interval quantifies simulator-seed variation, not human-population uncertainty.
- Held-out grader attacks are authored synthetic attacks, not production trajectories.

Run with:

```bash
python scripts/reviewer_demo.py
```
