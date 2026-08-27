import os, time, threading, requests
from bs4 import BeautifulSoup
import telebot
from flask import Flask
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
trimise = set()
def verifica_999():
    print(">>> Bot pornit! Verifica 999.md")
    while True:
        try:
            print("Verific 999.md...")
            url = "https://999.md/ro/list/transport/cars?r=ungheni"
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(r.text, 'html.parser')
            anunturi = soup.find_all('div', class_='ads-list-photo-item')[:5]
            print(f"Am gasit {len(anunturi)}")
            for a in anunturi:
                link_tag = a.find('a')
                if not link_tag: continue
                link = "https://999.md" + link_tag.get('href')
                if link in trimise: continue
                titlu = link_tag.get_text(strip=True) or "Anunt Ungheni"
                text = f"🚗 {titlu}\n🔗 {link}"
                bot.send_message(CHANNEL_ID, text)
                print(f"Trimis: {link}")
                trimise.add(link)
                time.sleep(2)
        except Exception as e:
            print(f"Eroare: {e}")
        time.sleep(300)
@app.route('/')
def home():
    return "Bot is alive! Ungheni"
threading.Thread(target=verifica_999, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
