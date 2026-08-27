import requests, time, os, json
from bs4 import BeautifulSoup

URL = "https://999.md/ro/list/transport/cars"
SEEN_FILE = "seen.json"

def load_seen():
    if os.path.exists(SEEN_FILE):
        return set(json.load(open(SEEN_FILE)))
    return set()

def save_seen(s):
    json.dump(list(s), open(SEEN_FILE,"w"))

def get_ads():
    r = requests.get(URL, headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
    soup = BeautifulSoup(r.text, "lxml")
    ads=[]
    for item in soup.select("li.ads-list-photo-item"):
        a=item.select_one("a")
        t=item.select_one(".ads-list-photo-item-title")
        if not a: continue
        link=a.get("href")
        if link.startswith("/"): link="https://999.md"+link
        title=t.text.strip() if t else "Fara titlu"
        ads.append({"id":link,"title":title,"link":link})
    return ads

def main():
    seen=load_seen()
    while True:
        try:
            ads=get_ads()
            new=[x for x in ads if x["id"] not in seen]
            for x in reversed(new):
                print(f"NOU: {x['title']} - {x['link']}")
                seen.add(x["id"])
            if new: save_seen(seen)
        except Exception as e:
            print(e)
        time.sleep(300)

if __name__=="__main__":
    main()
