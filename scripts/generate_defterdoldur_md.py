import json

with open("data/defterdoldur_tum_dersler_9al.json", "r", encoding="utf-8") as f:
    data = json.load(f)

md_out = [
    "# 9. Sınıf Anadolu Lisesi (AL) - DefterDoldur.com Kaynaklı Resmî Yıllık Planlar (İlk 4 Hafta & 1. Dönem)",
    "",
    "> **Resmî Plan Kaynağı:** [DefterDoldur.com](https://defterdoldur.com) (MEB Türkiye Yüzyılı Maarif Modeli 9. Sınıf Anadolu Lisesi Zümre Yıllık Planları)",
    "",
    "---",
    "",
    "## 🗓️ BÖLÜM 1: İLK 4 HAFTANIN DERS BAZLI KONU VE İÇERİK DÖKÜMÜ",
    ""
]

weeks_count = 4

for w_idx in range(weeks_count):
    h_no = w_idx + 1
    # 1. haftanin tarihini matematikten alalim
    sample_w = data["Matematik"][w_idx]
    tarih = sample_w.get("tarih", f"Hafta {h_no}")
    
    md_out.append(f"### 📍 {h_no}. HAFTA ({tarih})\n")
    
    for subject, weeks in data.items():
        if w_idx < len(weeks):
            w = weeks[w_idx]
            tema = w.get("tema", "")
            konu = w.get("konu", "")
            kazanim = w.get("kazanim", "")
            saat = w.get("saat", "")
            surec = w.get("surec", "")
            
            md_out.append(f"#### 🔹 {subject} ({saat} Saat)")
            if tema:
                md_out.append(f"- **Ünite / Tema:** {tema}")
            if konu:
                md_out.append(f"- **Konu (İçerik Çerçevesi):** {konu}")
            if kazanim:
                md_out.append(f"- **Öğrenme Çıktısı (Kazanım):** {kazanim}")
            if surec:
                md_out.append(f"- **Süreç ve Uygulama Detayları:**\n    {surec}")
            md_out.append("")
    md_out.append("---\n")

# Tablo Ozeti
md_out.append("## 📊 BÖLÜM 2: İLK 4 HAFTA MATRİS ÖZET TABLOSU\n")
md_out.append("| DERS | 1. HAFTA (ŞU AN) | 2. HAFTA | 3. HAFTA | 4. HAFTA |")
md_out.append("| :--- | :--- | :--- | :--- | :--- |")

for subject, weeks in data.items():
    row = [f"**{subject}**"]
    for w_idx in range(4):
        if w_idx < len(weeks):
            w = weeks[w_idx]
            kn = w.get("konu", "")
            kz = w.get("kazanim", "")
            if kn:
                val = kn.split("  ")[0]
            elif kz:
                val = kz.split(".")[0] + "..."
            else:
                val = "-"
            # Kisalt
            if len(val) > 40:
                val = val[:37] + "..."
            row.append(val)
        else:
            row.append("-")
    md_out.append("| " + " | ".join(row) + " |")

# Dosyaya kaydet
with open("data/defterdoldur_ilk_4_hafta_resmi_plan.md", "w", encoding="utf-8") as f:
    f.write("\n".join(md_out))

print("✅ data/defterdoldur_ilk_4_hafta_resmi_plan.md başarıyla oluşturuldu!")
