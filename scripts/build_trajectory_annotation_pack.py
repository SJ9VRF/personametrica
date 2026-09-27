from __future__ import annotations
import html, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
rows=[json.loads(x) for x in (ROOT/'data'/'grader_disagreement_queue.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
# Blind gold and internal grader verdicts for annotation.
tasks=[]
for r in rows[:240]:
    tasks.append({'review_id':r['review_id'],'task_id':r['task_id'],'task':r['task'],'trajectory':r['trajectory']})
outdir=ROOT/'annotation'/'trajectory_grading'; outdir.mkdir(parents=True,exist_ok=True)
(outdir/'tasks.json').write_text(json.dumps(tasks,indent=2),encoding='utf-8')
html_doc='''<!doctype html><meta charset="utf-8"><title>Trajectory grading calibration</title>
<style>body{font:16px/1.5 system-ui;max-width:1000px;margin:40px auto;padding:0 20px}pre{white-space:pre-wrap;background:#f5f5f5;padding:16px}.card{border:1px solid #ddd;padding:20px;margin:18px 0}button{margin-right:8px;padding:8px 12px}</style>
<h1>Trajectory grading calibration</h1><p>Judge whether the trajectory satisfies the task and policy. Use <b>Unknown</b> if the trace lacks enough evidence.</p><div id="app"></div>
<script>
fetch('tasks.json').then(r=>r.json()).then(tasks=>{let i=0, answers=[]; const app=document.querySelector('#app');
function render(){let t=tasks[i]; if(!t){app.innerHTML='<h2>Complete</h2><pre>'+JSON.stringify(answers,null,2)+'</pre>';return;} app.innerHTML=`<div class=card><b>${t.review_id}</b><h3>Task</h3><pre>${escapeHtml(JSON.stringify(t.task,null,2))}</pre><h3>Trajectory</h3><pre>${escapeHtml(JSON.stringify(t.trajectory,null,2))}</pre><button onclick="ans('pass')">Pass</button><button onclick="ans('fail')">Fail</button><button onclick="ans('unknown')">Unknown</button></div>`}
window.ans=v=>{answers.push({review_id:tasks[i].review_id,verdict:v});i++;render()}; window.escapeHtml=s=>s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); render();});
</script>'''
(outdir/'index.html').write_text(html_doc,encoding='utf-8')
(outdir/'README.md').write_text('# Trajectory grader calibration pack\n\nBlinded disagreement cases for independent human calibration. Gold labels and grader outputs are intentionally excluded from `tasks.json`. Export reviewer answers and score them with `scripts/score_trajectory_annotations.py`.\n',encoding='utf-8')
print(json.dumps({'tasks':len(tasks),'path':str(outdir.relative_to(ROOT))},indent=2))
