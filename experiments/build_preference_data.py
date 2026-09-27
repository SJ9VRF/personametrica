from __future__ import annotations
import random, sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))

from personalagi.training import TrainingDataPipeline
from personalbench.tasks.scenarios import generate_proactivity_scenarios

rng = random.Random(23)
pipe = TrainingDataPipeline()
rows: list[dict] = []

temporal_templates = [
    ('The user first preferred {old}, then explicitly updated the preference to {new}. What should the assistant use now?',
     'Use {new} as the current preference and keep {old} only as superseded history.',
     'Keep using {old} because it appeared earlier.'),
    ('Earlier the user said {old}; later they said {new} works better. Which state should guide the response?',
     'Use the later explicit preference, {new}, while preserving provenance for the old state.',
     'Use the older {old} state because it has existed longer.'),
    ('A user changed from {old} to {new}. How should long-term memory behave?',
     'Mark {old} superseded and retrieve {new} for current decisions.',
     'Store both as equally active and choose {old} first.'),
    ('Memory contains an old {old} preference and a newer explicit {new} preference. What is correct?',
     'Prefer temporally valid {new}; retain {old} only for history.',
     'Prefer {old} because first-written memories are more stable.'),
]
for i in range(320):
    old, new = rng.choice([('morning work', 'evening work'), ('evening work', 'morning work'),
                           ('short answers', 'detailed technical answers'), ('window seats', 'aisle seats')])
    tid = i % len(temporal_templates)
    p, c, r = temporal_templates[tid]
    rows.append(pipe.preference_pair(
        p.format(old=old, new=new), c.format(old=old, new=new), r.format(old=old, new=new),
        reason='prefer current temporally valid memory over stale memory',
        metadata={'family': 'temporal_memory', 'template_id': f'temporal_{tid}', 'group': i % 16}
    ))

privacy_templates = [
    ('The user asks the assistant to forget a stored preference about {topic}. What should happen?',
     'Delete the active memory, preserve only the audit event, and do not re-learn the forget command itself.',
     'Delete it and then immediately recreate the same memory from the forget command text.'),
    ('A user explicitly says “do not remember my {topic}”. What is the correct memory action?',
     'Do not persist the sensitive content; record only that a forget/privacy action occurred.',
     'Persist the content anyway so future personalization is richer.'),
]
for i in range(160):
    topic = rng.choice(['password', 'private note', 'home access code', 'temporary preference'])
    tid = i % len(privacy_templates)
    p, c, r = privacy_templates[tid]
    rows.append(pipe.preference_pair(
        p.format(topic=topic), c.format(topic=topic), r.format(topic=topic),
        reason='respect explicit memory control and privacy boundaries',
        metadata={'family': 'privacy_control', 'template_id': f'privacy_{tid}', 'group': i % 16}
    ))

for i, s in enumerate(generate_proactivity_scenarios(700, 23)):
    high_risk = s['stakes'] >= .8 and s['reversibility'] <= .3
    uncertain = s['confidence'] < .5
    low_value = s['goal_relevance'] < .25 and s['urgency'] < .25
    if high_risk:
        chosen = 'Ask for confirmation before any consequential action.'
        rejected = 'Take the high-stakes irreversible action immediately.'
        reason = 'require confirmation for high-stakes irreversible actions'
        family = 'high_stakes_autonomy'
    elif uncertain:
        chosen = 'Ask a clarifying question before committing to an action.'
        rejected = 'Act immediately despite low confidence in the user intent.'
        reason = 'calibrate action to uncertainty'
        family = 'uncertainty_calibration'
    elif low_value:
        chosen = 'Do not interrupt; wait until the opportunity is more relevant or urgent.'
        rejected = 'Interrupt the user now with a low-value proactive suggestion.'
        reason = 'avoid low-value proactive interruptions'
        family = 'low_value_proactivity'
    else:
        chosen = 'Offer a reversible suggestion or reminder without silently taking consequential action.'
        rejected = 'Silently take a consequential action on the user’s behalf.'
        reason = 'prefer reversible assistance over autonomous overreach'
        family = 'reversible_assistance'
    prompt = (
        f"Context: goal relevance {s['goal_relevance']:.2f}; urgency {s['urgency']:.2f}; "
        f"confidence {s['confidence']:.2f}; stakes {s['stakes']:.2f}; reversibility {s['reversibility']:.2f}. "
        'What should the personal agent do?'
    )
    rows.append(pipe.preference_pair(
        prompt, chosen, rejected, reason=reason,
        metadata={'family': family, 'template_id': f'proactivity_{i % 7}', 'group': i % 20}
    ))

rows, removed = pipe.deduplicate(rows)
rng.shuffle(rows)
pipe.export_jsonl(rows, 'data/preference_pairs.jsonl')
print(f'data/preference_pairs.jsonl ({len(rows)} unique pairs; {removed} duplicates removed)')
