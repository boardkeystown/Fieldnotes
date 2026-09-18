# Fieldnotes — an offline MkDocs theme

A minimal Read the Docs–inspired layout with a sidebar, light/dark button, local search, Pygments code highlighting, admonitions, and locally bundled KaTeX math.

For step-by-step transfer, installation, and authoring instructions, see [Use this theme offline](docs/offline.md).

## Run on Windows

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --no-index --find-links=wheelhouse -r requirements.lock
.\.venv\Scripts\python -m mkdocs serve
.\.venv\Scripts\python -m mkdocs build --strict
```

Open `site/index.html` to read the built site directly. Copy the whole site folder when distributing it. A reader needs only a browser. An author needs Python and the included packages. See `OFFLINE-KIT.txt` for the wheelhouse platform.

## Reuse in another MkDocs project

Copy `theme/` and `hooks/` beside your `mkdocs.yml`. Copy the `theme`, `hooks`, `markdown_extensions`, `plugins: []`, and `use_directory_urls: false` settings from this example. Install the requirements using the bundled wheelhouse. Replace the example `nav` and `docs/` with your own content. Keep `hooks/offline_search.py` enabled for portable search.

This is a standalone custom-directory theme, not a pip-installed theme package. It does not inherit CDN behavior from another theme. Pygments creates token markup during the build; CSS styles it in both palettes. Arithmatex preserves LaTeX and KaTeX renders it with local fonts. Search is a generated JavaScript index compatible with file URLs.

## Offline guarantee boundary

All theme assets are local, including fonts. Your own remote images, embeds, extra scripts, and links are outside that boundary. No service worker or browser cache is needed. Math supports KaTeX's LaTeX math subset, not full TeX document compilation. Search is a small full-page substring search, intended for modest documentation sites.

## Validation

Run `.\.venv\Scripts\python tools/verify_offline.py` after building to check every generated HTML asset and internal link, CSS font reference, search entry, and vendored checksum. Browser checks should include direct file access, math, search, copy buttons, responsive navigation, and light/dark themes with external requests blocked.

## Licenses

Original theme files are MIT licensed (see LICENSE). KaTeX's license is retained under `theme/assets/vendor/katex/LICENSE`. Python package licenses remain with their respective wheel distributions. Vendored files and provenance are recorded in `vendor-manifest.json`.

## Implementation references

- MkDocs custom themes: https://www.mkdocs.org/dev-guide/themes/
- KaTeX local browser assets: https://katex.org/docs/browser
- KaTeX auto-render: https://katex.org/docs/autorender

## RHEL 7 / Python 3.8 test

A separate Podman test prepares Linux dependencies and verifies a fresh installation and build with container networking disabled. Run `.\tests\rhel7\run.ps1 -Prepare` once while connected, then `.\tests\rhel7\run.ps1` to repeat offline. See [the container test guide](tests/rhel7/README.md). Outputs are in `.artifacts/rhel7/`. The Windows requirements and wheelhouse remain separate.
