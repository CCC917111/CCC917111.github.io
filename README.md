# Yike Chen · Research Portfolio

A minimal personal website built around a short introduction and selected work.
Detailed studies, publications and research software live on their own pages.
Static HTML and CSS keep the site self-contained: no package installation,
JavaScript or build step is required.

## Site structure

| File | Contents |
|---|---|
| `index.html` | Introduction, two selected studies and contact links |
| `research.html` | Detailed studies, roles, dates and supporting work |
| `publications.html` | Full author lists, venues, publication status and paper links |
| `projects.html` | Research software, with expandable method diagrams and results |
| `assets/style.css` | Shared typography, responsive layouts and keyboard focus |
| `assets/visuals/` | Conceptual method diagrams and the DWTS aggregate result chart |
| `assets/favicon.svg` | Site icon |

The four pages share navigation and footer markup. Keep those blocks consistent
when editing. Mark the current navigation link with `aria-current="page"` and
keep the skip link pointed at `#main`.

## Editing content

- Keep the homepage selective. Put detailed credentials in a CV PDF when one is
  available, then add a real `CV` link alongside the footer's contact links on
  all four pages. Do not publish a placeholder or broken download link.
- Research entries and projects have stable IDs for direct links.
- Preserve publication author order, venue details and precise publication status.
- Project figures use native HTML `details` elements. They work without JavaScript
  and link to the full-size SVG for closer reading.
- Update descriptions and Open Graph metadata when a page's focus changes.
- When changing shared CSS, update its `?v=` version on all four pages.
- Keep project leadership, original team credit and subsequent extensions clear.

The pricing, representation-learning and forest-fusion graphics are conceptual
workflows. The DWTS chart uses published v0.7.0 aggregate metrics from
[DWTS Voting Analysis](https://github.com/CCC917111/DWTS_voting_analysis/tree/main/results/exit_forecast_study).
Its historical evaluation populations and exploratory scope are part of the
figure; retain these labels when updating it.

## Local preview

From the repository root:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Check all four pages on desktop and phone widths, navigation and anchor links,
keyboard focus, expandable figures and image loading. Original reports, raw
research data and private verification artifacts do not belong in this site.

## Publishing

Push reviewed changes to `main` and confirm the **pages build and deployment**
GitHub Actions run succeeds for the new commit. `.nojekyll` serves the static
files without Jekyll processing.
