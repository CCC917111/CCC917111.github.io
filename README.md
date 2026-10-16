# Yike Chen · Research Portfolio

A responsive, self-contained personal website for research, publications and
software projects. Built with static HTML, CSS and a small optional project
filter. GitHub Pages publishes the site directly; no package installation or
build step is required.

## Site structure

| File | Contents |
|---|---|
| `index.html` | Research introduction, featured studies, selected publications, education and contact |
| `research.html` | Detailed studies, roles, dates and links to supporting work |
| `publications.html` | Full author lists, venues, publication status and paper links |
| `projects.html` | Illustrated software projects, topic filters and technical background |
| `assets/style.css` | Shared design, responsive layouts, focus states and reduced-motion support |
| `assets/site.js` | Accessible project filtering; all projects remain visible without JavaScript |
| `assets/visuals/` | Conceptual method diagrams and the DWTS aggregate result chart |
| `assets/favicon.svg` | Site icon |

The four pages share navigation and footer markup. Keep those blocks consistent
when adding or renaming pages. Mark the active navigation link with
`aria-current="page"`; keep the skip link pointed at `#main`.

## Editing content

- Research entries use `article.research-entry`, with a stable ID for direct links.
- Publications retain full author order, venue information and the precise
  publication status. Do not add a paper or CV link until its file or URL exists.
- Project cards use `article.project-card`. Set `data-category` to `agents`,
  `statistics` or `vision` to participate in the topic filters.
- Update descriptions and Open Graph metadata when a page's focus changes.
- Keep project leadership, original team credit and subsequent extensions clear.

The pricing, representation-learning, forest-fusion and decision-system graphics
are labeled conceptual workflows. The DWTS chart uses published v0.7.0 aggregate
metrics from [DWTS Voting Analysis](https://github.com/CCC917111/DWTS_voting_analysis/tree/main/results/exit_forecast_study).
Its historical evaluation populations and exploratory scope are part of the
figure; retain these labels when updating it.

## Local preview

From the repository root:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open the local site in a browser. Check all four pages on desktop and phone
widths, navigation and anchor links, image loading, keyboard focus, the project
filters and the all-projects fallback with JavaScript disabled. Original reports,
raw research data and private verification artifacts do not belong in this site.

## Publishing

Push reviewed changes to `main` and confirm that the **pages build and deployment**
GitHub Actions run succeeds for the new commit. `.nojekyll` keeps the static files
served without Jekyll processing.
