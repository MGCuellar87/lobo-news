from utils import soup_from, text_or_none

BASE = "https://www.dailylobo.com"

def fetch(cfg, overrides=None):
    url = (overrides or {}).get('url') or 'https://www.dailylobo.com/section/mens-basketball'
    soup = soup_from(url, cfg)

    items = []
    for card in soup.select('article, .card, .river, .story, li'):
        a = card.find('a', href=True)
        if not a: continue
        href = a['href']; title = text_or_none(a)
        if not title: continue
        if href.startswith('/'): href = BASE + href
        date = None
        t = card.find('time')
        if t: date = t.get('datetime') or t.get_text(strip=True)
        items.append({'title': title, 'url': href, 'published': date, 'source': 'Daily Lobo'})

    if not items:
        for a in soup.select('a[href]'):
            href = a['href']
            if '/article/' in href:
                title = text_or_none(a)
                if not title: continue
                if href.startswith('/'): href = BASE + href
                items.append({'title': title, 'url': href, 'published': None, 'source': 'Daily Lobo'})

    seen = set(); uniq = []
    for it in items:
        if it['url'] in seen: continue
        seen.add(it['url']); uniq.append(it)
    return uniq
