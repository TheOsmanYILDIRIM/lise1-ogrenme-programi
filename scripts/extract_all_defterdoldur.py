import urllib.request, re, json, os

PLANS = {
    "Matematik": "https://defterdoldur.com/plandetay/matematik/2456/matematik-al-9",
    "Fizik": "https://defterdoldur.com/plandetay/fizik/2400/fizik-al-9",
    "Kimya": "https://defterdoldur.com/plandetay/kimya/2400/kimya-al-9",
    "Biyoloji": "https://defterdoldur.com/plandetay/biyoloji/2400/biyoloji-al-9",
    "Tarih": "https://defterdoldur.com/plandetay/tarih/2400/tarih-al-9",
    "Cografya": "https://defterdoldur.com/plandetay/cografya/2400/cografya-al-9",
    "TDE": "https://defterdoldur.com/plandetay/turk-dili-ve-edebiyati/2400/turk-dili-ve-edebiyati-al-9"
}

def extract_plan(name, url):
    print(f"Çekiliyor: {name} -> {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
    
    weeks = html.split("Ders Tarihi")
    plan_list = []
    
    for idx, w in enumerate(weeks[1:], 1):
        t_m = re.search(r"^([0-9\-]+[\s\n]+[A-Za-zĞÜŞİÖÇğüşıöç]+)", w.strip())
        tarih = re.sub(r"\s+", " ", t_m.group(1)).strip() if t_m else f"Hafta {idx}"
        
        saat_m = re.search(r"Ders Saati[\s\n]*([0-9\+]+)", w)
        saat = saat_m.group(1) if saat_m else ""
        
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
    all_data = {}
    for name, url in PLANS.items():
        all_data[name] = extract_plan(name, url)
        print(f"✅ {name}: {len(all_data[name])} hafta başarıyla çekildi.")
        
    with open("data/defterdoldur_tum_dersler_9al.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
        
    print("\n🎉 Tüm 7 dersin DefterDoldur planları başarıyla kaydedildi!")
