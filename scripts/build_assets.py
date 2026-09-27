from __future__ import annotations
import json
from pathlib import Path

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def architecture():
    boxes=[('User / World',40,40),('Interaction Gateway',40,120),('Personal World Model',40,200),('Memory + Goals + Behavior',40,280),('Proactivity Policy',40,360),('Planner + Tools',40,440),('Outcome Verifier',40,520),('Feedback + Reward',40,600),('PersonalBench + Post-training',40,680)]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="820" height="780" viewBox="0 0 820 780">','<rect width="100%" height="100%" fill="white"/>','<style>text{font-family:Arial,sans-serif;fill:#111}.title{font-size:28px;font-weight:700}.box{fill:#fff;stroke:#111;stroke-width:2;rx:12}.label{font-size:18px;font-weight:600}.arrow{stroke:#111;stroke-width:2;marker-end:url(#a)}</style>','<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="#111"/></marker></defs>','<text x="410" y="28" text-anchor="middle" class="title">PersonaMetrica — Closed-loop architecture</text>']
    for i,(label,x,y) in enumerate(boxes):
        w=310; h=52; xx=255
        svg += [f'<rect class="box" x="{xx}" y="{y}" width="{w}" height="{h}"/>',f'<text class="label" x="410" y="{y+32}" text-anchor="middle">{esc(label)}</text>']
        if i < len(boxes)-1: svg.append(f'<line class="arrow" x1="410" y1="{y+h}" x2="410" y2="{boxes[i+1][2]-8}"/>')
    svg.append('</svg>')
    Path('docs/architecture.svg').write_text('\n'.join(svg))

def results():
    data=json.loads(Path('data/eval_results.json').read_text())['systems']
    full=data['full_temporal_os']['metrics']; temporal=data['no_temporal_update']['metrics']; uncal=data['uncalibrated_proactivity']['metrics']; noverify=data['no_outcome_verification']['metrics']
    rows=[('Personalization accuracy',full['personalization_accuracy'],temporal['personalization_accuracy']),('Stale memory rate',full['stale_memory_rate'],temporal['stale_memory_rate']),('Proactivity accuracy',full['proactive_decision_accuracy'],uncal['proactive_decision_accuracy']),('Failure detection',full['failure_detection_rate'],noverify['failure_detection_rate'])]
    svg=['<svg xmlns="http://www.w3.org/2000/svg" width="980" height="520" viewBox="0 0 980 520">','<rect width="100%" height="100%" fill="white"/>','<style>text{font-family:Arial,sans-serif;fill:#111}.title{font-size:28px;font-weight:700}.label{font-size:17px}.small{font-size:14px}.axis{stroke:#777;stroke-width:1}</style>','<text x="490" y="38" text-anchor="middle" class="title">Controlled benchmark: full system vs targeted ablation</text>']
    y=105
    for label,a,b in rows:
        svg += [f'<text x="30" y="{y+18}" class="label">{esc(label)}</text>',f'<rect x="300" y="{y}" width="{560*a:.1f}" height="20" fill="#222"/>',f'<rect x="300" y="{y+28}" width="{560*b:.1f}" height="20" fill="#aaa"/>',f'<text x="870" y="{y+16}" class="small">Full {a:.3f}</text>',f'<text x="870" y="{y+44}" class="small">Abl. {b:.3f}</text>']
        y += 95
    svg += ['<text x="300" y="495" class="small">Dark = full system; light = targeted ablation. Synthetic controlled benchmark only.</text>','</svg>']
    Path('docs/results.svg').write_text('\n'.join(svg))

if __name__=='__main__':
    Path('docs').mkdir(exist_ok=True)
    architecture(); results(); print('docs/architecture.svg'); print('docs/results.svg')
