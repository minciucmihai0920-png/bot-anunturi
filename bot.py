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
        requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"})
    except: pass

def verifica_999():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = "https://999.md/ro"
        r = requests.get(url, headers=headers, timeout=10)
        print(f"999 status: {r.status_code}", flush=True)
        soup = BeautifulSoup(r.text, 'html.parser')
        gasite = 0
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/ro/' in href and len(href) > 20:
                full = href if 'https' in href else f"https://999.md{href}"
                if '999.md' in full and full not in trimise:
                    # DOAR anunturi, nu pagini info
                    if '/info' in full or '/pages' in full or '/help' in full or 'privacy' in full:
                        continue
                    if '/ro/' in full and full.count('/') >= 4:
                        print(f"ANUNT GASIT: {full}", flush=True)
                        trimise.add(full)
                        gasite += 1
                        trimite_telegram(f"ANUNT NOU!\n\n{full}")
                        time.sleep(1)
                        if gasite >= 3:
                            break
        print(f"Verificare gata, gasite noi: {gasite}", flush=True)
    except Exception as e:
        print(f"Eroare: {e}", flush=True)

def bucla():
    time.sleep(3)
    print(">>> Trimit mesaj START pe canalul vinzare", flush=True)
    trimite_telegram("✅ BOTUL A PORNIT CU SUCCES - Acum trimite ORICE anunt de pe 999.md")
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
