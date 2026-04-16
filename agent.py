import os
import time
import requests
import threading
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
 return "Friend Chain AI Running"

def run_web():
 port = int(os.environ.get("PORT", 10000))
 app.run(host="0.0.0.0", port=port)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL_USERNAME")

last_post = ""

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHANNEL,
        "text": msg,
        "disable_web_page_preview": True
    }
    requests.post(url, data=data)

def get_btc_price():
    try:
        r = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
        price = r.json()["bitcoin"]["usd"]
        return price
    except:
        return None
threading.Thread(target=run_web).start()
print("Friend Chain AI Started")

while True:
    price = get_btc_price()

    if price:
        msg = f"Friend Chain AI Update\n\nBitcoin Price: ${price}\n\nStay sharp."

        if msg != last_post:
            send_telegram(msg)
            last_post = msg
            print("Posted:", msg)

    time.sleep(3600)