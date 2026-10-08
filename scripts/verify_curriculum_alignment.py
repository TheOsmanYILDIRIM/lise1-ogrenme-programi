#!/usr/bin/env python3
"""
verify_curriculum_alignment.py
Analyzes the newly extracted text of MEB 9th Grade Student Textbooks
and compares the 1st Month / 1st Unit topics against our 4-Week Study Plan and Anki Decks.
"""

import re
from pathlib import Path

DATA_DIR = Path("/data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari")

FILES = [
    ("Biyoloji 9", "biyoloji9.txt"),
    ("Coğrafya 9", "cografya9.txt"),
    ("Din Kültürü 9", "din9.txt"),
    ("Fizik 9", "fizik9.txt"),
    ("İngilizce 9", "ingilizce9.txt"),
    ("Kimya 9", "kimya9.txt"),
    ("Matematik 9 (1. Kitap)", "matematik9_1.txt"),
    ("Matematik 9 (2. Kitap)", "matematik9_2.txt"),
    ("Tarih 9", "tarih9.txt"),
    ("Türk Dili ve Edebiyatı 9", "tde9.txt")
]

def analyze_book(name, filename):
    filepath = DATA_DIR / filename
    if not filepath.exists():
        print(f"⚠️ {name}: Dosya henüz hazır değil ({filename})")
        return None
    
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read(50000) # Read first 50k chars (table of contents & unit 1 intro)
    
    lines = content.splitlines()
    print(f"\n{'='*60}\n📚 {name} ({filepath.name} - Boyut: {filepath.stat().st_size/1024:.1f} KB)\n{'='*60}")
    
    # Extract lines mentioning Ünite / Tema / İçindekiler / Bölüm
    toc_lines = []
    in_toc = False
    for line in lines[:400]:
        cleaned = line.strip()
        if not cleaned:
            continue
        if re.search(r"İÇİNDEKİLER|İ Ç İ N D E K İ L E R|CONTENTS|İçindekiler", cleaned, re.IGNORECASE):
            in_toc = True
        if in_toc:
            if len(toc_lines) < 35:
                toc_lines.append(cleaned)
    
    if toc_lines:
        print("📌 İÇİNDEKİLER / ÜNİTE YAPISI:")
        for l in toc_lines[:25]:
            print(f"   • {l}")
    else:
        print("📌 İLK BÖLÜM BAŞLIKLARI (Özet):")
        unit_headings = [l.strip() for l in lines[:300] if re.search(r"^[0-9]\.\s*ÜNİTE|^ÜNİTE|^TEMA|^BÖLÜM|^1\.", l.strip())]
        for h in unit_headings[:15]:
            print(f"   • {h}")

def main():
    print("==================================================")
    print("MEB ÖĞRENCİ DERS KİTAPLARI MÜFREDAT MUTABAKAT ANALİZİ")
    print("==================================================")
    for name, fn in FILES:
        analyze_book(name, fn)

if __name__ == "__main__":
    main()
