# NeurIPS 2026 template status

NeurIPS 2026 requires the official LaTeX style for both Main and Evaluations & Datasets submissions, and the mandatory paper checklist must appear after references/appendices in the single submitted PDF.

The research package contains:

- `paper/PAPER.md` — main paper content;
- `paper/APPENDIX_CHECKLIST.md` — technical appendix plus all 15 checklist answers;
- `paper/main_neurips_2026.tex` — source prepared for the official NeurIPS 2026 style;
- `scripts/prepare_neurips_2026_submission.py` — compiles the official-style PDF when `paper/neurips_2026.sty` is present;
- `paper/personalbench_x_anonymous.pdf` — readable locally compiled draft using a generic article style, **not the final venue-format PDF**.

The official formatting archive is published by NeurIPS at:

`https://media.neurips.cc/Conferences/NeurIPS2026/Formatting_Instructions_For_NeurIPS_2026.zip`

This environment could resolve the official URL through the NeurIPS website but could not download the ZIP because outbound file download/DNS is restricted. The style file is therefore not fabricated or copied from another year. Before submission, download the official archive, place `neurips_2026.sty` in `paper/`, run:

```bash
python scripts/prepare_neurips_2026_submission.py
```

and verify the resulting PDF is within the nine-content-page limit. The checklist itself does not count toward the content-page limit.
