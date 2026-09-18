# Verified result

Result: **PASS**

- Tested at: 2026-09-18T02:46:31.765062+00:00
- Container: Red Hat UBI 7, RHEL 7.9 userspace, x86_64.
- Python: 3.8.18; glibc: 2.17; MkDocs: 1.6.1.
- PyMdown Extensions: 10.15; Pygments: 2.19.2.
- Podman on Windows: 6.0.2, WSL machine, rootless containers.
- Pinned image digest: `registry.access.redhat.com/ubi7/python-38@sha256:6d8cf22d54a80f6e1c9ef394ed155fe9fe12864aa3b5f25547c149bd87ff8a89`.

The fresh test container ran with `--pull=never --network=none`. Only the loopback interface existed, and an outbound TCP connection returned errno 101 (network unreachable). It created an isolated virtual environment and installed pip plus 20 dependencies from local wheels using `--no-index`, with pip caching disabled. Dependency checks, a strict build, local asset/link/font checks, and an offline Markdown edit/rebuild passed. The search index included the edited text.

Eight HTML pages, seven search entries, and 64 vendored asset checksums were verified.

A separate headless Microsoft Edge test on Windows opened the container-generated output via `file://`, with HTTP/HTTPS requests blocked. Math samples, highlighted code, copy buttons, nested-page search, theme switching/persistence, and mobile navigation passed. No external HTTP requests or JavaScript page errors occurred.

The Windows mount initially rejected pip's attempt to change file permissions. The test now downloads into the container's Linux filesystem and exports file contents without trying to preserve Linux permissions on Windows.

This establishes the tested RHEL 7 userspace/Python 3.8 build and the output's behavior in Windows Edge. It does not establish Python 3.6 compatibility or the behavior of an old RHEL desktop browser/kernel.

To repeat the prepared offline test from the project root:

```powershell
.\tests\rhel7\run.ps1
```

The full generated environment report is `.artifacts/rhel7/result.json`; the output is `.artifacts/rhel7/site/index.html`. These generated artifacts are ignored by Git. The reusable test, pinned image, and dependency lockfile are source files under `tests/rhel7/`.
