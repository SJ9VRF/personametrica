import json, re, tomllib
from pathlib import Path

def test_release_versions_are_consistent():
    version=tomllib.loads(Path('pyproject.toml').read_text())['project']['version']
    citation=Path('CITATION.cff').read_text()
    assert re.search(rf'^version:\s*{re.escape(version)}\s*$',citation,re.M)
    assert json.loads(Path('MANIFEST.json').read_text())['version']==version
    assert f'v{version}' in Path('CHANGELOG.md').read_text()
