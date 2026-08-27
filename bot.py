import os, time, requests, threading
from bs4 import BeautifulSoup
from flask import Flask
import telebot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive! Ungheni"

def get_ads():
    try:
        print("Caut anunturi...")
        url = "https://999.md/ro/list/real-estate/apartments-and-rooms"
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            h = a['href']
            if '/ro/' in h and 'booster' not in h and len(h) > 25:
                if not h.startswith('http'):
                    h = 'https://999.md' + h
                links.append(h)
        return list(set(links))[:3]
    except Exception as e:
        print(e)
        return []

def loop():
    while True:
        try:
            ads = get_ads()
            for ad in ads:
                bot.send_message(CHANNEL_ID, f"🏠 Anunt nou!\n{ad}\n#Ungheni")
                print(f"Trimis {ad}")
                time.sleep(5)
            time.sleep(1800)
        except Exception as e:
            print(e)
            time.sleep(60)

threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
