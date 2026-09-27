from __future__ import annotations
import argparse,json,re,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--strict',action='store_true',help='Fail on external submission blockers (official style / hosted URL).'); args=ap.parse_args()
 checks=[]
 def ck(name,ok,detail,blocking=False): checks.append({'name':name,'ok':bool(ok),'detail':detail,'blocking':blocking})
 # paper/checklist
 paper=(ROOT/'paper/PAPER.md').read_text(); app=(ROOT/'paper/APPENDIX_CHECKLIST.md').read_text(); off=(ROOT/'paper/main_neurips_2026.tex')
 ck('anonymous paper source', 'Aura Yavary' not in paper, 'paper/PAPER.md contains no public author name')
 ck('15 checklist answers', all(f'{i}.' in app for i in range(1,16)), 'paper/APPENDIX_CHECKLIST.md contains items 1-15')
 ck('official-template-ready source', off.exists(), 'paper/main_neurips_2026.tex generated')
 style=ROOT/'paper/neurips_2026.sty'; ck('official NeurIPS 2026 style present',style.exists(),'Download official 2026 template and place paper/neurips_2026.sty before final submission',blocking=True)
 # croissant
 meta=json.loads((ROOT/'data/personalbench_x_croissant.json').read_text())
 for key in ['@context','@type','name','url','license','conformsTo','distribution','recordSet']:
  ck(f'Croissant core: {key}',key in meta and bool(meta[key]),f'{key} present')
 for key in ['rai:dataLimitations','rai:dataBiases','rai:personalSensitiveInformation','rai:dataUseCases','rai:dataSocialImpact','rai:hasSyntheticData','prov:wasGeneratedBy']:
  ck(f'Croissant RAI: {key}',key in meta and meta[key] is not None,f'{key} present')
 url=str(meta.get('url','')); hosted=url.startswith(('https://','http://')) and 'REPLACE_' not in url and '.invalid' not in url
 ck('anonymous reviewer-accessible dataset URL',hosted,f'current url={url!r}; must be externally accessible at submission',blocking=True)
 # bundle
 bundle=ROOT/'submission/personalbench_x_anonymous_bundle.zip'; ck('anonymous submission bundle',bundle.exists(),'submission zip exists')
 if bundle.exists():
  with zipfile.ZipFile(bundle) as z:
   names=z.namelist(); suspicious=[n for n in names if 'AUTHOR_METADATA' in n or n.startswith('project/')]
   ck('bundle excludes author-facing metadata',not suspicious,f'suspicious files={suspicious}')
 # PDF current draft
 pdf=ROOT/'paper/personalbench_x_anonymous.pdf'; ck('readable draft PDF',pdf.exists() and pdf.stat().st_size>10000,'generic-style research draft exists; not venue-format final')
 ck('PDF under 50MB',pdf.exists() and pdf.stat().st_size < 50*1024*1024,'NeurIPS maximum file size is 50MB')
 fmt=ROOT/'data/submission_format_audit.json'
 if fmt.exists():
  f=json.loads(fmt.read_text()); ck('generic draft content <=9 pages',bool(f.get('generic_draft_content_within_9_pages')),f"content pages before references={f.get('content_pages_before_references')}")
  ck('anonymous PDF content scan',not f.get('paper_identity_leaks'),f"leaks={f.get('paper_identity_leaks')}")
  ck('anonymous bundle content scan',not f.get('bundle_identity_leaks'),f"leaks={f.get('bundle_identity_leaks')}")
 # report
 blocking=[c for c in checks if c['blocking'] and not c['ok']]; failures=[c for c in checks if not c['ok'] and not c['blocking']]
 status='READY' if not blocking and not failures else ('BLOCKED_EXTERNAL' if blocking and not failures else 'FAIL')
 obj={'status':status,'strict':args.strict,'checks':checks,'external_blockers':[c['name'] for c in blocking]}
 (ROOT/'data/neurips_ed_submission_readiness.json').write_text(json.dumps(obj,indent=2)+'\n')
 lines=['# NeurIPS 2026 E&D submission readiness','',f'**Status: {status}**','', 'This checker separates repository/scientific completeness from requirements that need external venue assets or hosting.','']
 for c in checks: lines.append(f"- {'PASS' if c['ok'] else ('BLOCKED' if c['blocking'] else 'FAIL')}: **{c['name']}** - {c['detail']}")
 lines += ['', '## External blockers', '']
 if blocking:
  for c in blocking: lines.append(f"- {c['name']}: {c['detail']}")
 else: lines.append('- None.')
 (ROOT/'reports/NEURIPS_ED_SUBMISSION_READINESS.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps({'status':status,'passed':sum(c['ok'] for c in checks),'total':len(checks),'external_blockers':[c['name'] for c in blocking]},indent=2))
 if failures or (args.strict and blocking): return 2
 return 0
if __name__=='__main__': raise SystemExit(main())
