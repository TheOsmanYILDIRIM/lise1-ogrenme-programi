import urllib.request, re, json

def extract_all_weeks(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req).read().decode("utf-8")
    
    weeks = html.split("Ders Tarihi")
    plan_list = []
    
    for idx, w in enumerate(weeks[1:], 1):
        t_m = re.search(r"^([0-9\-]+[\s\n]+[A-Za-zĞÜŞİÖÇğüşıöç]+)", w.strip())
        tarih = re.sub(r"\s+", " ", t_m.group(1)).strip() if t_m else f"Hafta {idx}"
        
        saat_m = re.search(r"Ders Saati[\s\n]*([0-9\+]+)", w)
        saat = saat_m.group(1) if saat_m else "6"
        
        # Tema
        tema = ""
        tema_match = re.search(r"Ünite/Tema/Öğrenme Alanı.*?<div[^>]*>(.*?)</div>", w, re.DOTALL)
        if tema_match:
            tema = re.sub(r"<[^>]+>", " ", tema_match.group(1))
            tema = re.sub(r"\s+", " ", tema).strip()
            
        # Konu (İçerik Çerçevesi)
        konu = ""
        konu_match = re.search(r"Konu \(İçerik Çerçevesi\).*?<div[^>]*>(.*?)</div>", w, re.DOTALL)
        if konu_match:
            konu = re.sub(r"<[^>]+>", " ", konu_match.group(1))
            konu = re.sub(r"\s+", " ", konu).strip()
            
        # Kazanım (Öğrenme Çıktısı)
        kazanim = ""
        kaz_match = re.search(r"Öğrenme Çıktısı \(Kazanımlar\).*?<div[^>]*>(.*?)</div>", w, re.DOTALL)
        if kaz_match:
            kazanim = re.sub(r"<[^>]+>", " ", kaz_match.group(1))
            kazanim = re.sub(r"\s+", " ", kazanim).strip()
            
        # Süreç Bileşenleri
        surec = ""
        sur_match = re.search(r"Süreç Bileşenleri.*?<div[^>]*>(.*?)</div>", w, re.DOTALL)
        if sur_match:
            surec = re.sub(r"<br\s*/?>", "\n    • ", sur_match.group(1))
            surec = re.sub(r"<[^>]+>", " ", surec)
            surec = re.sub(r"&nbsp;", " ", surec)
            surec = re.sub(r"\s+", " ", surec).strip()
            
        plan_list.append({
            "hafta_no": idx,
            "tarih": tarih,
            "saat": saat,
            "tema": tema,
            "konu": konu,
            "kazanim": kazanim,
            "surec": surec
        })
        
    return plan_list

if __name__ == "__main__":
    url = "https://defterdoldur.com/plandetay/matematik/2456/matematik-al-9"
    plan = extract_all_weeks(url)
    print(f"Toplam {len(plan)} hafta verisi çıkarıldı.")
    
    with open("data/defterdoldur_matematik9_tam.json", "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
        
    for p in plan[:18]:
        no = p["hafta_no"]
        tar = p["tarih"]
        st = p["saat"]
        tm = p["tema"]
        kn = p["konu"]
        kz = p["kazanim"]
        print(f"Hafta {no} [{tar} - {st} Saat]:")
        print(f"  Tema: {tm}")
        print(f"  Konu: {kn}")
        print(f"  Kazanım: {kz}")
        print()
