import requests
from bs4 import BeautifulSoup
import time
import threading
from flask import Flask
import os

print(">>> BOT FINAL PORNESTE!!!", flush=True)

BOT_TOKEN = "8964072454:AAG98n3icTjE2IxksHhusnaR1v-rnbiC2Aw"
CHAT_ID = "-1004373402641"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot LIVE - ID corect!"

trimise = set()

def trimite_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
        print(f"Telegram: {r.status_code} {r.text[:500]}", flush=True)
        return r.status_code == 200
    except Exception as e:
        print(f"Eroare TG: {e}", flush=True)
        return False

def verifica_999():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = "https://999.md/ro/list/real-estate/houses-and-villas?o_33_1=776"
        r = requests.get(url, headers=headers, timeout=20)
        print(f"999 status: {r.status_code} len: {len(r.text)}", flush=True)
        soup = BeautifulSoup(r.text, 'html.parser')
        gasite = 0
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/ro/' in href and len(href) > 20 and ('boletin' in href or '/apartment' in href or href.count('/') >= 3):
                full = href if 'https' in href else f"https://999.md{href}"
                if '999.md' in full and full not in trimise and len(full) < 150:
                    # filtram doar linkuri de anunt
                    if any(x in full for x in ['/ro/', 'boletin']):
                        trimise.add(full)
                        gasite += 1
                        trimite_telegram(f"CASA NOUA Chisinau!\n\n{full}\n\nPret <25k - verifica rapid!")
                        time.sleep(1)
                        if gasite >= 3:
                            break
        print(f"Verificare gata, gasite noi: {gasite}, total trimise: {len(trimise)}", flush=True)
    except Exception as e:
        print(f"Eroare: {e}", flush=True)

def bucla():
    time.sleep(3)
    print(">>> Trimit mesaj START pe canalul vinzare123", flush=True)
    trimite_telegram("✅ BOTUL A PORNIT CU SUCCES pe canalul vinzare123!\n\nMonitorizez 999.md case Chisinau sub 25k euro la 3 minute!\n\nVei primi anunturi automat aici! 🏠")
    while True:
        verifica_999()
        time.sleep(180)

threading.Thread(target=bucla, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
