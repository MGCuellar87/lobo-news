from ..utils import soup_from, text_or_none

BASE = "https://golobos.com"

def fetch(cfg, overrides=None):
    url = (overrides or {}).get('url') or 'https://golobos.com/sports/mbball/news'
    soup = soup_from(url, cfg)

    items = []
    for a in soup.select('a'):
        href = a.get('href') or ''
        title = text_or_none(a)
        if not href or not title:
            continue
        if '/sports/mbball/' in href or '/mbball/' in href or '/sports/m-basketball/' in href:
            if href.startswith('/'):
                href = BASE + href
            date = None
            parent = a.find_parent(['article','div','li'])
            if parent:
                dt = parent.find('time')
                if dt and (dt.get('datetime') or dt.text):
                    date = dt.get('datetime') or dt.text
            items.append({
                'title': title,
                'url': href,
                'published': date,
                'source': 'GoLobos',
            })
    seen = set(); uniq = []
    for it in items:
        if it['url'] in seen: continue
        seen.add(it['url']); uniq.append(it)
    return uniq
