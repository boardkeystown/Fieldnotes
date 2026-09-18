---
order: 5
---
# Use this theme offline

This guide explains how to copy Fieldnotes to another computer and use it to **write, preview, and build documentation without internet access**. All theme styles, scripts, math fonts, and search assets are local.

The source project is `D:\Python\mkdocs_examples\offline_test`. Prepare a transfer folder on the connected computer, then carry that folder to the offline computer. You only need to prepare dependencies again if you change the target Python/platform or add packages.

## 1. Choose the destination environment

The theme files work on both tested platforms. The Python installation files must match the destination:

| Destination | Dependency kit in this project | Tested environment |
| --- | --- | --- |
| Windows x64, Python 3.14 | Root `requirements.lock` and `wheelhouse/` | Python 3.14.6 on Windows |
| RHEL 7 x86_64, Python 3.8 | `.artifacts/rhel7/requirements.lock`, `wheelhouse/`, and `bootstrap/` | UBI 7 / RHEL 7.9, Python 3.8.18, glibc 2.17 |

For the Linux row, `wheelhouse/` and `bootstrap/` are both **inside `.artifacts/rhel7/`**. Use the Linux lockfile with the Linux wheels; the root lockfile belongs to the Windows kit.

The RHEL test passed a fresh installation, build, and edit/rebuild with the container's network disabled. Python 3.6 is not supported by these kits. Other Python versions or architectures need a separately prepared and tested dependency kit.

!!! note "Python itself must already be available"
    The wheelhouse contains Python packages, not the Python interpreter. Before disconnecting, arrange a matching Python installation with `venv` and pip on the destination. If it is not installed, bring your approved offline Python installer or RPMs and their dependencies. You also need a local text editor and a browser. Node.js, npm, and a separate LaTeX installation are not needed.

## 2. Make a folder to transfer

The simplest starting point is a copy of this working documentation project. Keep its example pages until the offline installation is working, then replace them with your own.

Copy these files and folders:

| Copy | Purpose |
| --- | --- |
| `theme/` — the entire directory | Templates, light/dark styles, code styles, scripts, KaTeX, and all math fonts |
| `hooks/` | Generates search data locally during the build |
| `docs/` | Editable Markdown pages and local images/downloads |
| `mkdocs.yml` | Enables the theme, extensions, navigation, and search hook |
| `tools/` and `vendor-manifest.json` | Optional but recommended local asset and checksum checks |
| `LICENSE` | License for the original theme; the KaTeX license is already inside `theme/` |
| The matching dependency kit from step 1 | Allows installing the build tools offline |

Do not copy `.venv/`; create a new virtual environment on the destination. Git history is not required. A generated `site/` folder is optional for an authoring bundle because you will build it again.

### Copy the common project files

Run this example in PowerShell on the connected Windows computer. Change `D:\Transfer\my-docs` to your chosen transfer folder:

```powershell
cd D:\Python\mkdocs_examples\offline_test
$bundle = 'D:\Transfer\my-docs'
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

foreach ($item in @('theme', 'hooks', 'docs', 'tools',
                   'mkdocs.yml', 'vendor-manifest.json', 'LICENSE')) {
    Copy-Item -LiteralPath $item -Destination $bundle -Recurse -Force
}

New-Item -ItemType Directory -Path "$bundle\offline-packages" -Force | Out-Null
```

Now run **one** of the next two copy examples, depending on the destination.

### For a Windows / Python 3.14 destination

In the same PowerShell session:

```powershell
Copy-Item -LiteralPath 'requirements.lock' -Destination "$bundle\offline-packages"
Copy-Item -LiteralPath 'wheelhouse' -Destination "$bundle\offline-packages" -Recurse
Copy-Item -LiteralPath 'OFFLINE-KIT.txt' -Destination "$bundle\offline-packages"
```

### For a RHEL 7 / Python 3.8 destination

The Linux kit was generated during the Podman test. If it is missing, prepare it while connected using `tests/rhel7/run.ps1 -Prepare`; see [Container testing](container-test.md).

In the same PowerShell session:

```powershell
$linuxKit = '.artifacts\rhel7'
Copy-Item -LiteralPath "$linuxKit\requirements.lock" -Destination "$bundle\offline-packages"
Copy-Item -LiteralPath "$linuxKit\wheelhouse" -Destination "$bundle\offline-packages" -Recurse
Copy-Item -LiteralPath "$linuxKit\bootstrap" -Destination "$bundle\offline-packages" -Recurse
Copy-Item -LiteralPath "$linuxKit\checksums.json" -Destination "$bundle\offline-packages"
```

!!! warning "A Git clone does not include the prepared Linux kit"
    `.artifacts/` is ignored by Git. Copy the generated Linux files explicitly as shown above. Copying only the source repository will not provide the Linux installation packages.

Your transfer folder should now look like this:

```text
my-docs/
  mkdocs.yml
  docs/
  theme/
    assets/vendor/katex/
      fonts/
  hooks/
  tools/
  vendor-manifest.json
  LICENSE
  offline-packages/
    requirements.lock
    wheelhouse/
      ... .whl files ...
    bootstrap/                 Linux kit only: pip 24.3.1 wheel
```

A *wheel* (`.whl`) is a Python package installation file. Keep all wheels from the selected kit, including indirect dependencies.

Copy or zip the **whole `my-docs` folder** onto your approved transfer media. On the destination, extract it into a writable folder, preserving the directory structure. You do not need Podman on the destination to install directly into its matching Python environment.

## 3. Install on the offline computer

Use the instructions for the destination platform. The commands use the virtual environment's Python directly, so activation is not required.

### Windows with Python 3.14 x64

Open PowerShell in the copied project folder. This example assumes `C:\Docs\my-docs`:

```powershell
cd C:\Docs\my-docs
python --version
python -m venv .venv
.\.venv\Scripts\python -m pip install --no-index --no-cache-dir --find-links=offline-packages/wheelhouse -r offline-packages/requirements.lock
.\.venv\Scripts\python -m pip check
.\.venv\Scripts\python -m mkdocs build --strict
```

Confirm that `python --version` reports Python 3.14 before creating the environment. If multiple Pythons are installed, use the full path to the matching interpreter for the `venv` command.

### RHEL 7 with Python 3.8 x86_64

Open a terminal in the copied project folder. This example assumes `~/my-docs` and an available `python3.8` command:

```bash
cd ~/my-docs
python3.8 --version
python3.8 -m venv .venv
.venv/bin/python -m pip install --no-index --no-cache-dir --find-links=offline-packages/bootstrap pip==24.3.1
.venv/bin/python -m pip install --no-index --no-cache-dir --find-links=offline-packages/wheelhouse -r offline-packages/requirements.lock
.venv/bin/python -m pip check
.venv/bin/python -m mkdocs build --strict
```

The bundled pip wheel updates the environment's installer offline. This avoids using the older pip that may come with Python 3.8.

If Python was installed through Red Hat Software Collections, enable that collection in your shell first. Use the actual Python 3.8 executable on your machine in place of `python3.8`; the exact command depends on how Python was installed.

`--no-index` prevents pip from querying a package index. `--find-links` points it to the local installation files. None of these installation commands needs an online package download.

## 4. Write your documentation

Edit Markdown files inside `docs/` using your local text editor. Start by replacing `docs/index.md` with your own home page.

To add a page, create a file such as `docs/installation.md`, then add it to `nav` in `mkdocs.yml`:

```yaml
site_name: My Project Documentation
nav:
  - Home: index.md
  - Installation: installation.md
```

This is only the part of the configuration you change. Keep the theme, hooks, and Markdown extension settings already present in the copied `mkdocs.yml`. Update navigation when you remove example pages.

For code highlighting, put a language name such as `python`, `cpp`, or `bash` after the opening triple backticks. Use `$E = mc^2$` for inline math and `$$` delimiters for display math. See [Code & syntax](guide/code.md) and [Mathematics](guide/math.md) for complete examples.

The page's Light theme / Dark theme button changes its appearance. The browser remembers the choice when local storage is available.

### Preview while editing

On Windows:

```powershell
.\.venv\Scripts\python -m mkdocs serve
```

On RHEL/Linux:

```bash
.venv/bin/python -m mkdocs serve
```

Open the localhost address printed by MkDocs, normally `http://127.0.0.1:8000`. This connects to a server on your own computer; an internet connection is not needed. Save your Markdown changes to update the preview. Press Ctrl+C in the terminal to stop it.

## 5. Build and share the finished documentation

On Windows:

```powershell
.\.venv\Scripts\python -m mkdocs build --strict
.\.venv\Scripts\python tools/verify_offline.py
```

On RHEL/Linux:

```bash
.venv/bin/python -m mkdocs build --strict
.venv/bin/python tools/verify_offline.py
```

The verification command assumes the copied example's `site/` output and single `404.html` static template. If you change that structure or intentionally replace vendored assets, adjust the verification tool or manifest accordingly.

Open `site/index.html` directly in your browser. The theme, equations, highlighting, and search work from local files; you do not have to leave the preview server running.

To give someone **read-only documentation**, copy the entire generated `site/` folder. Readers only need a compatible browser. They do not need Python, MkDocs, the source theme, or the wheelhouse. Copying only `index.html` is insufficient because the other pages and assets live beside it.

To give someone an **editable project**, copy your source project and matching `offline-packages/` kit. They create their own virtual environment using step 3.

## Use the theme in an existing MkDocs project

Copy `theme/` and `hooks/` beside the existing project's `mkdocs.yml`, then install the matching dependencies from your local kit. The theme is supplied as a custom directory; there is no `pip install fieldnotes` step.

Use the following settings in that project's configuration, keeping its own `site_name` and `nav`:

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

Merge these settings into existing YAML keys instead of adding duplicate keys. If you keep additional plugins or extensions, include their dependencies in your offline kit and check whether they load remote resources.

`custom_dir` is relative to `mkdocs.yml`. Keep the theme folder outside `docs/`. Keep `use_directory_urls: false` for navigation that works when opening HTML files directly. Keep the search hook enabled so each build updates the local search index.

## Keep everything self-contained

- Store images and downloads inside `docs/` and reference them with relative paths.
- Keep the entire `theme/assets/vendor/katex/` directory, including `fonts/` and `LICENSE`.
- Use local CSS and JavaScript files when customizing the theme.
- Avoid remote fonts, CDN scripts, externally hosted images, and embedded online videos when their content must be available offline.
- When adding Python packages, prepare and transfer their compatible wheels before disconnecting.

Before transferring, test a fresh installation using your chosen kit and open the built documentation with external requests blocked. Check a math page, a highlighted code example, search, and both color themes. The theme has no CDN dependency, but content or plugins you add can introduce one.

## Common problems

| Problem | What to check |
| --- | --- |
| pip reports no matching distribution | Confirm Python version, OS, architecture, and that the lockfile and wheelhouse came from the same kit. |
| `venv` or pip is missing | Complete the destination's Python installation using the prepared installer/packages. The theme bundle does not supply Python itself. |
| The Linux kit is missing after a Git clone | Copy `.artifacts/rhel7/` dependencies from the connected preparation machine; they are ignored by Git. |
| Math appears as raw notation or missing glyphs | Check that Arithmatex is enabled and all KaTeX scripts, CSS, and fonts were copied. |
| Search is empty or broken | Keep `hooks/offline_search.py` enabled, rebuild, and check for `site/assets/search-index.js`. |
| Only the home page works after transfer | Copy the complete `site/` folder and keep `use_directory_urls: false`. |
| The theme cannot be found | Place `theme/` beside `mkdocs.yml` and set `theme.custom_dir: theme`. |
| Clipboard copying is restricted | Use the code block's text selection and your browser's copy command. |

For the repeatable RHEL 7 container check, see [Container testing](container-test.md). For template and color customization, see [Theme setup](theme-setup.md).
