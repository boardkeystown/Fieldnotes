# Verification

- Strict MkDocs build passed.
- Eight generated HTML pages, seven search entries, and 64 vendored file checksums checked.
- Every HTML asset, internal link, anchor, and CSS font reference resolves locally.
- Headless Microsoft Edge opened the site through file URLs with all HTTP/HTTPS requests blocked.
- Inline and display equations, aligned equations, matrices, and cases rendered successfully.
- Code token highlighting, copy button, nested-page search, dark/light toggling, saved appearance, and mobile navigation passed.
- No external HTTP requests and no JavaScript page errors were observed.
- Light, dark, and mobile screenshots visually reviewed.

Run tools/verify_offline.py after changing content or theme assets. The dependency kit targets CPython 3.14 on Windows x64; a different target needs matching wheels.

Verified project root: D:\Python\mkdocs_examples\offline_test
Fresh installation completed using --no-index --no-cache-dir and the bundled wheelhouse.


## RHEL 7 / Python 3.8

Passed an actual Podman test on UBI 7 (RHEL 7.9, Python 3.8.18, glibc 2.17). Fresh installation, build, and Markdown edit/rebuild passed with networking disabled. The generated output separately passed Windows Edge checks with external requests blocked. See [the detailed container result](tests/rhel7/RESULTS.md).
