from __future__ import annotations
import json
from pathlib import Path


class TrainingDataPipeline:
    """Turns failures/feedback into auditable preference data without requiring GPU training."""
    REQUIRED = {'prompt', 'chosen', 'rejected', 'reason', 'user_id'}

    def preference_pair(self, prompt: str, chosen: str, rejected: str, *, reason: str,
                        user_id: str = 'synthetic', metadata: dict | None = None) -> dict:
        row = {'prompt': prompt, 'chosen': chosen, 'rejected': rejected, 'reason': reason, 'user_id': user_id}
        if metadata:
            row['metadata'] = metadata
        return row

    def validate(self, row: dict) -> None:
        missing = self.REQUIRED - set(row)
        if missing:
            raise ValueError(f'missing preference-pair fields: {sorted(missing)}')
        for k in ('prompt', 'chosen', 'rejected', 'reason', 'user_id'):
            if not isinstance(row[k], str) or not row[k].strip():
                raise ValueError(f'{k} must be a non-empty string')
        if row['chosen'].strip() == row['rejected'].strip():
            raise ValueError('chosen and rejected must differ')

    @staticmethod
    def fingerprint(row: dict) -> tuple[str, str, str]:
        norm = lambda s: ' '.join(s.lower().split())
        return norm(row['prompt']), norm(row['chosen']), norm(row['rejected'])

    def deduplicate(self, rows: list[dict]) -> tuple[list[dict], int]:
        seen = set(); out = []
        for row in rows:
            self.validate(row)
            fp = self.fingerprint(row)
            if fp in seen:
                continue
            seen.add(fp); out.append(row)
        return out, len(rows) - len(out)

    def export_jsonl(self, rows: list[dict], path: str | Path) -> Path:
        p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('w', encoding='utf-8') as f:
            for row in rows:
                self.validate(row)
                f.write(json.dumps(row, ensure_ascii=False) + '\n')
        return p
