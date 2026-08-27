import requests
from bs4 import BeautifulSoup
import time
import threading
from flask import Flask
import os

print(">>> PORNESC BOTUL CU TOKEN NOU!!!", flush=True)

BOT_TOKEN = "8964072454:AAG98n3icTjE2IxksHhusnaR1v-rnbiC2Aw"
CHAT_ID = "-1003091041331"
URL_999 = "https://999.md/ro/list/real-estate/houses-and-villas?hide_duplicates=yes&hide_outdated=yes&o_33_1=776&o_33_1=1065&r_6_1_unit=eur&r_6_1_from=0&r_6_1_to=25000"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot e LIVE! Verifica Telegram - case Chisinau <25k"

trimise = set()

def trimite_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=10)
        print(f"Telegram: {r.status_code} {r.text[:300]}", flush=True)
        return r.status_code == 200
    except Exception as e:
        print(f"Eroare: {e}", flush=True)
        return False

def verifica_999():
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        r = requests.get(URL_999, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, 'html.parser')
        print(f"999.md status: {r.status_code}, lungime: {len(r.text)}", flush=True)
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/boletin/' in href or '/ro/' in href and len(href) > 25 and '999.md' in href or href.startswith('/ro/'):
                full = href if '999.md' in href else f"https://999.md{href}"
                if full not in trimise and 'real-estate' in full or 'boletin' in full:
                    trimise.add(full)
                    msg = f"🏠 <b>CASA NOUA <25k€ Chisinau!</b>\n\n{full}\n\n#chisinau #casa"
                    trimite_telegram(msg)
                    time.sleep(1)
    except Exception as e:
        print(f"Eroare verificare 999: {e}", flush=True)

def bucla():
    print(">>> Bucla pornita - trimit mesaj de start", flush=True)
    time.sleep(5)
    trimite_telegram("✅ <b>BOTUL A PORNIT CU SUCCES!</b>\n\nMonitorizez 999.md - case Chisinau < 25.000€\nVerific la fiecare 3 minute.\n\nO sa primesti anunturi aici automat! 🏠")
    while True:
        verifica_999()
        time.sleep(180)

threading.Thread(target=bucla, daemon=True).start()
print(">>> Thread pornit!", flush=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
