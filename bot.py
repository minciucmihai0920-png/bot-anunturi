import os, requests, time, threading
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)
trimise = set()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def trimite_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text})
    except: pass

def verifica_999():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get("https://999.md/ro/list", headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        gasite = 0
        for a in soup.find_all('a', href=True):
            href = a['href']
            full = href if 'https' in href else f"https://999.md{href}"
            # Vrem doar anunturi reale, nu blog/info
            if '/blog' in full: continue
            if '/info' in full: continue
            if '/ro/' not in full: continue
            if full.count('/') < 4: continue
            if len(full) < 30: continue
            if full in trimise: continue
            if '999.md' not in full: continue
            
            # Doar daca pare anunt (are cifre in link)
            if not any(c.isdigit() for c in full[-15:]):
                continue

            print(f"ANUNT GASIT: {full}", flush=True)
            trimise.add(full)
            trimite_telegram(f"🏠 ANUNT NOU 999.md\n\n{full}")
            gasite += 1
            time.sleep(1)
            if gasite >= 3: break
        print(f"Gata, gasite noi: {gasite}", flush=True)
    except Exception as e:
        print(f"Eroare: {e}", flush=True)

def bucla():
    time.sleep(5)
    trimite_telegram("✅ BOT FINAL PORNIT - trimite doar anunturi reale, fara bloguri")
    while True:
        verifica_999()
        time.sleep(180)

threading.Thread(target=bucla, daemon=True).start()

@app.route('/')
def home():
    return "Bot online!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
