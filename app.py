import os, time, threading, requests
from bs4 import BeautifulSoup
from flask import Flask

BOT_TOKEN=os.getenv("BOT_TOKEN")
CHANNEL_ID=os.getenv("CHANNEL_ID")
sent=set()
app=Flask(__name__)

@app.route('/')
def home():
    return "Bot LIVE - TOATE ANUNTURILE 999"

def get_ads():
    try:
        r=requests.get("https://999.md/ro/list", headers={"User-Agent":"Mozilla/5.0"}, timeout=15)
        soup=BeautifulSoup(r.text,"html.parser")
        ads=[]
        for a in soup.select("a[href*='/boletin/']"):
            link=a.get("href")
            if not link: continue
            if not link.startswith("http"): link="https://999.md"+link
            title=a.get_text(strip=True)
            if len(title)<10: continue
            ads.append((title,link))
            if len(ads)>=5: break
        return ads
    except:
        return []

def send(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id":CHANNEL_ID,"text":msg}, timeout=10)
    except: pass

def loop():
    while True:
        for tit,link in get_ads():
            if link not in sent:
                send(f"📢 {tit}\n\n{link}")
                sent.add(link)
        time.sleep(60)

threading.Thread(target=loop,daemon=True).start()

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
