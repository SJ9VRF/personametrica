from __future__ import annotations
import re, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; P=ROOT/'paper'
STYLE=P/'neurips_2026.sty'
OFFICIAL='https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip'

def md_to_tex(text:str, out:Path):
    tmp=P/'_tmp_fragment.md'; tmp.write_text(text)
    subprocess.run(['pandoc',str(tmp.relative_to(ROOT)),'-t','latex','--natbib','-o',str(out.relative_to(ROOT))],cwd=ROOT,check=True)
    tmp.unlink()

def main():
    md=(P/'PAPER.md').read_text()
    title=md.splitlines()[0].removeprefix('# ').strip()
    m=re.search(r'## Abstract\n\n(.*?)\n\n## 1\. Introduction',md,re.S)
    if not m: raise SystemExit('Could not locate abstract/introduction boundaries')
    abstract=m.group(1).strip(); body='## 1. Introduction'+md[m.end():]
    md_to_tex(body,P/'official_body.tex'); md_to_tex((P/'APPENDIX_CHECKLIST.md').read_text(),P/'official_appendix_checklist.tex')
    tex=rf'''\documentclass{{article}}
\usepackage{{neurips_2026}}
\usepackage{{amsmath,amssymb,booktabs,graphicx}}
\usepackage{{url}}
\graphicspath{{{{./}}{{paper/}}}}
\title{{{title}}}
\author{{Anonymous Author(s)}}
\begin{{document}}
\maketitle
\begin{{abstract}}
{abstract}
\end{{abstract}}
\input{{paper/official_body.tex}}
\bibliographystyle{{plainnat}}
\bibliography{{paper/references}}
\clearpage
\input{{paper/official_appendix_checklist.tex}}
\end{{document}}
'''
    (P/'main_neurips_2026.tex').write_text(tex)
    if not STYLE.exists():
        (P/'OFFICIAL_STYLE_REQUIRED.txt').write_text('Official NeurIPS 2026 style file is not bundled because it could not be fetched from this network-isolated environment. Download the official template from:\n'+OFFICIAL+'\nPlace neurips_2026.sty in paper/ and rerun: python scripts/prepare_neurips_2026_submission.py\n')
        print('Prepared paper/main_neurips_2026.tex. Official style is required to compile.'); print(OFFICIAL); return 0
    if not shutil.which('lualatex'): raise SystemExit('lualatex is required')
    cmd=['lualatex','-interaction=nonstopmode','-halt-on-error','-output-directory=paper','paper/main_neurips_2026.tex']
    subprocess.run(cmd,cwd=ROOT,check=True); subprocess.run(cmd,cwd=ROOT,check=True)
    shutil.copy2(P/'main_neurips_2026.pdf',P/'personalbench_x_neurips2026_anonymous.pdf')
    print('Built official-style paper/personalbench_x_neurips2026_anonymous.pdf')
    return 0
if __name__=='__main__': raise SystemExit(main())
