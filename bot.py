import os, sys, time, threading, requests
from bs4 import BeautifulSoup
from flask import Flask

print(">>> Pornesc botul...", flush=True)

TOKEN = os.environ.get("BOT_TOKEN", "")
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")
URL_SITE = "https://999.md/ro/list/real-estate/houses-and-villas?hide_dup=1&o_33_1=737&sort_type=price_asc&view_type=short"

HEADERS = {"User-Agent": "Mozilla/5.0"}
seen = set()
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot e LIVE! Verifica 999.md la 3 min."

def trimite(msg):
    if not TOKEN or not CHANNEL_ID:
        print("!!! LIPSESTE TOKEN sau CHANNEL_ID in Environment !!!", flush=True)
        return
    try:
        r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                          data={"chat_id": CHANNEL_ID, "text": msg, "parse_mode": "HTML"}, timeout=15)
        print(f"Telegram raspuns: {r.status_code} {r.text[:200]}", flush=True)
    except Exception as e:
        print(f"Eroare Telegram: {e}", flush=True)

def verifica():
    print(f">>> Verific 999.md ...", flush=True)
    try:
        resp = requests.get(URL_SITE, headers=HEADERS, timeout=30)
        print(f"999.md status: {resp.status_code}", flush=True)
        if resp.status_code != 200:
            return
        soup = BeautifulSoup(resp.text, "html.parser")
        anunturi = soup.select("a[href*='/ro/']") 
        gasite = 0
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "/ro/" in href and len(href) > 20:
                if href.startswith("/"): href = "https://999.md" + href
                if href not in seen:
                    titlu = a.get_text(strip=True)[:100]
                    if len(titlu) > 10:
                        seen.add(href)
                        gasite += 1
                        msg = f"🏠 <b>Anunt nou!</b>\n{titlu}\n{href}"
                        print(f"NOU: {titlu}", flush=True)
                        trimite(msg)
        if gasite == 0:
            print("Nimic nou.", flush=True)
    except Exception as e:
        print(f"Eroare verifica: {e}", flush=True)

def bucla():
    print(">>> Bot pornit! Verifica 999.md la fiecare 3 min", flush=True)
    trimite("✅ Botul a pornit si monitorizeaza 999.md (case Chisinau < 25k€)!")
    while True:
        verifica()
        time.sleep(180)

# PORNESTE THREAD-UL IMEDIAT, nu doar in __main__
threading.Thread(target=bucla, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
