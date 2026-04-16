import feedparser
import requests
from datetime import datetime

# Trusted RSS feeds
RSS_FEEDS = [
    "https://cointelegraph.com/rss",
    "https://cryptopotato.com/feed/",
    "https://decrypt.co/feed",
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
]

# X / Trend watchlist keywords (future ready layer)
WATCHLIST = [
    "binance",
    "coinbase",
    "ethereum",
    "solana",
    "base",
    "bitcoin",
    "airdrop",
    "hack",
    "listing",
]

def clean_text(text):
    if not text:
        return ""
    return text.replace("\n", " ").replace("\r", " ").strip()

def fetch_rss_news():
    items = []

    for url in RSS_FEEDS:
        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:
                title = clean_text(entry.get("title", ""))
                link = entry.get("link", "")
                published = entry.get("published", str(datetime.utcnow()))

                items.append({
                    "title": title,
                    "link": link,
                    "source": url,
                    "published": published,
                    "type": "rss"
                })

        except:
            pass

    return items

def fetch_trend_signals():
    # Placeholder trend layer
    # Future me real X scraping/API yaha add hoga
    signals = []

    for word in WATCHLIST:
        signals.append({
            "title": f"Trending talk around {word}",
            "link": "",
            "source": "X Trends",
            "published": str(datetime.utcnow()),
            "type": "trend"
        })

    return signals

def get_all_sources():
    data = []
    data.extend(fetch_rss_news())
    data.extend(fetch_trend_signals())
    return data