import urllib.parse as urlparse
from pathlib import Path
import requests
import yaml
from bs4 import BeautifulSoup


def load_config(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def polite_get(url, cfg):
    headers = { 'User-Agent': cfg.get('user_agent', 'LoboNewsBot/1.0') }
    timeout = cfg.get('request_timeout', 20)
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp


def soup_from(url, cfg):
    resp = polite_get(url, cfg)
    return BeautifulSoup(resp.text, 'lxml')


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def normalize_url(u: str):
    if not u:
        return None
    u = u.strip()
    # Remove tracking parameters
    parsed = urlparse.urlparse(u)
    clean = parsed._replace(query='', fragment='')
    return urlparse.urlunparse(clean)


def text_or_none(el):
    if not el:
        return None
    t = el.get_text(strip=True)
    return t or None
