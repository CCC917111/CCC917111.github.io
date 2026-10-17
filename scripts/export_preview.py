"""Export HTML previews that do not need sibling CSS or image files.

The live website keeps its shared stylesheet and static images. Previews embed
those display dependencies for single-file viewers; navigation and download
links point to the corresponding published pages and assets.
"""
from argparse import ArgumentParser
from base64 import b64encode
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import mimetypes

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://ccc917111.github.io/'
PAGES = ('index.html', 'research.html', 'publications.html', 'projects.html')


def local_asset(reference):
    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        raise ValueError(f'Expected a local display asset: {reference}')
    path = (ROOT / unquote(parsed.path)).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError(f'Asset missing or outside repository: {reference}')
    return path


def data_uri(reference):
    path = local_asset(reference)
    mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
    return f'data:{mime};base64,{b64encode(path.read_bytes()).decode("ascii")}'


class Preview(HTMLParser):
    def __init__(self, page):
        super().__init__(convert_charrefs=False)
        self.page = page
        self.parts = []

    def emit_tag(self, tag, attrs, closed=False):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            css = local_asset(attrs['href']).read_text()
            if '@import' in css or 'url(' in css or '</style' in css.lower():
                raise ValueError('Review stylesheet dependencies before exporting')
            self.parts.append('<style data-preview-source="assets/style.css">\n' + css + '</style>')
            return
        if tag == 'link' and attrs.get('rel') == 'icon':
            attrs['href'] = data_uri(attrs['href'])
        if tag == 'img' and attrs.get('src'):
            attrs['src'] = data_uri(attrs['src'])
            attrs.pop('loading', None)  # Single-file previews render every embedded image.
        if tag == 'source' and attrs.get('srcset'):
            candidates = []
            for candidate in attrs['srcset'].split(','):
                fields = candidate.strip().split()
                candidates.append(' '.join([data_uri(fields[0]), *fields[1:]]))
            attrs['srcset'] = ', '.join(candidates)
        if tag == 'a' and attrs.get('href'):
            href = attrs['href']
            if not href.startswith('#'):
                attrs['href'] = urljoin(SITE + self.page, href)
        if tag == 'svg' and 'icon-arrow' in attrs.get('class', '').split():
            attrs.setdefault('width', '12')
            attrs.setdefault('height', '12')
        formatted = ''.join(
            f' {key}' if value is None else f' {key}="{escape(value, quote=True)}"'
            for key, value in attrs.items())
        self.parts.append(f'<{tag}{formatted}{" /" if closed else ""}>')

    def handle_starttag(self, tag, attrs):
        self.emit_tag(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self.emit_tag(tag, attrs, closed=True)

    def handle_endtag(self, tag):
        self.parts.append(f'</{tag}>')

    def handle_data(self, data):
        self.parts.append(data)

    def handle_entityref(self, name):
        self.parts.append(f'&{name};')

    def handle_charref(self, name):
        self.parts.append(f'&#{name};')

    def handle_decl(self, decl):
        self.parts.append(f'<!{decl}>')

    def handle_comment(self, comment):
        self.parts.append(f'<!--{comment}-->')


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True,
                        help='New output directory outside the website checkout')
    args = parser.parse_args()
    destination = args.out.resolve()
    if destination.is_relative_to(ROOT):
        parser.error('Keep generated previews outside the published checkout')
    if any((destination / page).exists() for page in PAGES):
        parser.error('Preview files already exist; choose a new output directory')
    rendered = {}
    for page in PAGES:
        preview = Preview(page)
        preview.feed((ROOT / page).read_text())
        preview.close()
        rendered[page] = ''.join(preview.parts)
    destination.mkdir(parents=True, exist_ok=True)
    for page, content in rendered.items():
        (destination / page).write_text(content)
    print(f'Exported {len(rendered)} self-contained HTML previews to {destination}')


if __name__ == '__main__':
    main()
