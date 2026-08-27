import os, time, threading, requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN", "8186531834:AAE5g2j5R3c1p3S_x6tU1h5J6m7N8b9v0c1d2")
CHANNEL = os.environ.get("CHANNEL_ID", "@testbot999anunturi")
SITE_URL = "https://999.md/ro/list/transport-and-equipment/buses"
SEEN_FILE = "seen.txt"

def get_seen():
    if not os.path.exists(SEEN_FILE):
        return set()
    try:
        with open(SEEN_FILE, "r") as f:
            return set([x.strip() for x in f if x.strip()])
    except:
        return set()

def save_seen(link):
    try:
        with open(SEEN_FILE, "a") as f:
            f.write(link + "\n")
    except:
        pass

def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHANNEL, "text": text, "parse_mode": "HTML"}
        r = requests.post(url, data=data, timeout=15)
        print(f"Telegram raspuns: {r.status_code} - {r.text[:200]}")
        return r.status_code == 200
    except Exception as e:
        print(f"Eroare telegram: {e}")
        return False

def check_999():
    print(">>> Verific 999.md...")
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(SITE_URL, headers=headers, timeout=20)
        print(f"999.md status: {r.status_code}, lungime: {len(r.text)}")
        if r.status_code != 200:
            return
        seen = get_seen()
        print(f"Am deja {len(seen)} linkuri vazute")
        links = []
        # cauta linkuri
        import re
        found = re.findall(r'href="(/ro/[^"]+)"', r.text)
        for f in found:
            if "/booster" in f or "transport-and-equipment" in f or "/list/" in f:
                full = "https://999.md" + f
                if full not in seen and full not in links:
                    links.append(full)
        print(f"Am gasit {len(links)} linkuri noi potentiale")
        for link in links[:5]:
            titlu = link.split("/")[-1].replace("-", " ")[:100]
            msg = f"🚌 <b>Autobuz nou pe 999.md</b>\n\n{titlu}\n\n🔗 {link}"
            if send_telegram(msg):
                save_seen(link)
                print(f"Trimis: {link}")
                time.sleep(2)
            else:
                print(f"Nu am putut trimite: {link}")
    except Exception as e:
        print(f"Eroare check: {e}")

def loop():
    print(">>> Bot pornit! Verifica 999.md la fiecare 3 min")
    time.sleep(10)
    while True:
        check_999()
        time.sleep(180)

@app.route("/")
def home():
    return "Botul merge! Verifica logs"

threading.Thread(target=loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
