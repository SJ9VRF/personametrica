from __future__ import annotations
from dataclasses import dataclass, field
import random

@dataclass
class UserPersona:
    user_id: str
    work_time: str = 'evening'
    response_detail: str = 'concise'
    autonomy: float = .5
    drift_at: int | None = 20
    drift_to: str = 'morning'
    conditional_detail: dict[str, str] = field(default_factory=lambda: {'technical': 'detailed'})
    seed: int = 0

    def utterance(self, turn: int) -> str:
        if turn == 0:
            return f'I prefer working in the {self.work_time}.'
        if turn == 1:
            return f'I prefer {self.response_detail} answers.'
        if turn == 2:
            return 'My goal is finish my conference talk by Friday.'
        if self.drift_at is not None and turn == self.drift_at:
            self.work_time = self.drift_to
            return f'Actually, {self.work_time}s work better for me now.'
        if turn % 11 == 0:
            return 'For technical topics, give me more detail.'
        # Per-person, per-turn deterministic background interaction.
        r = random.Random(self.seed * 10007 + turn)
        return r.choice([
            'Help me make progress on my talk.',
            'What should I do next?',
            "Keep me on track, but don't nag me.",
            'I made some progress today.',
            'Do not interrupt me unless it is important.',
            'Remind me when a deadline is close.',
        ])


def generate_personas(n: int, seed: int = 7) -> list[UserPersona]:
    r = random.Random(seed)
    out = []
    for i in range(n):
        wt = r.choice(['morning', 'evening'])
        out.append(UserPersona(
            user_id=f'u{i:04d}', work_time=wt,
            response_detail=r.choice(['concise', 'detailed']),
            autonomy=r.random(), drift_at=r.choice([8, 10, 20, 40, None]),
            drift_to='evening' if wt == 'morning' else 'morning', seed=seed * 1000 + i,
        ))
    return out
