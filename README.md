# ccc917111.github.io

Personal academic homepage. Plain static HTML — GitHub Pages serves it as-is, with no
build step, so nothing can fail to compile.

## Where the content lives

| File | Contents |
|---|---|
| `index.html` | About, research interests, education |
| `research.html` | Research projects, newest first |
| `publications.html` | Journal articles and conference papers |
| `projects.html` | Public code repositories, technical background |
| `assets/style.css` | All styling for every page |
| `assets/favicon.svg` | Tab icon |

The four pages share the same masthead and sidebar block. When the name, email or
navigation changes, update all four.

## Editing

Edit the HTML directly. To add a publication, copy an existing `<div class="entry">` block in
`publications.html`; to add a research entry, copy one in `research.html`. Wrap your own name
in `<span class="me">` inside an author list.

## Adding a CV

Put `cv.pdf` in the repository root and add `<a href="cv.pdf">CV</a>` inside the
`<div class="masthead__inner">` block on all four pages.

## Local preview

Open `index.html` in a browser, or run `python3 -m http.server` in this directory.
