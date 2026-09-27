from __future__ import annotations
import json,re,tomllib
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]; PAGE=ROOT/'project/index.html'
html=PAGE.read_text(encoding='utf-8'); soup=BeautifulSoup(html,'html.parser')
version=tomllib.loads((ROOT/'pyproject.toml').read_text(encoding='utf-8'))['project']['version']
checks={}; errors=[]
def check(name,cond,detail=''):
    checks[name]={'passed':bool(cond),'detail':detail}
    if not cond: errors.append(f'{name}: {detail}')
def txt(sel):
    x=soup.select_one(sel); return x.get_text(' ',strip=True) if x else ''
# Identity and metadata
check('doctype',html.lstrip().lower().startswith('<!doctype html>'),'HTML5 doctype required')
check('title',bool(soup.title and 'PersonaMetrica' in soup.title.text),'PersonaMetrica title missing')
check('public_author',(soup.find('meta',attrs={'name':'author'}) or {}).get('content')=='Aura Yavary','public author must be Aura Yavary')
check('description','evaluation' in (soup.find('meta',attrs={'name':'description'}) or {}).get('content','').lower(),'research description missing')
check('viewport',bool(soup.find('meta',attrs={'name':'viewport'})),'viewport missing')
check('og',all(soup.find('meta',attrs={'property':x}) for x in ['og:title','og:description','og:image']),'Open Graph incomplete')
check('twitter',all(soup.find('meta',attrs={'name':x}) for x in ['twitter:card','twitter:title','twitter:description','twitter:image']),'Twitter metadata incomplete')
ld=soup.find('script',attrs={'type':'application/ld+json'})
try:
    obj=json.loads(ld.string if ld else '')
    ok=obj.get('name')=='PersonaMetrica' and obj.get('author',{}).get('name')=='Aura Yavary' and obj.get('version')==version
except Exception: ok=False
check('json_ld',ok,'JSON-LD name/author/version mismatch')
# Evidence-first hero
hero=txt('header.hero'); hero_l=hero.lower()
for name,phrase in [('brand','PersonaMetrica'),('protocol_question','evaluation protocols'),('protocol_sensitive','protocol-sensitive'),('seed_resampling','seed resampling'),('bootstrap_point','51.6%'),('bootstrap_interval','50.7–53.8%'),('grid_robustness','13 leave-one-level-out'),('grader_attack','96%'),('causal_hardening','0%'),('scope_frontier','frontier-model'),('scope_sota','sota')]:
    check('hero_'+name,phrase.lower() in hero_l,f'hero missing {phrase}')
check('hero_no_legacy_gain','+58.2' not in hero and 'mean personalization accuracy' not in hero_l,'legacy gain must not be primary hero claim')
hero_links=[a.get_text(' ',strip=True) for a in soup.select('header.hero .buttons a')]
for label in ['Paper','Code','Demo','Benchmark','Video','Novelty audit']:
    check('hero_cta_'+re.sub('[^a-z]','_',label.lower()),label in hero_links,f'hero missing {label} CTA')
# 14-part flagship-page contract: Hero + 13 downstream sections.
check('hero_section_01',bool(soup.select_one('header#hero[data-section="01"]')),'Hero must be explicit section 01')
hero_contract=txt('.hero-contract').lower()
for phrase in ['problem','my contribution','main result','does it work?']:
    check('hero_contract_'+re.sub('[^a-z]','_',phrase),phrase in hero_contract,f'60-second hero contract missing {phrase}')
required_ids=['problem','idea','architecture','contribution','experiments','results','failures','demo','scaling','safety','technical','artifacts','citation']
check('page_14_part_contract',1+sum(bool(soup.find(id=sid)) for sid in required_ids)==14,'flagship page must contain Hero + 13 required sections')
# Research narrative sections
for sid in required_ids: check('section_'+sid,bool(soup.find(id=sid)),f'missing section {sid}')
idea=txt('#idea').lower()
for phrase in ['ranking-stability','evaluator-under-evaluation','counterfactual','not claimed','first personalization benchmark','universal sota']:
    check('novelty_'+re.sub('[^a-z]','_',phrase),phrase in idea,f'novelty boundary missing {phrase}')
problem=txt('#problem').lower(); check('problem_change','user changes' in problem or 'user change' in problem,'evolving-user problem missing')
check('problem_autonomy','autonomy' in problem,'autonomy boundary missing')
arch=txt('#architecture').lower();
for phrase in ['agent loop','recovery loop','eval / post-training loop','provenance','confidence','verify']:
    check('architecture_'+re.sub('[^a-z]','_',phrase),phrase in arch,f'architecture missing {phrase}')
contrib=txt('#contribution').lower()
for phrase in ['designed and implemented','research framing','system implementation','technical decisions i owned']:
    check('ownership_'+re.sub('[^a-z]','_',phrase),phrase in contrib,f'ownership missing {phrase}')
exp=txt('#experiments').lower()
for phrase in ['500 synthetic long-horizon users','10 held-out test seeds','75 frozen evaluation protocols','baselines / ablations','held-out evaluator attack families']:
    check('experiments_'+re.sub('[^a-z]','_',phrase),phrase in exp,f'experiment setup missing {phrase}')
res=txt('#results').lower()
for phrase in ['personalization','proactivity','verified recovery','baseline → method snapshot','latency','external api cost','synthetic/mechanistic']:
    check('results_'+re.sub('[^a-z]','_',phrase),phrase in res,f'results missing {phrase}')
fail=txt('#failures').lower(); check('failure_visible','failure modes are part of the result' in fail,'failure analysis must be visible'); check('failure_reward','unseen paraphrases' in fail,'semantic generalization failure missing'); check('failure_why','root cause:' in fail,'failure root-cause explanation missing'); check('failure_recovery','concrete execution recovery' in fail and 'retries once' in fail,'concrete recovery path missing')
check('interactive_demo',bool(soup.select_one('#steps[role="tablist"]')) and bool(soup.select_one('#viewer[aria-live]')),'interactive trajectory missing')
scale=txt('#scaling').lower()
for phrase in ['model size','task horizon','sandbox tool primitives','reference local latency','external api cost','robustness']:
    check('scaling_'+re.sub('[^a-z]','_',phrase),phrase in scale,f'scaling scope missing {phrase}')
safe=txt('#safety').lower()
for phrase in ['irreversible actions','human escalation','confirmation','known limits']:
    check('safety_'+re.sub('[^a-z]','_',phrase),phrase in safe,f'safety missing {phrase}')
tech=txt('#technical').lower()
for phrase in ['engineering system design','training / post-training baseline','eval methodology','evidence ledger']:
    check('technical_'+re.sub('[^a-z]','_',phrase),phrase in tech,f'technical link missing {phrase}')
art=txt('#artifacts')
for phrase in ['Paper','Code','GitHub','Benchmark','Dataset','Novelty / SOTA audit','Demo','Video','Technical report','Blog post']:
    check('artifact_'+re.sub('[^a-z]','_',phrase.lower()),phrase in art,f'artifact missing {phrase}')
cit=txt('#citation')
for phrase in ['Aura Yavary','2026',f'v{version}','@software{','PersonaMetrica']:
    check('citation_'+re.sub('[^a-z0-9]','_',phrase.lower()),phrase in cit,f'citation missing {phrase}')

# Evidence Layer: unnumbered second layer below the polished project narrative.
process=txt('#research-process').lower()
check('research_process_section',bool(soup.find(id='research-process')),'Inside the research process section missing')
for phrase in ['logged experiments','failed or materially revised hypotheses','major design decisions','persistent failure modes','calibration reversed the story','evaluator itself failed','perfect reward score was misleading','more rows did not mean more data']:
    check('research_process_'+re.sub('[^a-z]','_',phrase),phrase in process,f'research-process layer missing {phrase}')
for href in ['../experiments/EXPERIMENT_JOURNAL.md','../experiments/FAILED_EXPERIMENTS.md','../experiments/DECISION_LOG.md','../experiments/UNEXPECTED_FINDINGS.md','../artifacts/README.md','../docs/GIT_HISTORY.md','../docs/EVIDENCE_LAYER.md','../scripts/reproduce.py']:
    check('research_link_'+re.sub('[^a-z0-9]','_',href.lower()),bool(soup.select_one(f'#research-process a[href="{href}"]')),f'research-process link missing {href}')

# Exact visible numbering must match the public 14-part contract.
expected_kickers={
'problem':'02 · Why this problem matters','idea':'03 · Core idea','architecture':'04 · Architecture','contribution':'05 · My contribution',
'experiments':'06 · Experiments','results':'07 · Results','failures':'08 · Failure analysis','demo':'09 · Interactive demo',
'scaling':'10 · Scaling','safety':'11 · Safety / limitations','technical':'12 · Technical deep dive','artifacts':'13 · Artifacts','citation':'14 · Citation'}
for sid,label in expected_kickers.items():
    sec=soup.find(id=sid); kicker=sec.select_one('.kicker').get_text(' ',strip=True) if sec and sec.select_one('.kicker') else ''
    check('numbering_'+sid,kicker==label,f'{sid} kicker must be {label!r}, got {kicker!r}')

# Accessibility and integrity
check('image_alt',all(i.get('alt','').strip() for i in soup.find_all('img')),'all images need alt text')
check('skip_link',bool(soup.select_one('a.skip[href="#main"]')),'skip link missing')
check('main_landmark',bool(soup.find('main',id='main')),'main landmark missing')
check('reduced_motion','prefers-reduced-motion' in html,'reduced-motion CSS missing')
check('focus_visible',':focus-visible' in html,'focus-visible CSS missing')
broken=[]; external=[]
for tag,attr in [('a','href'),('img','src'),('source','src'),('link','href')]:
    for el in soup.find_all(tag):
        v=el.get(attr)
        if not v or v.startswith('#') or v.startswith('mailto:') or v.startswith('data:'): continue
        if re.match(r'^https?://',v): external.append(v); continue
        if not (PAGE.parent/v).resolve().exists(): broken.append((tag,v))
check('local_links',not broken,f'broken local targets: {broken}')
check('zero_external_runtime_deps',not external,f'external runtime dependencies: {external}')
for rel in ['paper/personametrica_anonymous.pdf','data/personametrica_bench.jsonl','reports/NOVELTY_SOTA_AUDIT.md']:
    check('canonical_'+rel.replace('/','_').replace('.','_'),(ROOT/rel).exists(),f'missing canonical artifact {rel}')
video=ROOT/'project/assets/personal_agi_os_demo.mp4'; check('video_artifact',video.exists() and video.stat().st_size>1000,'demo video missing')
try:
    tr=json.loads((ROOT/'project/assets/trajectory.json').read_text()); tr_ok=len(tr)>=5 and tr[-1].get('recovery',{}).get('recovered') is True
except Exception: tr_ok=False
check('trajectory_artifact',tr_ok,'runtime trajectory lacks verified recovery')
report={'page':'project/index.html','version':version,'checks':checks,'passed':not errors,'errors':errors}
(ROOT/'data/project_page_qa.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
lines=['# Project Page QA','',f"**Status:** {'PASS' if not errors else 'FAIL'}",'',f"Checks: {sum(x['passed'] for x in checks.values())}/{len(checks)} passed.",'']
for k,v in checks.items(): lines.append(f"- {'✓' if v['passed'] else '✗'} `{k}`" + (f" — {v['detail']}" if v['detail'] and not v['passed'] else ''))
(ROOT/'reports/PROJECT_PAGE_QA.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if errors:
    print('\n'.join(errors)); raise SystemExit(1)
print(f'Project page QA passed: {len(checks)}/{len(checks)} checks.')
