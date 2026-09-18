---
order: 2
---
# Getting started

A small folder of plain text is all you need to begin.

## Your project

```text
mkdocs.yml             Site settings and navigation
docs/                  Your Markdown documentation
theme/                 Templates and bundled assets
hooks/offline_search.py Portable local search index
wheelhouse/            Offline Python installation files
```

## Write a page

Create `docs/notes.md` in any text editor:

```markdown
# Lab notes

Record the assumptions, then show the result.

## First observation

The measured energy is $E = mc^2$.
```

Add your page to the `nav` section in `mkdocs.yml`. Keep paths relative to `docs/`.

## Preview and build

```powershell
.\.venv\Scripts\python -m mkdocs serve
.\.venv\Scripts\python -m mkdocs build --strict
```

The preview runs on your own machine. The build produces a portable `site/` folder; opening its `index.html` works without a server.

## Make it yours

Change `site_name` and `site_description` in `mkdocs.yml`. Edit the color variables at the top of `theme/assets/theme.css` to adjust the palette. The brand mark uses the first letter of your site name.

!!! note "Keep the project portable"
    Use relative Markdown links and local images. To add an image, place it under `docs/images/` and reference it from your page.
