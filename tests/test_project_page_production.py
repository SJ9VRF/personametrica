from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]

def test_project_page_qa_passes():
    subprocess.run([sys.executable,'scripts/project_page_qa.py'],cwd=ROOT,check=True,capture_output=True,text=True)
    q=json.loads((ROOT/'data/project_page_qa.json').read_text())
    assert q['passed'] is True

def test_deployment_assets_exist():
    for p in ['project/site.webmanifest','project/robots.txt','project/assets/favicon.svg','project/assets/social_card.svg','docs/PROJECT_PAGE_DEPLOYMENT.md']:
        assert (ROOT/p).exists()
