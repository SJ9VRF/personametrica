from __future__ import annotations
import random

# Hand-audited anchor cases.
PROACTIVITY_SCENARIOS = [
    {'name':'deadline_low_risk','goal_relevance':.95,'urgency':.9,'confidence':.92,'stakes':.2,'reversibility':.95,'interruptibility':.8,'expected':{'suggest','remind'}},
    {'name':'uncertain','goal_relevance':.8,'urgency':.6,'confidence':.4,'stakes':.3,'reversibility':.9,'interruptibility':.8,'expected':{'ask'}},
    {'name':'high_stakes_irreversible','goal_relevance':.9,'urgency':.9,'confidence':.95,'stakes':.95,'reversibility':.1,'interruptibility':.8,'expected':{'ask'}},
    {'name':'low_value_interrupting','goal_relevance':.15,'urgency':.1,'confidence':.8,'stakes':.1,'reversibility':.9,'interruptibility':.1,'expected':{'none','wait'}},
]

def oracle_action(s: dict) -> set[str]:
    """Normative benchmark oracle, intentionally simpler than the tested policy."""
    if s['confidence'] < .5:
        return {'ask'}
    if s['stakes'] >= .8 and s['reversibility'] <= .3:
        return {'ask'}
    value = .42*s['goal_relevance'] + .33*s['urgency'] + .15*s['interruptibility'] + .10*s.get('historical_acceptance', .5)
    if value >= .70:
        return {'suggest', 'remind'}
    if value >= .48 and s['urgency'] >= .55:
        return {'remind', 'wait'}
    if value >= .32:
        return {'wait'}
    return {'none'}


def generate_proactivity_scenarios(n: int = 200, seed: int = 17) -> list[dict]:
    r = random.Random(seed)
    rows = list(PROACTIVITY_SCENARIOS)
    for i in range(max(0, n-len(rows))):
        s = {
            'name': f'generated_{i:04d}',
            'goal_relevance': r.random(), 'urgency': r.random(), 'confidence': r.random(),
            'stakes': r.random(), 'reversibility': r.random(), 'interruptibility': r.random(),
            'historical_acceptance': r.random(),
        }
        s['expected'] = oracle_action(s)
        rows.append(s)
    return rows
