from ..utils import soup_from, text_or_none

BASE = "https://www.krqe.com"

def fetch(cfg, overrides=None):
    url = (overrides or {}).get('url') or 'https://www.krqe.com/sports/local-sports/'
    soup = soup_from(url, cfg)

    keywords = ['lobo', 'lobos', 'new mexico', 'unm']

    items = []
    for card in soup.select('article, .article, .post, .card, li'):
        a = card.find('a', href=True)
        if not a: continue
        title = text_or_none(a)
        if not title: continue
        tit = title.lower()
        if not any(k in tit for k in keywords): continue
        href = a['href']
        if href.startswith('/'): href = BASE + href
        date = None
        t = card.find('time')
        if t: date = t.get('datetime') or t.get_text(strip=True)
        items.append({'title': title, 'url': href, 'published': date, 'source': 'KRQE'})

    seen = set(); uniq = []
    for it in items:
        if it['url'] in seen: continue
        seen.add(it['url']); uniq.append(it)
    return uniq
