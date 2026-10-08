import json, os

with open("data/defterdoldur_tum_dersler_9al.json", "r", encoding="utf-8") as f:
    core_data = json.load(f)

with open("data/defterdoldur_yabanci_diller_9al.json", "r", encoding="utf-8") as f:
    lang_data = json.load(f)

all_lessons = {**core_data, **lang_data}
vault_dir = "/storage/emulated/0/Documents/AGY-Vault/10-Projects/Lise-1-Yillik-Planlar"

for subject, weeks in all_lessons.items():
    safe_name = subject.replace(" ", "_").replace("(", "").replace(")", "").replace("/", "_")
    fpath = os.path.join(vault_dir, f"{safe_name}_Yillik_Plan_AL9.md")
    
    lines = [
        f"# 9. Sınıf {subject} - Yıllık Planı (Tüm Yıl - 37/41 Hafta)",
        "",
        "> **Kaynak:** DefterDoldur.com (MEB Türkiye Yüzyılı Maarif Modeli Resmî Zümre Yıllık Planı)",
        f"> **Ders:** {subject}",
        f"> **Toplam Hafta Sayısı:** {len(weeks)}",
        "",
        "---",
        ""
    ]
    
    for w in weeks:
        h_no = w.get("hafta_no", "")
        tarih = w.get("tarih", "")
        saat = w.get("saat", "")
        tema = w.get("tema", "")
        konu = w.get("konu", "")
        kazanim = w.get("kazanim", "")
        surec = w.get("surec", "")
        
        lines.append(f"## 📍 {h_no}. Hafta ({tarih}) - {saat} Saat")
        if tema:
            lines.append(f"- **Ünite / Tema:** {tema}")
        if konu:
            lines.append(f"- **Konu (İçerik Çerçevesi):** {konu}")
        if kazanim:
            lines.append(f"- **Kazanım (Öğrenme Çıktısı):** {kazanim}")
        if surec:
            lines.append(f"- **Süreç Bileşenleri / Uygulama:**\n    {surec}")
        lines.append("\n---\n")
        
    with open(fpath, "w", encoding="utf-8") as out_f:
        out_f.write("\n".join(lines))
    print(f"✅ {subject} -> {fpath} ({len(weeks)} hafta kaydedildi)")

# Ayrica tam JSON yedegini de vault a kopyala
with open(os.path.join(vault_dir, "tum_dersler_9al_yillik_planlar.json"), "w", encoding="utf-8") as jf:
    json.dump(all_lessons, jf, ensure_ascii=False, indent=2)

print("\n🎉 Tüm derslerin yıllık planları AGY-Vault'a başarıyla aktarıldı!")
