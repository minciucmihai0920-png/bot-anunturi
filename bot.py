import requests
from bs4 import BeautifulSoup
import time
import threading
from flask import Flask
import os

print(">>> PORNESC BOTUL FINAL!!!", flush=True)

BOT_TOKEN = "8964072454:AAG98n3icTjE2IxksHhusnaR1v-rnbiC2Aw"
CHAT_ID = "-1003091041331"

URL_999 = "https://999.md/ro/search?hide_duplicates=yes&hide_outdated=yes&o_33_1=776&o_33_1=1065&r_6_1_unit=eur&r_6_1_from=0&r_6_1_to=25000&query=casa+Chisinau"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot e LIVE! Merge perfect"

trimise = set()

def trimite_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        # FARA HTML ca sa nu mai dea eroare
        r = requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
        print(f"Telegram: {r.status_code} {r.text[:400]}", flush=True)
        return True
    except Exception as e:
        print(f"Eroare TG: {e}", flush=True)
        return False

def verifica_999():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(URL_999, headers=headers, timeout=20)
        print(f"999 status: {r.status_code} len: {len(r.text)}", flush=True)
        soup = BeautifulSoup(r.text, 'html.parser')
        count = 0
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/ro/' in href and 'boletin' in href:
                full = href if 'https' in href else f"https://999.md{href}"
                if full not in trimise:
                    trimise.add(full)
                    trimite_telegram(f"CASA NOUA sub 25k Chisinau!\n\n{full}")
                    count += 1
                    if count >= 2:
                        break
        print(f"Verificare gata, trimise: {count}", flush=True)
    except Exception as e:
        print(f"Eroare 999: {e}", flush=True)

def bucla():
    print(">>> Trimit mesaj start", flush=True)
    time.sleep(3)
    trimite_telegram("BOTUL A PORNIT CU SUCCES! Monitorizez 999.md case Chisinau sub 25000 euro. Vei primi anunturi aici la 3 min!")
    while True:
        verifica_999()
        time.sleep(180)

threading.Thread(target=bucla, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
