import os
import json
import time
import re
from pathlib import Path
from datetime import datetime, timedelta
from dateutil import parser as dateparser
import yaml

from sources.golobos import fetch as fetch_golobos
from sources.dailylobo import fetch as fetch_dailylobo
from sources.krqe import fetch as fetch_krqe
from sources.cbssports import fetch as fetch_cbssports
from sources.on3 import fetch as fetch_on3

from utils import load_config, normalize_url, ensure_dir

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data'
SITE_DIR = ROOT / 'site'

SOURCES = {
    'golobos': fetch_golobos,
    'dailylobo': fetch_dailylobo,
    'krqe': fetch_krqe,
    'cbssports': fetch_cbssports,
    'on3': fetch_on3,
}

def within_age(dt, max_age_days: int):
    if not isinstance(dt, datetime):
        return True
    return dt >= datetime.utcnow() - timedelta(days=max_age_days)

def render_html(items, generated_at):
    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>UNM Lobo Basketball News</title>
</head>
<body>
<h1>UNM Lobo Basketball News</h1>
<p>Updated {generated_at} UTC</p>
"""

    for item in items:
        title = item.get("title", "Untitled")
        url = item.get("url", "#")
        source = item.get("source", "")
        published = item.get("published", "")

        html += (
            f'<p>'
            f'{url}<a>{title}</a> '
            f'[{source}] {published}'
            f'</p>\n'
    )

    html += """
</body>
</html>
"""

    return html


def main():
    cfg = load_config(ROOT / 'config.yaml')
    ensure_dir(DATA_DIR)
    ensure_dir(SITE_DIR / 'assets')

    max_age = int(cfg.get('min_article_age_days', 120))
    max_items = int(cfg.get('max_items', 120))

    items = []
    for s in cfg.get('sources', []):
        name = s.get('name')
        if not s.get('enabled', True):
            continue
        fn = SOURCES.get(name)
        if not fn:
            continue
        try:
            fetched = fn(cfg, overrides=s.get('overrides') or {})
            items.extend(fetched)
        except Exception as e:
            print(f"[WARN] Source {name} error: {e}")

    # Deduplicate by normalized URL
    seen = set()
    deduped = []
    for it in items:
        u = normalize_url(it.get('url'))
        if not u or u in seen:
            continue
        seen.add(u)
        it['url'] = u
        deduped.append(it)

    # Filter by age
    filtered = []
    for it in deduped:
        pub = it.get('published')
        dt = None
        if pub:
            try:
                dt = dateparser.parse(pub)
            except Exception:
                dt = None
        if dt is None:
            filtered.append(it)
        else:
            if within_age(dt, max_age):
                filtered.append(it)

    # Sort newest first by published or fallback to now
    def sort_dt(it):
        try:
            return dateparser.parse(it.get('published'))
        except Exception:
            return datetime.utcnow()
    filtered.sort(key=sort_dt, reverse=True)

    # Trim
    filtered = filtered[:max_items]

    # Save data
    (ROOT / 'data').mkdir(parents=True, exist_ok=True)
    with open(ROOT / 'data' / 'articles.json', 'w', encoding='utf-8') as f:
        import json as _json
        _json.dump(filtered, f, ensure_ascii=False, indent=2)

    # Render HTML
    html = render_html(filtered, generated_at=datetime.utcnow().strftime('%Y-%m-%d %H:%M'))
    (ROOT / 'index.html').write_text(html, encoding='utf-8')

    # Write a minimal CSS if missing
    css_path = SITE_DIR / 'assets' / 'styles.css'
    if not css_path.exists():
        css_path.write_text("""
:root { --bg:#0b0b0b; --fg:#f5f5f5; --muted:#9aa0a6; --accent:#c00; }
* { box-sizing:border-box; }
body { margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; background:var(--bg); color:var(--fg); }
header { text-align:center; padding:24px 12px; border-bottom:1px solid #222; }
h1 { margin:0 0 8px; letter-spacing:.5px; }
.meta { color:var(--muted); margin:0; }
main { max-width: 900px; margin: 0 auto; padding: 20px 12px; }
.day { margin: 24px 0; }
.day h2 { font-size: 14px; color: var(--muted); font-weight:600; border-bottom:1px solid #222; padding-bottom:6px; }
ul { list-style:none; margin:0; padding:0; }
li { padding:10px 0; border-bottom:1px dotted #333; }
a { color:#9dd1ff; text-decoration:none; }
a:hover { text-decoration:underline; }
.src { color:#aaa; font-size:12px; margin-left:6px; }
time { color:#666; font-size:12px; margin-left:6px; }
footer { text-align:center; padding:20px; color:#666; border-top:1px solid #222; }
""", encoding='utf-8')

    print(f"Wrote {len(filtered)} items to index.html")

if __name__ == '__main__':
    main()
