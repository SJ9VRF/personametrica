from __future__ import annotations
import json, subprocess, sys, tomllib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
# The generated page is now itself the reviewed public source of truth. Rebuild it
# from measured artifacts rather than restoring the legacy portfolio template.
subprocess.run([sys.executable,'scripts/build_project_page.py'],cwd=ROOT,check=True)
version=tomllib.loads((ROOT/'pyproject.toml').read_text(encoding='utf-8'))['project']['version']
manifest=ROOT/'project/site.webmanifest'
if manifest.exists():
    m=json.loads(manifest.read_text(encoding='utf-8'))
    m['name']='PersonaMetrica'
    m['short_name']='PersonaMetrica'
    m['description']='Evaluation science for long-horizon personal agents under calibration, protocol, and evaluator uncertainty.'
    manifest.write_text(json.dumps(m,indent=2),encoding='utf-8')
print(f'project page rebuilt from evidence-first PersonaMetrica source (v{version})')
