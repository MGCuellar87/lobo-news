# Lobo News Aggregator (Scraper-Only)

A simple, automated **UNM Lobo men's basketball** news aggregator that scrapes multiple public sources and generates a single static page (Drudge-style) of latest headlines. No RSS, no APIs — just HTML scraping with respectful rate limiting and `robots.txt` checks.

## Features
- Scrapes multiple sources and extracts **title, URL, and publish date (if available)**
- De-duplicates by canonical URL
- Sorts newest first
- Generates a single static HTML page: `site/index.html`
- Can run on a schedule via **GitHub Actions** and auto-commit updates

## Sources (preconfigured)
- GoLobos – Men's Basketball news (official athletics)  
  https://golobos.com/sports/mbball/news  
- The Daily Lobo – Men's Basketball section  
  https://www.dailylobo.com/section/mens-basketball  
- KRQE – Local Sports (filtered for Lobo mentions)  
  https://www.krqe.com/sports/local-sports/  
- CBS Sports – New Mexico Lobos team page  
  https://www.cbssports.com/college-basketball/teams/NMEX/new-mexico-lobos/  
- On3 – New Mexico Lobos Basketball news  
  https://www.on3.com/college/new-mexico-lobos/category/basketball/news/

> **Note:** HTML structures on news sites change. This starter includes resilient selectors and fallback heuristics, plus a configuration file where you can adjust patterns without editing code.

## Local Setup

```bash
# 1) Create and activate a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the scraper
python scraper/main.py

# 4) Open the generated site
open site/index.html  # Windows: start site\index.html
```

## Configuration
Edit `config.yaml` to tweak:
- `min_article_age_days` — exclude very old items
- `max_items` — total items on homepage
- `sources` — enable/disable sources and override selectors

## Deploy to GitHub Pages (auto)
1. Create a public repo and push this project.
2. Enable **Pages**: Settings → Pages → Build from branch → `main` → `/root` (or `docs` if you prefer).
3. The included workflow `.github/workflows/scrape.yml` runs every 30 minutes, scrapes, rebuilds `site/index.html`, and commits changes back to `main`.

> If your repo is private, ensure Pages is allowed and the workflow has the right permissions. The default `GITHUB_TOKEN` is used to commit.

## Respect & Legal
- This project only stores **metadata** (title, link, date) and does not republish article text.
- It makes limited, polite requests and honors `robots.txt` where applicable.
- Always review each site's Terms of Service for scraping policies.

## Troubleshooting
- **No items from a source?** Update selectors in `config.yaml` or in the corresponding `scraper/sources/*.py` file.
- **Bad dates?** Some sites don’t expose publish dates in listings; the scraper falls back to current time.
- **Selectors changed?** Inspect the site’s HTML (right-click → Inspect) and update `article_selector`, `title_selector`, or `date_selector`.

---
Generated on 2026-02-18.
