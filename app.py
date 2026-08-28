import os, threading, time, requests
from flask import Flask
from bs4 import BeautifulSoup

app = Flask(__name__)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
vazute = set()

@app.route('/')
def home():
    return "Bot LIVE - Toate anunturile 999"

def trimite(titlu, link):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        text = f"📢 {titlu}\n\n🔗 {link}"
        requests.post(url, data={"chat_id": CHANNEL_ID, "text": text}, timeout=10)
    except: pass

def loop():
    while True:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get("https://999.md/ro/list", headers=headers, timeout=20)
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a", href=True)[:40]:
                href = a["href"]
                if "/boletin/" in href:
                    link = "https://999.md" + href if href.startswith("/") else href
                    tit = a.get_text(strip=True)[:80]
                    if link not in vazute and len(tit) > 5:
                        vazute.add(link)
                        trimite(tit, link)
        except Exception as e:
            print(e)
        time.sleep(60)

threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
