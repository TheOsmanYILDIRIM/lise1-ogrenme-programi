import urllib.request, re, json

def parse_defterdoldur(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req).read().decode("utf-8")
    
    weeks_data = html.split("Ders Tarihi")
    parsed_weeks = []
    for idx, w in enumerate(weeks_data[1:], 1):
        tarih_m = re.search(r"^([0-9\-]+[\s\n]+[A-Za-zĞÜŞİÖÇğüşıöç]+)", w.strip())
        tarih = re.sub(r"\s+", " ", tarih_m.group(1)).strip() if tarih_m else f"Hafta {idx}"
        
        saat_m = re.search(r"Ders Saati[\s\n]*([0-9\+]+)", w)
        saat = saat_m.group(1) if saat_m else "6"
        
        tema_m = re.search(r"Ünite/Tema/Öğrenme Alanı[\s\n]*</div>[\s\n]*<div[^>]*>[\s\n]*<p>([^<]+)</p>", w)
        tema = tema_m.group(1).strip() if tema_m else ""
        
        konu_m = re.search(r"Konu \(İçerik Çerçevesi\)[\s\n]*</div>[\s\n]*<div[^>]*>[\s\n]*([^<]+)[\s\n]*</div>", w)
        konu = konu_m.group(1).strip() if konu_m else ""
        
        kazanim_m = re.search(r"Öğrenme Çıktısı \(Kazanımlar\)[\s\n]*</div>[\s\n]*<div[^>]*>[\s\n]*(.*?)[\s\n]*</div>", w, re.DOTALL)
        kazanim = ""
        if kazanim_m:
            kazanim = re.sub(r"<[^>]+>", " ", kazanim_m.group(1))
            kazanim = re.sub(r"\s+", " ", kazanim).strip()
            
        surec_m = re.search(r"Süreç Bileşenleri[\s\n]*</div>[\s\n]*<div[^>]*>[\s\n]*(.*?)[\s\n]*</div>", w, re.DOTALL)
        surec = ""
        if surec_m:
            surec = re.sub(r"<br\s*/?>", "\n    • ", surec_m.group(1))
            surec = re.sub(r"<[^>]+>", "", surec)
            surec = re.sub(r"&nbsp;", " ", surec)
            surec = surec.strip()
            if surec and not surec.startswith("•"):
                surec = "• " + surec
                
        parsed_weeks.append({
            "hafta_no": idx,
            "tarih": tarih,
            "saat": saat,
            "tema": tema,
            "konu": konu,
            "kazanim": kazanim,
            "surec": surec
        })
    return parsed_weeks

if __name__ == "__main__":
    mat_url = "https://defterdoldur.com/plandetay/matematik/2456/matematik-al-9"
    weeks = parse_defterdoldur(mat_url)
    print(f"Toplam {len(weeks)} hafta parse edildi.")
    
    with open("data/defterdoldur_matematik9_tam_plan.json", "w", encoding="utf-8") as f:
        json.dump(weeks, f, ensure_ascii=False, indent=2)
        
    for w in weeks[:18]:
        h_no = w['hafta_no']
        t = w['tarih']
        s = w['saat']
        tm = w['tema']
        k = w['konu']
        kz = w['kazanim']
        sr = w['surec']
        print(f"\n[{h_no}. Hafta: {t} - {s} Saat]")
        print(f"Tema: {tm}")
        print(f"Konu: {k}")
        print(f"Kazanım: {kz}")
        if sr:
            print(f"Süreç: {sr[:200]}...")
