"""Check the generated site's local dependency closure using the standard library."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import hashlib, json, re
root = Path(__file__).resolve().parents[1]
site = root / 'site'
errors = []
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]; self.ids=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        for key in ('src','href','poster'):
            if a.get(key): self.refs.append((tag, key, a[key]))
pages={}
for path in site.rglob('*.html'):
    parser=Page(); parser.feed(path.read_text(encoding='utf-8')); pages[path.resolve()]=parser
if not pages: errors.append('No built HTML pages found')
def check(path, ref, asset=True):
    url=urlsplit(ref)
    if url.scheme or url.netloc:
        if asset and url.scheme not in ('data',): errors.append(f'Remote asset: {path}: {ref}')
        return
    target=(path.parent/unquote(url.path)).resolve() if url.path else path.resolve()
    if target.is_dir(): target=target/'index.html'
    if not target.is_file(): errors.append(f'Missing local file: {path}: {ref}')
    elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
        errors.append(f'Missing anchor: {path}: {ref}')
for path, parser in pages.items():
    for tag,key,ref in parser.refs: check(path,ref,tag!='a')
for path in site.rglob('*.css'):
    css=path.read_text(encoding='utf-8')
    for ref in re.findall(r'url\([\s\"\']*([^\)\"\']+)',css): check(path,ref.strip())
    if re.search(r'@import\s+[\"\']https?:',css): errors.append(f'Remote CSS import: {path}')
manifest=json.loads((root/'vendor-manifest.json').read_text())
for name, expected in manifest['files'].items():
    if hashlib.sha256((root/name).read_bytes()).hexdigest()!=expected: errors.append(f'Vendor checksum mismatch: {name}')
index=(site/'assets/search-index.js').read_text(encoding='utf-8')
entries=json.loads(index.split(' = ',1)[1].rstrip(';\n'))
for entry in entries: check(site/'index.html',entry['url'])
if len(entries)!=len(pages)-1: errors.append('Search index does not cover every documentation page')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: {len(pages)} HTML pages, {len(entries)} search entries, {len(manifest["files"])} vendored checksums; all HTML assets, links, anchors, and CSS fonts resolve locally.')
