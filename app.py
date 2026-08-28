import os
import time
import threading
import requests
from bs4 import BeautifulSoup
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
sent_ads = set()
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot ANUNTURI e viu!"

def get_999_ads():
    try:
        url = "https://999.md/ro/list/real-estate/apartments-and-rooms?o_33_1=776&oi_33_1=779"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        ads = []
        for item in soup.select("a[href*='/boletin/']"):
            link = item.get("href")
            if not link: continue
            if not link.startswith("http"): link = "https://999.md" + link
            title = item.get_text(strip=True)
            if len(title) < 10: continue
            ads.append((title, link))
            if len(ads) >= 3: break
        return ads
    except: return []

def send_to_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHANNEL_ID, "text": text}, timeout=10)
    except: pass

def loop():
    while True:
        for title, link in get_999_ads():
            if link in sent_ads: continue
            send_to_telegram(f"🏠 {title}\n\n🔗 {link}")
            sent_ads.add(link)
            time.sleep(2)
        time.sleep(60)

threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
