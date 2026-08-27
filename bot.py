import requests, time, os, json
from bs4 import BeautifulSoup
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"
def run():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
def keep_alive():
    t = Thread(target=run)
    t.start()

URL = "https://999.md/ro/list/transport"
SEEN_FILE = "seen.json"
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL = os.environ.get("CHANNEL_ID")

def load_seen():
    if os.path.exists(SEEN_FILE):
        try:
            return set(json.load(open(SEEN_FILE)))
        except:
            return set()
    return set()

def save_seen(seen):
    json.dump(list(seen), open(SEEN_FILE, "w"))

def get_ads():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        ads = []
        for a in soup.select("a[href*='/bo']"):
            href = a.get("href")
            if not href: continue
            title = a.get_text(strip=True)
            if title and len(title) > 5:
                if "https" not in href:
                    href = "https://999.md" + href
                ads.append({"id": href, "title": title, "link": href})
        return ads[:10]
    except Exception as e:
        print(f"Eroare get_ads: {e}")
        return []

def send_telegram(text, link):
    if not TOKEN or not CHANNEL:
        print("Lipseste TOKEN sau CHANNEL!")
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHANNEL, "text": f"{text}\n\n{link}"}
        resp = requests.post(url, data=data, timeout=10)
        print(f"Telegram: {resp.text}")
    except Exception as e:
        print(f"Eroare telegram: {e}")

def main():
    seen = load_seen()
    print(f"Bot pornit! Văzute: {len(seen)} TOKEN setat: {bool(TOKEN)} CHANNEL: {CHANNEL}")
    while True:
        try:
            ads = get_ads()
            print(f"Găsite {len(ads)} anunțuri")
            new = [x for x in ads if x["id"] not in seen]
            print(f"NOI: {len(new)}")
            for x in reversed(new):
                print(f"NOU: {x['title']}")
                send_telegram(x['title'], x['link'])
                seen.add(x["id"])
                time.sleep(2)
            if new:
                save_seen(seen)
        except Exception as e:
            print(f"Eroare main: {e}")
        time.sleep(300)

if __name__=="__main__":
    keep_alive()
    main()
