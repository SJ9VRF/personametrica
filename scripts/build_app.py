from __future__ import annotations
import json
from pathlib import Path

def pct(x): return f'{100*x:.1f}%'

def main():
    d=json.loads(Path('data/eval_results.json').read_text()); s=d['systems']; f=s['full_temporal_os']['metrics']; stale=s['no_temporal_update']['metrics']
    template=Path('app/index.html').read_text()
    # Replace only the benchmark values in the static demo, preserving hand-authored UI.
    import re
    template=re.sub(r'Temporal OS personalization</div><div class=metric>[^<]+',f'Temporal OS personalization</div><div class=metric>{pct(f["personalization_accuracy"])}',template)
    template=re.sub(r'First-mention baseline</div><div class=metric>[^<]+',f'First-mention baseline</div><div class=metric>{pct(stale["personalization_accuracy"])}',template)
    template=re.sub(r'Baseline stale memory</div><div class=metric>[^<]+',f'Baseline stale memory</div><div class=metric>{pct(stale["stale_memory_rate"])}',template)
    Path('app/index.html').write_text(template); print('app/index.html')
if __name__=='__main__': main()
