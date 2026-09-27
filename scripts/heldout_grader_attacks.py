from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from personalbench.agent_evals.heldout_attacks import run_heldout_attack_suite
out=run_heldout_attack_suite()
(ROOT/'data'/'heldout_grader_attacks.json').write_text(json.dumps(out,indent=2)+'\n')
lines=['# Held-out grader attacks','','These attacks were added after the original ten-perturbation grader suite and are evaluated separately to test evaluator overfitting. They are controlled synthetic attacks, not frontier-model trajectories.','', '| Grader | False accept rate |','|---|---:|']
for name,m in out['metrics'].items(): lines.append(f"| {name} | {m['false_accept_rate']:.1%} |")
lines += ['', '## Attack-family false accepts','', '| Attack | End-state | Robust v3.4 | Causal v3.5 |','|---|---:|---:|---:|']
for a,m in out['by_attack'].items(): lines.append(f"| {a} | {m['end_state_only_false_accept_rate']:.1%} | {m['robust_trajectory_false_accept_rate']:.1%} | {m['causal_trajectory_false_accept_rate']:.1%} |")
lines += ['', 'The causal grader requires an observable allowed action, payload support for the requested state, live permission at action time, full-target verification, and verification after the final action. The result should be interpreted as evaluator hardening on authored attacks, not as evidence of model capability.']
(ROOT/'reports'/'HELDOUT_GRADER_ATTACKS.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(out['metrics'],indent=2))
