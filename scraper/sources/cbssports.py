from ..utils import soup_from, text_or_none

BASE = "https://www.cbssports.com"

def fetch(cfg, overrides=None):
    url = (overrides or {}).get('url') or 'https://www.cbssports.com/college-basketball/teams/NMEX/new-mexico-lobos/'
    soup = soup_from(url, cfg)

    items = []
    for a in soup.select('a[href]'):
        href = a['href']; title = text_or_none(a)
        if not title: continue
        full = BASE + href if href.startswith('/') else href
        if 'college-basketball' in href and ('news' in href or '/teams/' in href or '/cbk/' in href):
            items.append({'title': title, 'url': full, 'published': None, 'source': 'CBS Sports'})
    seen = set(); uniq = []
    for it in items:
        if it['url'] in seen: continue
        seen.add(it['url']); uniq.append(it)
    return uniq
