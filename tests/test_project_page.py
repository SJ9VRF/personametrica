from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]

def test_project_page_has_required_surfaces():
    text=(ROOT/'project/index.html').read_text(encoding='utf-8')
    required=[
        'PersonaMetrica','Why this problem matters','Core idea','My contribution','Architecture',
        'Experiments','Results','Failure analysis','Interactive demo','Scaling',
        'Safety / limitations','Technical deep dive','Artifacts','Citation',
        '>Paper<','>Code<','>Demo<','>Benchmark<','>Video<','Aura Yavary'
    ]
    for item in required:
        assert item in text

def test_project_assets_exist_and_trajectory_recovers():
    assert (ROOT/'project/assets/personal_agi_os_demo.mp4').exists()
    assert (ROOT/'project/assets/video_poster.png').exists()
    traj=json.loads((ROOT/'project/assets/trajectory.json').read_text())
    assert len(traj) >= 5
    final=traj[-1]
    assert final['recovery']['recovered'] is True
    assert final['recovery']['attempts'] == 2

def test_scaling_report_has_measured_cases():
    d=json.loads((ROOT/'data/scaling_results.json').read_text())
    assert len(d['cases']) >= 5
    assert all(x['wall_seconds_median'] > 0 for x in d['cases'])
    assert all(x['external_inference_cost_usd'] == 0 for x in d['cases'])
