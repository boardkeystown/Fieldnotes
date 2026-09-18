---
order: 6
---
# Theme setup

This project includes the Fieldnotes theme, its offline assets, and working examples. The theme is already enabled in the project's `mkdocs.yml`.

## Where the files live

```text
offline_test/
  mkdocs.yml                 Configuration and page navigation
  docs/                      Edit your documentation here
    index.md                 Overview and feature examples
    guide/getting-started.md  Writing and preview instructions
    guide/code.md            Code highlighting and annotations
    guide/math.md            LaTeX math examples
    offline.md               Offline installation and distribution
    theme-setup.md           This page
  theme/
    main.html                Page layout and navigation
    404.html                 Error page
    assets/
      theme.css              Layout, light and dark palettes
      code.css               Syntax highlighting palettes
      appearance.js          Initial color preference
      theme.js               Theme switch, search, math, copy buttons
      vendor/katex/          Bundled math engine, CSS, and fonts
  hooks/offline_search.py     Generates the local search index
  wheelhouse/                Offline Python dependencies
  site/                      Generated HTML; do not edit directly
```

MkDocs keeps theme templates outside `docs/`. Your Markdown content belongs inside `docs/`; the build copies the theme assets into the generated site automatically.

## Active configuration

The project uses these settings in `mkdocs.yml`:

```yaml
docs_dir: docs
site_dir: site
use_directory_urls: false
theme:
  name: null
  custom_dir: theme
  static_templates:
    - 404.html
plugins: []
hooks:
  - hooks/offline_search.py
markdown_extensions:
  - admonition
  - attr_list
  - tables
  - footnotes
  - toc:
      permalink: true
  - pymdownx.highlight:
      anchor_linenums: true
  - pymdownx.superfences
  - pymdownx.arithmatex:
      generic: true
```

`use_directory_urls: false` makes page links work when opening the HTML files directly. The search hook creates a local JavaScript index, and the templates load the bundled KaTeX engine and fonts. No CDN configuration is needed.

## Edit and preview

Run from the project folder:

```powershell
cd D:\Python\mkdocs_examples\offline_test
.\.venv\Scripts\python -m mkdocs serve -f mkdocs.yml
```

Edit Markdown files under `docs/` and open the localhost address printed by MkDocs. Add new pages to `nav` in `mkdocs.yml`.

## Build and check

```powershell
.\.venv\Scripts\python -m mkdocs build --strict -f mkdocs.yml
.\.venv\Scripts\python tools/verify_offline.py
```

Open `site/index.html` directly to read the output without a server. Copy the entire `site/` folder to distribute the documentation.

## Customize the theme

- Change `site_name` and `site_description` in `mkdocs.yml`.
- Edit `theme/assets/theme.css` to adjust layout and the light/dark color variables.
- Edit `theme/main.html` to change the page structure.
- Keep the bundled `theme/assets/vendor/katex/` directory intact for offline math.

See [Code & syntax](guide/code.md) for highlighting and callouts, [Mathematics](guide/math.md) for equations, and [Use this theme offline](offline.md) for installation on a disconnected computer.

