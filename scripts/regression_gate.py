from __future__ import annotations
import argparse, json
from pathlib import Path

def evaluate(results: dict, gates: dict) -> list[str]:
    failures=[]
    systems=results.get("systems",{})
    for system, metrics_gates in gates.items():
        if system not in systems:
            failures.append(f"missing system: {system}")
            continue
        metrics=systems[system].get("metrics", systems[system])
        for metric, rule in metrics_gates.items():
            if metric not in metrics:
                failures.append(f"{system}.{metric}: missing")
                continue
            value=float(metrics[metric])
            if "min" in rule and value < float(rule["min"]):
                failures.append(f"{system}.{metric}={value:.4f} < min {rule['min']}")
            if "max" in rule and value > float(rule["max"]):
                failures.append(f"{system}.{metric}={value:.4f} > max {rule['max']}")
    return failures

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--results',default='data/eval_results.json')
    ap.add_argument('--gates',default='configs/regression_gates.json')
    args=ap.parse_args()
    results=json.loads(Path(args.results).read_text())
    gates=json.loads(Path(args.gates).read_text())
    failures=evaluate(results,gates)
    if failures:
        print('REGRESSION GATE FAILED')
        for f in failures: print('-',f)
        raise SystemExit(1)
    print('Regression gate passed.')

if __name__=='__main__': main()
