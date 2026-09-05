from utils import soup_from, text_or_none

BASE = "https://www.on3.com"

def fetch(cfg, overrides=None):
    url = (overrides or {}).get('url') or 'https://www.on3.com/college/new-mexico-lobos/category/basketball/news/'
    soup = soup_from(url, cfg)

    items = []
    for card in soup.select('article, .Card, .StoryCard, li, .post'):
        a = card.find('a', href=True)
        if not a: continue
        title = text_or_none(a)
        if not title: continue
        href = a['href']
        if href.startswith('/'): href = BASE + href
        date = None
        t = card.find('time')
        if t: date = t.get('datetime') or t.get_text(strip=True)
        items.append({'title': title, 'url': href, 'published': date, 'source': 'On3'})

    seen = set(); uniq = []
    for it in items:
        if it['url'] in seen: continue
        seen.add(it['url']); uniq.append(it)
    return uniq
