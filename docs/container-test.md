---
order: 7
---
# Test with Podman

Build and edit this documentation inside a RHEL 7-based container running Python 3.8, with networking disabled during verification.

## Prepare Podman

On Windows, Podman uses a Linux machine to run containers. If you have just installed Podman and have no machine yet, initialize and start one:

```powershell
podman machine init --cpus 2 --memory 2048 --disk-size 20
podman machine start
```

Use `podman machine list` to check existing machines first. This project's test script can also locate the per-user Podman installation if a newly opened terminal has not picked up PATH changes.

## First run while connected

From `D:\Python\mkdocs_examples\offline_test`, run:

```powershell
.\tests\rhel7\run.ps1 -Prepare
```

This downloads the pinned UBI 7/Python 3.8 image and resolves Linux dependencies. It then starts a fresh container with networking disabled to run the actual test. The Python 3.8 dependency set is separate from the main Windows environment.

## Repeat the offline test

```powershell
.\tests\rhel7\run.ps1
```

The script uses `--pull=never --network=none`. It checks that only the loopback interface exists, creates a fresh virtual environment, installs from the downloaded wheels with `--no-index --no-cache-dir`, and builds with `--strict`. It also edits a temporary copy of the home page and rebuilds to check offline authoring and search indexing.

Your source project is mounted read-only. The modified page is only in the test copy.

## Find the results

The test writes the following files under the project root:

```text
.artifacts/rhel7/
  result.json          Test results and environment versions
  requirements.lock    Resolved Linux/Python 3.8 dependencies
  checksums.json       Package checksums
  bootstrap/           Offline pip installer
  wheelhouse/          Linux dependency wheels
  site/index.html      Documentation built inside the container
```

Open `.artifacts/rhel7/site/index.html` in your browser to inspect the output. Test browser rendering with external requests blocked as a separate step; disabling the container's network does not disable the host browser's network.

## What this establishes

A successful run checks the RHEL 7 user-space libraries, Python 3.8 packages, local assets, offline installation, and documentation builds. It does not emulate the RHEL 7 kernel or its desktop browser, and it does not test Python 3.6.

The image is pinned by digest in `tests/rhel7/image.txt`. The complete resolved dependency set is saved in `tests/rhel7/requirements.lock`. See `tests/rhel7/README.md` for repeatable test details and transferring the kit to another machine.
