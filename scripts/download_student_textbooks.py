#!/usr/bin/env python3
"""
download_student_textbooks.py
Downloads the official MEB 2024-2025/2025-2026 Türkiye Yüzyılı Maarif Modeli 9. Sınıf Öğrenci Ders Kitapları
and extracts their full text with pdftotext.
"""

import os
import sys
import time
import subprocess
import urllib.request
import shutil
from pathlib import Path

TARGET_DIR = Path("/data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari")
TARGET_DIR.mkdir(parents=True, exist_ok=True)

BOOKS = [
    {
        "id": "biyoloji9",
        "title": "Biyoloji 9. Sınıf Ders Kitabı",
        "url": "https://tymm.meb.gov.tr/assets/pdf/biyoloji-9-sinif-ders-kitabi.pdf",
        "pdf_filename": "biyoloji9.pdf",
        "txt_filename": "biyoloji9.txt"
    },
    {
        "id": "cografya9",
        "title": "Coğrafya 9. Sınıf Ders Kitabı",
        "url": "https://tymm.meb.gov.tr/assets/pdf/cografya-dersi-sinif-9-ders-kitabi.pdf",
        "pdf_filename": "cografya9.pdf",
        "txt_filename": "cografya9.txt"
    },
    {
        "id": "din9",
        "title": "Din Kültürü ve Ahlak Bilgisi 9. Sınıf Ders Kitabı",
        "url": "https://tymm.meb.gov.tr/assets/pdf/din-kulturu-ve-ahlak-bilgisi-9.pdf",
        "pdf_filename": "din9.pdf",
        "txt_filename": "din9.txt"
    },
    {
        "id": "fizik9",
        "title": "Fizik 9. Sınıf Ders Kitabı",
        "url": "https://tymm.meb.gov.tr/assets/pdf/fizik-dersi-9-sinif-ders-kitabi.pdf",
        "pdf_filename": "fizik9.pdf",
        "txt_filename": "fizik9.txt"
    },
    {
        "id": "ingilizce9",
        "title": "İngilizce 9. Sınıf Ders Kitabı",
        "url": "https://tymm.meb.gov.tr/assets/pdf/ingilizce-dersi-9-sinif-ders-kitabi.pdf",
        "pdf_filename": "ingilizce9.pdf",
        "txt_filename": "ingilizce9.txt"
    },
    {
        "id": "kimya9",
        "title": "Kimya 9. Sınıf Ders Kitabı",
        "url": "https://tymm.meb.gov.tr/assets/pdf/kimya-9sinif-ders-kitabi_20260908_105401_981.pdf",
        "pdf_filename": "kimya9.pdf",
        "txt_filename": "kimya9.txt"
    },
    {
        "id": "matematik9_1",
        "title": "Matematik 9. Sınıf Ders Kitabı (1. Kitap)",
        "url": "https://tymm.meb.gov.tr/assets/pdf/matematik-9sinif-ders-kitabi-1kitap_20260908_111051_343.pdf",
        "pdf_filename": "matematik9_1.pdf",
        "txt_filename": "matematik9_1.txt"
    },
    {
        "id": "matematik9_2",
        "title": "Matematik 9. Sınıf Ders Kitabı (2. Kitap)",
        "url": "https://tymm.meb.gov.tr/assets/pdf/matematik-9sinif-ders-kitabi-2kitap_20260908_111224_539.pdf",
        "pdf_filename": "matematik9_2.pdf",
        "txt_filename": "matematik9_2.txt"
    },
    {
        "id": "tarih9",
        "title": "Tarih 9. Sınıf Ders Kitabı",
        "url": "https://tymm.meb.gov.tr/assets/pdf/tarih-9sinif-ders-kitabi_20260908_184825_403.pdf",
        "pdf_filename": "tarih9.pdf",
        "txt_filename": "tarih9.txt"
    },
    {
        "id": "tde9",
        "title": "Türk Dili ve Edebiyatı 9. Sınıf Ders Kitabı",
        "url": "https://tymm.meb.gov.tr/assets/pdf/turk-dili-ve-edebiyati-9sinif-ders-kitabi_20260908_185914_237.pdf",
        "pdf_filename": "tde9.pdf",
        "txt_filename": "tde9.txt"
    }
]

def download_file(url: str, dest_path: Path):
    temp_path = dest_path.with_suffix(".tmp")
    print(f"📥 İndiriliyor: {dest_path.name} <- {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    with urllib.request.urlopen(req) as response, open(temp_path, "wb") as out_file:
        total_size = int(response.headers.get("Content-Length", 0))
        downloaded = 0
        chunk_size = 1024 * 512
        start_time = time.time()
        
        while True:
            chunk = response.read(chunk_size)
            if not chunk:
                break
            out_file.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                elapsed = time.time() - start_time
                speed_mb = (downloaded / (1024 * 1024)) / elapsed if elapsed > 0 else 0
                print(f"\r   İlerleme: %{percent:5.1f} ({downloaded/(1024*1024):.1f}/{total_size/(1024*1024):.1f} MB) [{speed_mb:.2f} MB/s]", end="", flush=True)
        print()
    
    if temp_path.exists():
        temp_path.replace(dest_path)
    print(f"✅ İndirme tamamlandı: {dest_path.name} ({dest_path.stat().st_size / (1024*1024):.2f} MB)")

def extract_text(pdf_path: Path, txt_path: Path):
    print(f"📄 Metin ayrıştırılıyor: {pdf_path.name} -> {txt_path.name}")
    try:
        subprocess.run(["pdftotext", "-layout", str(pdf_path), str(txt_path)], check=True)
        print(f"✅ Metin çıkarıldı: {txt_path.name} ({txt_path.stat().st_size / 1024:.1f} KB)")
    except Exception as e:
        print(f"❌ Metin çıkarma hatası ({pdf_path.name}): {e}")

def main():
    print("==================================================")
    print("MEB 9. SINIF ÖĞRENCİ DERS KİTAPLARI İNDİRME MOTORU")
    print("Türkiye Yüzyılı Maarif Modeli Resmî Öğrenci Kitapları")
    print("==================================================\n")
    
    for book in BOOKS:
        pdf_path = TARGET_DIR / book["pdf_filename"]
        txt_path = TARGET_DIR / book["txt_filename"]
        
        print(f"\n--- [{book['id']}] {book['title']} ---")
        # Download
        download_file(book["url"], pdf_path)
        # Extract text
        extract_text(pdf_path, txt_path)

    # Make standard matematik9.pdf / matematik9.txt copy/link to matematik9_1 for backward compat
    mat1_pdf = TARGET_DIR / "matematik9_1.pdf"
    mat1_txt = TARGET_DIR / "matematik9_1.txt"
    mat_pdf = TARGET_DIR / "matematik9.pdf"
    mat_txt = TARGET_DIR / "matematik9.txt"
    
    if mat1_pdf.exists():
        shutil.copyfile(mat1_pdf, mat_pdf)
    if mat1_txt.exists():
        shutil.copyfile(mat1_txt, mat_txt)
    print("\n✅ Matematik 1. Kitap -> matematik9.pdf / matematik9.txt eşlendi.")

if __name__ == "__main__":
    main()
