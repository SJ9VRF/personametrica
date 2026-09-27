from __future__ import annotations
import json, re, subprocess, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
pdf=ROOT/'paper/personalbench_x_anonymous.pdf'
if not pdf.exists(): raise SystemExit('missing paper PDF')
info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
m=re.search(r'^Pages:\s+(\d+)',info,re.M); pages=int(m.group(1)) if m else -1
# Determine first page that begins the bibliography by searching the literal References heading.
ref_page=None
for i in range(1,pages+1):
    txt=subprocess.check_output(['pdftotext','-f',str(i),'-l',str(i),str(pdf),'-'],text=True,errors='ignore')
    if re.search(r'(?m)^References\s*$',txt):
        ref_page=i; break
content_pages=(ref_page-1) if ref_page else None
text=subprocess.check_output(['pdftotext',str(pdf),'-'],text=True,errors='ignore')
identifiers=['Aura Yavary','Arefeh Yavary','UC Davis','Google LLC']
leaks=[x for x in identifiers if x.lower() in text.lower()]
checklist=ROOT/'paper/APPENDIX_CHECKLIST.md'
app=checklist.read_text()
checklist_complete=all(re.search(rf'(?m)^{i}\.\s',app) for i in range(1,16))
# supplement anonymity by content, not only filenames
bundle=ROOT/'submission/personalbench_x_anonymous_bundle.zip'
bundle_leaks=[]
if bundle.exists():
    with zipfile.ZipFile(bundle) as z:
        for name in z.namelist():
            if name.endswith(('.md','.tex','.txt','.json','.jsonl','.py','.bib','.cff','.html')):
                try: t=z.read(name).decode('utf-8','ignore').lower()
                except Exception: continue
                for x in identifiers:
                    if x.lower() in t: bundle_leaks.append({'file':name,'term':x})
obj={
 'pdf_pages_total':pages,
 'references_start_page':ref_page,
 'content_pages_before_references':content_pages,
 'generic_draft_content_within_9_pages': content_pages is not None and content_pages<=9,
 'pdf_size_bytes':pdf.stat().st_size,
 'pdf_under_50mb':pdf.stat().st_size < 50*1024*1024,
 'paper_identity_leaks':leaks,
 'bundle_identity_leaks':bundle_leaks,
 'checklist_complete_15_items':checklist_complete,
 'official_style_present':(ROOT/'paper/neurips_2026.sty').exists(),
 'official_template_url':'https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip',
}
(ROOT/'data/submission_format_audit.json').write_text(json.dumps(obj,indent=2)+'\n')
lines=['# Submission Format & Anonymity Audit','',
       f"- Total draft PDF pages: **{pages}**",
       f"- References start on generic draft page: **{ref_page}**",
       f"- Content pages before References: **{content_pages}**",
       f"- Generic draft content within 9-page target: **{'PASS' if obj['generic_draft_content_within_9_pages'] else 'FAIL'}**",
       f"- PDF < 50 MB: **{'PASS' if obj['pdf_under_50mb'] else 'FAIL'}**",
       f"- 15 checklist items present: **{'PASS' if checklist_complete else 'FAIL'}**",
       f"- Identity leaks in PDF text: **{leaks or 'none'}**",
       f"- Identity leaks in anonymous bundle text: **{bundle_leaks or 'none'}**",
       f"- Official `neurips_2026.sty` present: **{'YES' if obj['official_style_present'] else 'NO — external blocker'}**",'',
       'The page-count check is intentionally conservative but **not a substitute for compiling with the official 2026 style**. The official style remains mandatory before submission.']
(ROOT/'reports/SUBMISSION_FORMAT_AUDIT.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(obj,indent=2))
if not obj['generic_draft_content_within_9_pages'] or not obj['pdf_under_50mb'] or leaks or bundle_leaks or not checklist_complete:
    raise SystemExit(2)
