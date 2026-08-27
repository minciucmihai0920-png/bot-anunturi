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

URL = "https://999.md/ro/list/transport/cars"
SEEN_FILE = "seen.json"

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
    r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
    soup = BeautifulSoup(r.text, "html.parser")
    ads = []
    for a in soup.select("a[href*='/boletin/']"):
        title = a.get_text(strip=True)
        href = a.get("href")
        if not title or not href:
            continue
        ad_id = href
        ads.append({"id": ad_id, "title": title})
    return ads

def main():
    seen=load_seen()
    while True:
        try:
            ads=get_ads()
            new=[x for x in ads if x["id"] not in seen]
            for x in reversed(new):
                print(f"NOU: {x['title']}")
                seen.add(x["id"])
            if new: save_seen(seen)
        except Exception as e:
            print(e)
        time.sleep(300)

if __name__=="__main__":
    keep_alive()
    main()
