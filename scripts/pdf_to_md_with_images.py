import os
import subprocess
import re

BOOKS = [
    ("cografya9", "Coğrafya 9"),
    ("tarih9", "Tarih 9"),
    ("biyoloji9", "Biyoloji 9"),
    ("matematik9", "Matematik 9"),
    ("fizik9", "Fizik 9"),
    ("kimya9", "Kimya 9"),
    ("tde9", "Türk Dili ve Edebiyatı 9")
]

BASE_DIR = "/data/data/com.termux/files/home/lise1-ogrenme-programi/data/meb_kitaplari"

def convert_pdf_to_markdown_with_images(book_key, title):
    pdf_path = os.path.join(BASE_DIR, f"{book_key}.pdf")
    img_dir = os.path.join(BASE_DIR, f"{book_key}_images")
    md_path = os.path.join(BASE_DIR, f"{book_key}.md")
    
    if not os.path.exists(pdf_path):
        print(f"PDF bulunamadı: {pdf_path}")
        return
    
    os.makedirs(img_dir, exist_ok=True)
    
    # 1. Resimleri çıkar (PNG olarak)
    print(f"[{title}] Görseller çıkarılıyor...")
    subprocess.run(["pdfimages", "-png", pdf_path, os.path.join(img_dir, "img")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Resimleri listele
    images = sorted([f for f in os.listdir(img_dir) if f.endswith(".png")])
    print(f"[{title}] Toplam {len(images)} görsel çıkarıldı.")
    
    # 2. Metni çıkar
    txt_path = os.path.join(BASE_DIR, f"{book_key}.txt")
    if not os.path.exists(txt_path):
        subprocess.run(["pdftotext", "-layout", pdf_path, txt_path])
    
    with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    
    # 3. Markdown formatına dönüştür ve görselleri bağla
    lines = text.split("\n")
    md_lines = [
        f"# {title} - MEB Ders Kitabı & Zenginleştirilmiş Öğrenme Metni",
        "",
        f"> **Kaynak:** MEB OGM Materyal 9. Sınıf Güncel Müfredatı",
        f"> **Görsel Dizini:** `./{book_key}_images/` ({len(images)} adet şekil/şema/harita)",
        "",
        "---",
        ""
    ]
    
    img_idx = 0
    paragraph_count = 0
    
    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        
        # Başlık tespiti
        if re.match(r'^(ÜNİTE\s+\d+|[0-9]+\.\s+ÜNİTE|[A-ZĞÜŞİÖÇ\s]{4,}:?$)', clean) and len(clean) < 60:
            md_lines.append(f"\n## {clean}\n")
        elif re.match(r'^\d+\.\d+\.?\s+', clean) or re.match(r'^[A-Z]\)\s+', clean):
            md_lines.append(f"\n### {clean}\n")
        else:
            md_lines.append(clean)
            paragraph_count += 1
            # Her 6-8 paragrafta bir ilgili görseli markdown'a göm
            if paragraph_count % 7 == 0 and img_idx < len(images):
                img_name = images[img_idx]
                md_lines.append(f"\n![{title} Şekil/Görsel {img_idx+1}](./{book_key}_images/{img_name})\n")
                img_idx += 1
    
    # Kalan önemli görselleri bir galeri şeklinde ekle
    if img_idx < len(images):
        md_lines.append("\n\n---\n## 🖼️ Ünite ve Konu Görselleri / Harita / Şema Galerisi\n")
        for i in range(img_idx, min(len(images), img_idx + 25)):
            md_lines.append(f"![{title} Görsel {i+1}](./{book_key}_images/{images[i]})\n")
    
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    
    print(f"✅ [{title}] Markdown ({os.path.basename(md_path)}) başarıyla oluşturuldu!")

if __name__ == "__main__":
    for key, name in BOOKS:
        convert_pdf_to_markdown_with_images(key, name)
