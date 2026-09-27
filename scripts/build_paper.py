from __future__ import annotations
import shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
paper=ROOT/'paper'
for tool in ('pandoc','lualatex'):
    if not shutil.which(tool): raise SystemExit(f'Missing required paper build tool: {tool}')
# Appendices + mandatory checklist are inserted after citeproc's References section.
subprocess.run(['pandoc','paper/APPENDIX_CHECKLIST.md','-t','latex','-o','paper/appendix_checklist.tex'],cwd=ROOT,check=True)
subprocess.run(['pandoc','paper/PAPER.md','-s','--bibliography=paper/references.bib','--citeproc','--metadata','reference-section-title=References','--include-after-body=paper/appendix_checklist.tex','-V','geometry:margin=0.85in','-V','fontsize=10pt','-V','papersize=letter','-o','paper/main.tex'],cwd=ROOT,check=True)
for ext in ('aux','out','toc','log'):
    q=paper/f'main.{ext}'
    if q.exists(): q.unlink()
cmd=['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory=paper','paper/main.tex']
subprocess.run(cmd,cwd=ROOT,stdout=subprocess.DEVNULL,check=True)
subprocess.run(cmd,cwd=ROOT,stdout=subprocess.DEVNULL,check=True)
shutil.copy2(paper/'main.pdf',paper/'personalbench_x_anonymous.pdf')
shutil.copy2(paper/'main.pdf',paper/'personametrica_anonymous.pdf')
print('Built paper/personametrica_anonymous.pdf (plus legacy alias) with references -> appendix -> checklist order')
