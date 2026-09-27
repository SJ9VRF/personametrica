from __future__ import annotations
import hashlib, json, platform
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=[
    ROOT/'personalbench/agent_evals/models.py',
    ROOT/'personalbench/agent_evals/graders.py',
    ROOT/'personalbench/agent_evals/suite.py',
    ROOT/'personalbench/agent_evals/reliability.py',
]
h=hashlib.sha256()
entries=[]
for p in files:
    b=p.read_bytes(); digest=hashlib.sha256(b).hexdigest(); h.update(p.name.encode()+b'\0'+b)
    entries.append({'path':str(p.relative_to(ROOT)),'sha256':digest,'bytes':len(b)})
out={'schema_version':'1.0','grader_bundle_sha256':h.hexdigest(),'python':platform.python_version(),'files':entries}
(ROOT/'data'/'grader_fingerprint.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
(ROOT/'reports'/'GRADER_FINGERPRINT.md').write_text('# Grader fingerprint\n\nThe checked-in agent-evaluation results are bound to a content hash of the grader/task implementation. Any evaluator code change changes this fingerprint and requires regenerated results.\n\n- Bundle SHA-256: `'+out['grader_bundle_sha256']+'`\n- Schema version: `1.0`\n- Python: `'+out['python']+'`\n',encoding='utf-8')
print(json.dumps(out,indent=2))
