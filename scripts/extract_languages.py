import urllib.request, re, json

LANG_PLANS = {
    "İngilizce (Birinci Yabancı Dil)": "https://defterdoldur.com/plandetay/ingilizce/2350/ingilizce-al-9",
    "Almanca (İkinci Yabancı Dil)": "https://defterdoldur.com/plandetay/almanca/2350/almanca-al-9"
}

def extract_lang_plan(name, url):
    print(f"Çekiliyor: {name} -> {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
    
    weeks = html.split("Ders Tarihi")
    plan_list = []
    
    for idx, w in enumerate(weeks[1:], 1):
        t_m = re.search(r"^([0-9\-]+[\s\n]+[A-Za-zĞÜŞİÖÇğüşıöç]+)", w.strip())
        tarih = re.sub(r"\s+", " ", t_m.group(1)).strip() if t_m else f"Hafta {idx}"
        
        saat_m = re.search(r"Ders Saati[\s\n]*([0-9\+]+)", w)
        saat = saat_m.group(1) if saat_m else ("4" if "İngilizce" in name else "2")
        
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
    lang_data = {}
    for name, url in LANG_PLANS.items():
        lang_data[name] = extract_lang_plan(name, url)
        print(f"✅ {name}: {len(lang_data[name])} hafta çekildi.")
        
    with open("data/defterdoldur_yabanci_diller_9al.json", "w", encoding="utf-8") as f:
        json.dump(lang_data, f, ensure_ascii=False, indent=2)
        
    # Markdown ekle
    md = [
        "# 9. Sınıf Anadolu Lisesi - İngilizce ve Almanca Resmî Yıllık Planları (İlk 4 Hafta)",
        "",
        "> **Kaynak:** [DefterDoldur.com](https://defterdoldur.com) (MEB Maarif Modeli 9. Sınıf AL Planları)",
        "",
        "---",
        ""
    ]
    
    for w_idx in range(4):
        h_no = w_idx + 1
        tarih = lang_data["İngilizce (Birinci Yabancı Dil)"][w_idx].get("tarih", f"Hafta {h_no}")
        md.append(f"### 📍 {h_no}. HAFTA ({tarih})\n")
        
        for name, weeks in lang_data.items():
            w = weeks[w_idx]
            md.append(f"#### 🌐 {name} ({w.get('saat', '')} Saat)")
            if w.get('tema'):
                md.append(f"- **Ünite / Tema:** {w['tema']}")
            if w.get('konu'):
                md.append(f"- **Konu (İçerik):** {w['konu']}")
            if w.get('kazanim'):
                md.append(f"- **Kazanım (Öğrenme Çıktısı):** {w['kazanim']}")
            if w.get('surec'):
                md.append(f"- **Süreç ve İletişim Becerileri:**\n    {w['surec']}")
            md.append("")
        md.append("---\n")
        
    with open("data/defterdoldur_ingilizce_almanca_4hafta.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md))
        
    print("✅ data/defterdoldur_ingilizce_almanca_4hafta.md kaydedildi!")
