import os
import time
import threading
import requests
import feedparser
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL_USERNAME")

app = Flask(name)

@app.route("/")
def home():
    return "Friend Chain AI Running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

sent_titles = set()

RSS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss",
    "https://decrypt.co/feed"
]

KEYWORDS = [
    "bitcoin", "etf", "binance", "coinbase", "hack",
    "sec", "ethereum", "solana", "partnership",
    "launch", "airdrop", "listing", "whale"
]

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL,
        "text": msg,
        "disable_web_page_preview": False
    }
    requests.post(url, data=data, timeout=20)

def important(title):
    t = title.lower()
    return any(k in t for k in KEYWORDS)

def fetch_news():
    for feed_url in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                title = entry.title.strip()
                link = entry.link.strip()

                if title in sent_titles:
                    continue

                if important(title):
                    sent_titles.add(title)
                    return title, link
        except:
            pass
    return None, None

threading.Thread(target=run_web).start()
print("Friend Chain AI Smart News Started")

while True:
    title, link = fetch_news()

    if title:
        msg = f"🚨 Smart Crypto Alert\n\n{title}\n\n{link}"
        send_telegram(msg)
        print("Posted:", title)

    time.sleep(900)