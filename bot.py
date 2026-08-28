from flask import Flask
import os
import time
import threading
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # ex: @anunturi_ungheni sau -100123...

sent_ads = set()

def get_999_ads():
    try:
        url = "https://999.md/ro/list/real-estate/apartments?r=ungheni"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        ads = []
        for item in soup.select("a[href*='/boletin/']")[:5]:
            link = item.get("href")
            if not link.startswith("http"):
                link = "https://999.md" + link
            title = item.get_text(strip=True)[:100]
            if link not in sent_ads and title:
                ads.append((title, link))
        return ads
    except Exception as e:
        print(f"Eroare scraper: {e}")
        return []

def send_to_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHANNEL_ID, "text": text}
        requests.post(url, data=data, timeout=10)
        print(f"Trimis: {text[:50]}")
    except Exception as e:
        print(f"Eroare telegram: {e}")

def loop():
    while True:
        print("Caut anunturi...")
        ads = get_999_ads()
        for title, link in ads:
            msg = f"🏠 {title}\n\n🔗 {link}"
            send_to_telegram(msg)
            sent_ads.add(link)
            time.sleep(2
