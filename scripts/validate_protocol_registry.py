from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
reg=json.loads((ROOT/'configs'/'protocol_registry.json').read_text())
assert reg['development_seeds']==[1,2,3]
assert reg['long_horizon_test_seeds']==list(range(30,40))
assert len(reg['calibration_families'])>=3
assert len(reg['protocol_stability_thresholds'])>=5
assert len(reg['protocol_stability_defer_costs'])>=5
assert 'No single operating-point utility result' in reg['interpretation_rule']
print('Protocol registry validation: PASS')
