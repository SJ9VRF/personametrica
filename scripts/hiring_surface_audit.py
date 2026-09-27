from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION='4.2.0'
public=['README.md','docs/HIRING_MANAGER_README.md','project/index.html','CITATION.cff','pyproject.toml']
texts={p:(ROOT/p).read_text(encoding='utf-8') for p in public}
checks={
 'public_name_aura_yavary': all('Aura Yavary' in texts[p] for p in ['README.md','docs/HIRING_MANAGER_README.md','project/index.html']),
 'current_version_on_public_surfaces': all(VERSION in texts[p] for p in public),
 'homepage_has_claim_boundary': 'not a frontier-model' in texts['project/index.html'].lower(),
 'homepage_links_fast_reviewer_demo': 'REVIEWER_DEMO.md' in texts['project/index.html'],
 'hiring_readme_keeps_known_failures': 'Known failures kept visible' in texts['docs/HIRING_MANAGER_README.md'],
 'readme_links_reviewer_demo': 'REVIEWER_DEMO.md' in texts['README.md'],
 'readme_links_cold_start_audit': 'COLD_START_AUDIT.md' in texts['README.md'],
 'no_placeholder_tokens_on_public_surfaces': not any(re.search(r'REPLACE_WITH|TODO|TBD',t,re.I) for t in texts.values()),
}
if not all(checks.values()): raise SystemExit('Hiring-surface audit failed: '+', '.join(k for k,v in checks.items() if not v))
out={'version':VERSION,'status':'PASS','checks':checks,'surfaces':public}
(ROOT/'data/hiring_surface_audit.json').write_text(json.dumps(out,indent=2)+'\n')
(ROOT/'reports/HIRING_SURFACE_AUDIT.md').write_text('# Hiring-surface audit\n\n**Status: PASS**\n\n'+''.join(f'- {k}: PASS\n' for k in checks)+'\nThis audit checks presentation consistency only; it does not substitute for scientific validation.\n')
print(json.dumps(out,indent=2))
