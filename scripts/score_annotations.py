from __future__ import annotations
import argparse,json,math
from collections import Counter
from pathlib import Path

def fleiss_kappa(label_matrix):
    # label_matrix: list[list[label]], same number of raters per item
    if not label_matrix: return 0.0
    n=len(label_matrix[0])
    if n<2 or any(len(x)!=n for x in label_matrix): raise ValueError('Fleiss kappa requires equal >=2 raters per item')
    cats=sorted({x for row in label_matrix for x in row})
    N=len(label_matrix)
    P=[]; totals=Counter()
    for row in label_matrix:
        c=Counter(row); totals.update(c)
        P.append((sum(v*v for v in c.values())-n)/(n*(n-1)))
    Pbar=sum(P)/N
    pe=sum((totals[c]/(N*n))**2 for c in cats)
    return (Pbar-pe)/(1-pe) if pe<1 else 1.0

def main():
    ap=argparse.ArgumentParser();ap.add_argument('annotations',nargs='+');ap.add_argument('--tasks',default='annotation/tasks.json');ap.add_argument('--out',default='data/human_annotation_results.json');args=ap.parse_args()
    tasks=json.loads(Path(args.tasks).read_text())['tasks']; task_ids={t['id'] for t in tasks}
    anns=[]
    for p in args.annotations:
        x=json.loads(Path(p).read_text());anns.append(x['labels'])
    common=sorted(set.intersection(*(set(a) for a in anns)) & task_ids) if anns else []
    matrix=[[a[i] for a in anns] for i in common]
    raw=sum(len(set(r))==1 for r in matrix)/max(1,len(matrix))
    out={'annotators':len(anns),'items_with_all_labels':len(common),'raw_unanimous_agreement':raw,'fleiss_kappa':fleiss_kappa(matrix) if matrix else None}
    Path(args.out).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
if __name__=='__main__':main()
