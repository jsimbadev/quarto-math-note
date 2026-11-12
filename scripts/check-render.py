#!/usr/bin/env python3
"""Minimal post-render sanity: expected files and local HTML anchors."""
from pathlib import Path
from html.parser import HTMLParser

class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.references = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if 'id' in values:
            self.ids.add(values['id'])
        if tag == 'a' and values.get('href', '').startswith('#'):
            self.references.append(values['href'][1:])

def main():
    root = Path(__file__).resolve().parent.parent
    html, pdf = root / '_output/index.html', root / '_output/index.pdf'
    for path in (html, pdf):
        if not path.exists() or path.stat().st_size < 100:
            raise SystemExit(f'Missing or tiny rendered output: {path}')
    if pdf.read_bytes()[:4] != b'%PDF':
        raise SystemExit('PDF signature invalid')
    parser = Anchors()
    parser.feed(html.read_text(encoding='utf-8'))
    bad = sorted({ref for ref in parser.references if ref not in parser.ids})
    if bad:
        raise SystemExit('Broken local HTML anchors: ' + ', '.join(bad[:12]))
    print('Rendered HTML and PDF OK')

if __name__ == '__main__':
    main()
