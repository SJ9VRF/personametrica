# Project Page Deployment

`project/index.html` is a self-contained static project page with no external runtime dependencies. It can be hosted on GitHub Pages, Cloudflare Pages, Netlify, Vercel static hosting, or any ordinary web server.

## What must be deployed

Deploy the repository with relative paths preserved, because the page links to checked-in research artifacts in `paper/`, `reports/`, `docs/`, `data/`, and `dashboard/`.

## Local review

From the repository root:

```bash
python -m http.server 8000
```

Then open `/project/` on the local server. Using a server rather than `file://` gives browser behavior closest to a real deployment.

## Release QA

```bash
python scripts/project_page_qa.py
```

The check validates required sections, metadata, JSON-LD, local links, accessibility basics, demo/video assets, and the absence of third-party runtime dependencies.

Visual browser screenshots are optional and intentionally not part of the release gate; the deterministic release gate is DOM/static and artifact based.

## URL-dependent metadata

The release intentionally does **not** invent a public canonical URL before deployment. Once a final domain/path exists, add `canonical`, `og:url`, and an absolute Open Graph image URL during deployment.
