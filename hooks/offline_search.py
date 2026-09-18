"""Build a script-based search index: works over file:// without fetch or workers."""
from html.parser import HTMLParser
from pathlib import Path
import json
_entries = []
class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
    def handle_data(self, data):
        self.parts.append(data)
def on_pre_build(config):
    _entries.clear()
def on_page_content(html, page, config, files):
    parser = Text()
    parser.feed(html)
    _entries.append(dict(title=page.title, url=page.url, text=' '.join(' '.join(parser.parts).split())))
    return html
def on_post_build(config):
    target = Path(config['site_dir']) / 'assets' / 'search-index.js'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text('window.FIELDNOTES_SEARCH = ' + json.dumps(_entries, ensure_ascii=True) + ';\n', encoding='utf-8')
