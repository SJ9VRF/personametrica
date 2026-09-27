from __future__ import annotations
import hashlib, json, tomllib
from pathlib import Path
ROOT=Path('.')
EXCLUDE={'.pytest_cache','__pycache__','.git','build','.mypy_cache','.ruff_cache'}
version=tomllib.loads(Path('pyproject.toml').read_text(encoding='utf-8'))['project']['version']
rows=[]
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or any(part in EXCLUDE or part.endswith('.egg-info') for part in p.parts): continue
    if p.name=='MANIFEST.json': continue
    raw=p.read_bytes(); rows.append({'path':p.as_posix().lstrip('./'),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
Path('MANIFEST.json').write_text(json.dumps({'version':version,'files':rows},indent=2),encoding='utf-8')
print(f'MANIFEST.json v{version} ({len(rows)} files)')
