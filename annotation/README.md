# Human annotation pack

This directory contains a **protocol and labeling UI**, not human results.

## Contents

- `tasks.json`: 620 independent tasks (300 proactivity, 320 belief-update).
- `index.html`: browser labeling UI; reference labels are not displayed.

Run locally:

```bash
python -m http.server 8000 -d annotation
```

Then open `http://localhost:8000/` and export each annotator's JSON.

## Recommended study

- At least 3 independent annotators/item.
- Randomized item order.
- Annotators must not see simulator reference labels.
- Record item-level confidence and optional rationale in a future production study.
- Use majority label only when agreement exceeds a pre-registered threshold; adjudicate the rest.
- Report Fleiss' kappa, raw agreement, ambiguous-item rate, and results both with and without adjudicated items.

The local scorer accepts multiple exported annotation files. No human-alignment claim should be made until real labels are collected.
