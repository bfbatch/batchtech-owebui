# BATCHTECH: BatchTechUI's own version, separate from the upstream Open WebUI version in package.json.
# Upstream merges bump package.json only; this number changes only when a BatchTechUI release is cut.
from pathlib import Path

try:
    BATCHTECH_VERSION = (Path(__file__).parent / 'BATCHTECH_VERSION').read_text().strip() or '0.0.0'
except Exception:
    BATCHTECH_VERSION = '0.0.0'


def _load_changelog():
    """BatchTechUI's own release notes in the shape /api/changelog returns (same as the upstream CHANGELOG.md parser)."""
    try:
        import markdown
        from bs4 import BeautifulSoup

        text = (Path(__file__).parent / 'BATCHTECH_CHANGELOG.md').read_text(encoding='utf8')
        soup = BeautifulSoup(markdown.markdown(text), 'html.parser')
        out = {}
        for h2 in soup.find_all('h2'):
            parts = h2.get_text().strip().split(' - ')
            if len(parts) < 2:
                continue
            entry = {'date': parts[1]}
            node = h2.find_next_sibling()
            while node and node.name != 'h2':
                if node.name == 'h3':
                    ul = node.find_next_sibling('ul')
                    items = []
                    for li in ul.find_all('li') if ul else []:
                        items.append(
                            {'title': '', 'content': li.get_text(' ', strip=True), 'raw': li.decode_contents()}
                        )
                    entry[node.get_text().lower()] = items
                node = node.find_next_sibling()
            out[parts[0][1:-1]] = entry
        return out
    except Exception:
        return {}


BATCHTECH_CHANGELOG = _load_changelog()
