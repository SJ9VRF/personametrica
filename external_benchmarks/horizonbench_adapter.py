from __future__ import annotations
import json, math
from pathlib import Path
from typing import Iterable

REQUIRED = {"id","generator","has_evolved","correct_letter","predicted_letter","correct"}

def load_results(path: str|Path):
    rows=[]
    with Path(path).open(encoding='utf-8') as f:
        for line_no,line in enumerate(f,1):
            if not line.strip(): continue
            row=json.loads(line)
            missing=REQUIRED-set(row)
            if missing: raise ValueError(f"{path}:{line_no}: missing {sorted(missing)}")
            expected = row['predicted_letter'] == row['correct_letter']
            if bool(row['correct']) != expected:
                raise ValueError(f"{path}:{line_no}: inconsistent correct flag")
            conf=row.get('confidence')
            if conf is not None and not (0.0 <= float(conf) <= 1.0):
                raise ValueError(f"{path}:{line_no}: confidence outside [0,1]")
            rows.append(row)
    if not rows: raise ValueError(f"{path}: empty results")
    return rows

def _acc(rows): return sum(bool(r['correct']) for r in rows)/len(rows) if rows else None

def summarize(rows):
    evolved=[r for r in rows if bool(r['has_evolved'])]
    static=[r for r in rows if not bool(r['has_evolved'])]
    out={'n':len(rows),'accuracy':_acc(rows),'evolved_n':len(evolved),'evolved_accuracy':_acc(evolved),'static_n':len(static),'static_accuracy':_acc(static)}
    with_conf=[r for r in rows if r.get('confidence') is not None]
    out['confidence_coverage']=len(with_conf)/len(rows)
    if len(with_conf)==len(rows):
        out['brier']=sum((float(r['confidence'])-int(bool(r['correct'])))**2 for r in rows)/len(rows)
    return out

def utility(rows, threshold:float, defer_cost:float):
    if any(r.get('confidence') is None for r in rows):
        raise ValueError('utility requires confidence for every row; official HorizonBench base output does not require it')
    acted=[r for r in rows if float(r['confidence'])>=threshold]
    correct=sum(bool(r['correct']) for r in acted); wrong=len(acted)-correct; deferred=len(rows)-len(acted)
    return (correct-wrong-defer_cost*deferred)/len(rows)

def compare_models(named_rows:dict[str,list[dict]]):
    ids={name:{r['id'] for r in rows} for name,rows in named_rows.items()}
    first=next(iter(ids.values()))
    if any(v!=first for v in ids.values()): raise ValueError('model result files must contain the same item IDs')
    return {name:summarize(rows) for name,rows in named_rows.items()}
