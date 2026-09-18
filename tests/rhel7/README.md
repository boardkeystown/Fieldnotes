# RHEL 7 / Python 3.8 offline container test

Run from PowerShell in the project root after starting Podman's machine:

```powershell
# First run: download the image and Linux wheels, then test offline.
.\tests\rhel7\run.ps1 -Prepare

# Repeat with no downloads and container networking disabled.
.\tests\rhel7\run.ps1
```

The project is mounted read-only. The test copies it into a temporary container directory, creates a fresh Python virtual environment, installs from local wheels with `--no-index --no-cache-dir`, builds with `--strict`, checks local assets and links, edits a temporary Markdown page, and rebuilds. It verifies that only the loopback network interface exists and an outbound connection fails.

`requirements.in` selects Python 3.8-compatible direct dependencies. Preparation records the full resolved versions in `requirements.lock`. It uses PyMdown Extensions 10.15; the main Windows setup remains on 10.16.1. The generated Linux kit lives in `.artifacts/rhel7/` and is separate from the Windows `wheelhouse/`.

Outputs:

- `.artifacts/rhel7/result.json`: environment and test results.
- `.artifacts/rhel7/site/index.html`: container-built documentation.
- `.artifacts/rhel7/wheelhouse/`: Linux/Python 3.8 packages.
- `.artifacts/rhel7/bootstrap/`: a Python 3.8-compatible pip wheel.
- `.artifacts/rhel7/checksums.json`: downloaded wheel and lockfile checksums.

For a disconnected machine, transfer the project and `.artifacts/rhel7` kit, and export/import the image using `podman save` / `podman load`. The offline run uses `--pull=never --network=none`. Preparation needs network access; verification does not. Podman must already be installed with its machine initialized on Windows.

This checks RHEL 7 userspace, Python, package compatibility, and offline builds. It does not reproduce the RHEL 7 kernel or desktop browser. Browser rendering must be checked separately.

See [the recorded passing test](RESULTS.md) for exact versions, checks, and limitations.
