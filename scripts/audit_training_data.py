from __future__ import annotations
import json, math, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from personalagi.training import TrainingDataPipeline

path = ROOT / 'data/preference_pairs.jsonl'
rows = [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines() if x.strip()]
pipe = TrainingDataPipeline()
valid = 0; fps = Counter(); families = Counter(); templates = Counter(); reasons = Counter()
for row in rows:
    pipe.validate(row); valid += 1
    fps[pipe.fingerprint(row)] += 1
    md = row.get('metadata', {})
    families[md.get('family', 'unknown')] += 1
    templates[md.get('template_id', 'unknown')] += 1
    reasons[row['reason']] += 1

def entropy(counter: Counter) -> float:
    n = sum(counter.values())
    return 0.0 if not n else -sum((c/n)*math.log2(c/n) for c in counter.values())

report = {
    'rows': len(rows), 'valid_rows': valid,
    'exact_duplicate_rows': sum(c-1 for c in fps.values() if c > 1),
    'unique_pairs': len(fps), 'families': dict(sorted(families.items())),
    'template_count': len(templates), 'reason_count': len(reasons),
    'family_entropy_bits': round(entropy(families), 4),
    'template_entropy_bits': round(entropy(templates), 4),
}
(ROOT/'data/training_data_audit.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
lines = ['# Training Data Audit', '', f"- Rows: **{report['rows']}**",
         f"- Valid rows: **{report['valid_rows']}**", f"- Exact duplicate rows: **{report['exact_duplicate_rows']}**",
         f"- Unique pairs: **{report['unique_pairs']}**", f"- Families: **{len(families)}**",
         f"- Templates: **{report['template_count']}**", '', '## Family distribution', '']
for k,v in sorted(families.items()): lines.append(f'- `{k}`: {v}')
lines += ['', '## Scope', '', 'This audit checks schema validity, exact duplicate leakage, and coarse diversity. It does not establish human-label quality or frontier-model preference validity.']
(ROOT/'reports/TRAINING_DATA_AUDIT.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(json.dumps(report, indent=2))
