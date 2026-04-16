import os
import time
import threading
import requests
from flask import Flask
from dotenv import load_dotenv
from datetime import datetime

from sources import get_all_sources
from filters import get_best_items
from formatter import format_post, format_recap
from memory import already_sent, mark_sent, get_today_posts, clear_today_posts

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL_USERNAME")

app = Flask(__name__)

@app.route("/")
def home():
    return "Friend Chain AI Running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHANNEL,
        "text": msg,
        "disable_web_page_preview": False
    }

    try:
        requests.post(url, data=data, timeout=20)
    except:
        pass

def run_alert_cycle():
    raw_items = get_all_sources()
    best_items = get_best_items(raw_items, limit=5)

    for item in best_items:
        title = item["title"]

        if not already_sent(title):
            msg = format_post(item)
            send_telegram(msg)
            mark_sent(title)
            print("Posted:", title)
            break

def run_daily_recap():
    posts = get_today_posts()

    if posts:
        fake_items = [{"title": x} for x in posts[:5]]
        msg = format_recap(fake_items)
        send_telegram(msg)

    clear_today_posts()

def scheduler():
    last_recap_day = None

    while True:
        try:
            run_alert_cycle()

            now = datetime.utcnow()
            today = now.strftime("%Y-%m-%d")

            # Daily recap at 18:00 UTC
            if now.hour == 18 and last_recap_day != today:
                run_daily_recap()
                last_recap_day = today

        except Exception as e:
            print("Error:", e)

        time.sleep(300)

threading.Thread(target=run_web).start()
print("Friend Chain AI Elite System Started")

scheduler()