from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'configs'/'protocol_registry.json'
raw=path.read_bytes()
out={
  'registry_path':'configs/protocol_registry.json',
  'sha256':hashlib.sha256(raw).hexdigest(),
  'release':json.loads(raw.decode('utf-8'))['release'],
  'status':'frozen-release-protocol',
  'note':'This is a repository-level protocol lock, not an externally timestamped preregistration.'
}
(ROOT/'data'/'protocol_registry_fingerprint.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
