from __future__ import annotations
import json, textwrap, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'project'/'assets'; OUT.mkdir(parents=True,exist_ok=True)
TMP=OUT/'video_frames'; shutil.rmtree(TMP,ignore_errors=True); TMP.mkdir()
W,H=1280,720
bg=(11,13,16); fg=(244,245,247); muted=(170,179,191); accent=(200,255,99); panel=(23,28,34)
font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold_path='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
F1=ImageFont.truetype(bold_path,62); F2=ImageFont.truetype(bold_path,34); FB=ImageFont.truetype(font_path,25); FS=ImageFont.truetype(font_path,20); FM=ImageFont.truetype(bold_path,18)
summary=json.loads((ROOT/'data/release_summary.json').read_text()); fail=json.loads((ROOT/'data/failure_analysis.json').read_text()); scale=json.loads((ROOT/'data/scaling_results.json').read_text())
slides=[
 ('PersonaMetrica','An evolving assistant that learns, remembers, decides when to act, verifies outcomes, and improves from feedback.','Aura Yavary · Flagship 7 · 2026'),
 ('The research question','Can personal intelligence improve over time without increasing stale memory, intrusive proactivity, autonomy violations, or unverified actions?','Longitudinal intelligence under behavioral constraints'),
 ('Learn → update → remember','Temporal user state tracks confidence, provenance, supersession, conditional preferences, explicit forgetting, and cross-session persistence.','100 synthetic users × 60 turns in the checked-in main benchmark'),
 ('Decide when to intervene','A calibrated policy chooses act / ask / suggest / remind / wait / none from urgency, confidence, stakes, reversibility, and user autonomy.','86.5% decision accuracy · 0% autonomy violation in the controlled benchmark'),
 ('Verify the world','Tool actions are not assumed successful. Expected outcomes are compared with observed state and failures trigger recovery/evaluation.','100% injected failure detection with verifier · 0% without verifier'),
 ('Audit the metric—and the grader','Real feature ablations isolate temporal update, contradiction resolution, proactivity calibration, privacy, goal lifecycle, and verification.','Ranking reverses after shared confidence calibration; grader robustness is tested on held-out attacks'),
 ('Show the failure surface','Low-value proactivity is the weakest slice; the lexical reward baseline falls to 66.7% on unseen paraphrases.','Failures remain visible and become the next experiment'),
 ('A complete research artifact','Paper · code · PersonalBench · dataset · interactive demo · video · system report · threat model · evidence ledger','Controlled synthetic substrate; no human/frontier-model performance claim'),
]

def wrap(draw,text,font,width):
    words=text.split(); lines=[]; cur=''
    for w in words:
        trial=(cur+' '+w).strip()
        if draw.textbbox((0,0),trial,font=font)[2] <= width: cur=trial
        else:
            if cur: lines.append(cur)
            cur=w
    if cur: lines.append(cur)
    return lines
for i,(title,body,foot) in enumerate(slides):
    im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
    d.rounded_rectangle((70,60,1210,660),radius=28,fill=panel)
    d.text((105,95),f'{i+1:02d} / {len(slides):02d}',font=FM,fill=accent)
    y=155
    for line in wrap(d,title,F1,1000): d.text((105,y),line,font=F1,fill=fg); y+=72
    y+=28
    for line in wrap(d,body,FB,980): d.text((105,y),line,font=FB,fill=fg); y+=39
    y=590
    for line in wrap(d,foot,FS,980): d.text((105,y),line,font=FS,fill=muted); y+=30
    if i==0: im.save(OUT/'video_poster.png')
    im.save(TMP/f'frame_{i:02d}.png')
concat=TMP/'concat.txt'
with concat.open('w') as f:
    for i in range(len(slides)):
        f.write(f"file 'frame_{i:02d}.png'\n")
        f.write('duration 4\n')
    f.write(f"file 'frame_{len(slides)-1:02d}.png'\n")
subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-vf','fps=30,format=yuv420p','-c:v','libx264','-movflags','+faststart',str(OUT/'personal_agi_os_demo.mp4')],cwd=TMP,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
shutil.rmtree(TMP)
print(OUT/'personal_agi_os_demo.mp4')
