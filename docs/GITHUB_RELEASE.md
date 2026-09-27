# GitHub Release Package

This release is structured to be uploaded directly as a GitHub repository. It includes source, tests, CI, benchmark data, paper/report artifacts, project homepage, citation metadata, license, contributing guide, release checks, and a reproducibility command.

## Recommended repository root

Upload the contents of this release directory as the repository root. Do not wrap it in an additional nested folder.

## Verification before publishing

```bash
python -m pytest -q
python scripts/project_page_qa.py
python scripts/regression_gate.py
python scripts/release_check.py
```

## GitHub Pages

Publish the `project/` directory as the static project page, or follow `docs/PROJECT_PAGE_DEPLOYMENT.md` for a root-path deployment.

A public GitHub URL is deliberately not hard-coded in the local artifact before the repository actually exists.
