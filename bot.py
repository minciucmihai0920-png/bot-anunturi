def verifica_999():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        url = "https://999.md/ro"
        r = requests.get(url, headers=headers)
        print(f"999 status: {r.status_code}", flush=True)
        soup = BeautifulSoup(r.text, 'html.parser')
        gasite = 0
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/ro/' in href and len(href) > 20:
                full = href if 'https' in href else f"https://999.md{href}"
                if '999.md' in full and full not in trimise:
                    # DOAR anunturi, nu pagini info
                    if '/info' in full or '/pages' in full or '/help' in full:
                        continue
                    if '/ro/' in full and full.count('/') >= 4:
                        print(f"ANUNT GASIT: {full}", flush=True)
                        trimise.add(full)
                        gasite += 1
                        trimite_telegram(f"ANUNT NOU!\n\n{full}\n\nPret <25k - verifica rapid!")
                        time.sleep(1)
                        if gasite >= 3:
                            break
        print(f"Verificare gata, gasite noi: {gasite}", flush=True)
    except Exception as e:
        print(f"Eroare: {e}", flush=True)
