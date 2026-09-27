from __future__ import annotations
import sys
from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parents[1]))
import json, html
from pathlib import Path

GOOD_HIGH={'personalization_accuracy','goal_capture_rate','proactive_decision_accuracy','failure_detection_rate','high_stakes_confirmation_rate','low_confidence_clarification_rate','low_value_noninterrupt_rate'}
GOOD_LOW={'stale_memory_rate','contradiction_rate','autonomy_violation_rate','verification_false_alarm_rate','memory_confidence_brier'}

def pct(x): return f'{x*100:.1f}%'

def main():
    p=Path('data/eval_results.json'); data=json.loads(p.read_text()) if p.exists() else {'systems':{},'benchmark':{}}
    systems=data.get('systems',{}); bench=data.get('benchmark',{})
    full=systems.get('full_temporal_os',{}).get('metrics',{})
    focus=['personalization_accuracy','stale_memory_rate','contradiction_rate','proactive_decision_accuracy','autonomy_violation_rate','failure_detection_rate','memory_confidence_brier']
    rows=[]
    for name,row in systems.items():
        cells=''.join(f'<td>{pct(row["metrics"].get(k,0))}</td>' for k in focus)
        rows.append(f'<tr><th>{html.escape(name.replace("_"," ").title())}</th>{cells}</tr>')
    cards=''.join(f'<div class="card"><span>{html.escape(k.replace("_"," ").title())}</span><strong>{pct(v)}</strong></div>' for k,v in full.items() if k in set(focus))
    bars=[]
    for name,row in systems.items():
        v=row['metrics']['personalization_accuracy']; bars.append(f'<div class="barrow"><label>{html.escape(name.replace("_"," "))}</label><div class="track"><i style="width:{v*100:.1f}%"></i></div><b>{pct(v)}</b></div>')
    page=f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PersonaMetrica — Research Dashboard</title><style>
    :root{{--bg:#07090d;--panel:#10141b;--line:#262c37;--muted:#9ba5b5}}*{{box-sizing:border-box}}body{{font-family:Inter,ui-sans-serif,system-ui;background:var(--bg);color:#f7f8fa;margin:0}}main{{max-width:1280px;margin:auto;padding:44px 28px 70px}}h1{{font-size:52px;letter-spacing:-2px;margin:0}}.sub{{color:var(--muted);max-width:760px;line-height:1.6}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:28px 0}}.card{{border:1px solid var(--line);background:var(--panel);border-radius:18px;padding:18px}}.card span{{display:block;color:var(--muted);font-size:13px}}.card strong{{font-size:30px;display:block;margin-top:8px}}section{{margin-top:42px}}table{{width:100%;border-collapse:collapse;overflow:hidden;border-radius:14px}}th,td{{padding:12px;border-bottom:1px solid var(--line);text-align:right;font-size:13px}}th:first-child{{text-align:left}}thead th{{color:var(--muted)}}.barrow{{display:grid;grid-template-columns:220px 1fr 65px;align-items:center;gap:12px;margin:11px 0}}.barrow label{{font-size:13px;color:#d8dde7}}.track{{height:11px;background:#1b2029;border-radius:99px;overflow:hidden}}.track i{{height:100%;display:block;background:#f5f7fa}}.barrow b{{text-align:right}}code{{background:#151923;padding:3px 7px;border-radius:6px}}@media(max-width:700px){{.barrow{{grid-template-columns:1fr}}table{{font-size:11px;display:block;overflow-x:auto}}h1{{font-size:39px}}}}
    </style></head><body><main><h1>PersonaMetrica</h1><p class="sub">Reproducible synthetic research dashboard. {bench.get('users','?')} users × {bench.get('turns','?')} turns; {bench.get('proactivity_scenarios','?')} proactivity scenarios. These results validate mechanisms in a controlled substrate and are not human/frontier-model claims.</p><div class="grid">{cards}</div><section><h2>Personalization under ablation</h2>{''.join(bars)}</section><section><h2>System comparison</h2><table><thead><tr><th>System</th>{''.join(f'<th>{html.escape(k.replace("_"," ").title())}</th>' for k in focus)}</tr></thead><tbody>{''.join(rows)}</tbody></table></section><section><h2>Reproduce</h2><p class="sub"><code>python scripts/reproduce.py</code> regenerates tests, data, benchmark, ablations, preference pairs, this dashboard, and the result summary.</p></section></main></body></html>'''
    out=Path('dashboard/index.html'); out.write_text(page); print(out)
if __name__=='__main__': main()
