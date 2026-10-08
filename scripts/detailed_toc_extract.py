#!/usr/bin/env python3
"""
detailed_toc_extract.py
Extracts full Table of Contents / Unit 1 Details for all 10 student books.
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

def extract_toc(name, fn):
    p = DATA_DIR / fn
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read(40000)
    
    print(f"\n==================== {name} ====================")
    # Search for Unit / Theme titles in text
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    found = []
    for line in lines[:250]:
        if re.search(r"^\d+\.\s*(ÜNİTE|TEMA|BÖLÜM|Bölüm)|^(ÜNİTE|TEMA|İÇİNDEKİLER|THEME|Theme)\s*\d*|^\d+\.\d+\.?\s+[A-ZÇĞİÖŞÜ]", line):
            found.append(line)
    
    for item in found[:15]:
        print(f"  • {item}")

def main():
    for name, fn in FILES:
        extract_toc(name, fn)

if __name__ == "__main__":
    main()
