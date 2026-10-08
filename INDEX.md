# 📚 Lise 1 (9. Sınıf Anadolu Lisesi) Öğrenme Programı - Proje İndeksi

Bu dizin, 9. Sınıf Anadolu Lisesi (AL-9) öğrencisi için hazırlanan MEB Türkiye Yüzyılı Maarif Modeli uyumlu tüm ders kitapları, yıllık planlar, Anki soru-cevap desteleri ve video ders rehberlerini bir araya getiren ana atölyedir.

---

## 🧭 Proje Dizin Yapısı ve Haritası

```
lise1-ogrenme-programi/
├── INDEX.md                                # 📌 Proje ana haritası ve kılavuz (Bu dosya)
├── notes.md                                # 📝 Mimari notlar ve ders dağılımı
├── backlog.md                              # 📋 Yapılacaklar ve süreç takibi
├── log.md                                  # 📜 Tamamlanan adımlar ve sürüm günlüğü
├── data/
│   ├── defterdoldur_tum_dersler_9al.json   # 🗄️ 9 Dersin 41 haftalık doğrulanmış resmî JSON veritabanı
│   ├── defterdoldur_ilk_4_hafta_resmi_plan.md # 🗓️ İlk 4 haftanın tüm dersler resmî zümre planı
│   ├── meb_kitaplari/                      # 📖 MEB 9. Sınıf Resimli Zenginleştirilmiş Kitapları (.md + PNG)
│   │   ├── matematik_etkinlik_kitabi.md
│   │   ├── fizik9.md
│   │   ├── kimya9.md
│   │   ├── biyoloji9.md
│   │   ├── tarih9.md
│   │   ├── cografya9.md
│   │   └── tde9.md
│   ├── anki_decks/                         # 📇 Flashcard / Aralıklı Tekrar Soru-Cevap Desteleri (.txt)
│   │   ├── 9_sinif_biyoloji_anki.txt
│   │   ├── 9_sinif_cografya_anki.txt
│   │   └── 9_sinif_tarih_anki.txt
│   └── video_curation/                     # 📺 Video Oynatma Listeleri ve Kanal Rehberi
│       └── 9_sinif_video_rehberi.md
└── scripts/
    └── verify_anki_decks.py                # 🧪 Anki kart format ve bütünlük test aracı
```

---

## 🗂️ 1. MEB Resmî Maarif Modeli Öğrenci Ders Kitapları (`data/meb_kitaplari/`)
Kitaplar, MEB TYMM (Türkiye Yüzyılı Maarif Modeli) ve OGM Materyal resmî portallarından temin edilmiş güncel 9. Sınıf Öğrenci Ders Kitaplarıdır:
* 📐 [Matematik 9 (1. Kitap) PDF](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/matematik9_1.pdf) | [Metin](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/matematik9_1.txt)
* 📐 [Matematik 9 (2. Kitap) PDF](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/matematik9_2.pdf) | [Metin](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/matematik9_2.txt)
* ⚡ [Fizik 9 Ders Kitabı PDF](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/fizik9.pdf) | [Metin](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/fizik9.txt)
* 🧪 [Kimya 9 Ders Kitabı PDF](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/kimya9.pdf) | [Metin](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/kimya9.txt)
* 🧬 [Biyoloji 9 Ders Kitabı PDF](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/biyoloji9.pdf) | [Metin](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/biyoloji9.txt)
* 🏛️ [Tarih 9 Ders Kitabı PDF](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/tarih9.pdf) | [Metin](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/tarih9.txt)
* 🌍 [Coğrafya 9 Ders Kitabı PDF](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/cografya9.pdf) | [Metin](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/cografya9.txt)
* 📖 [Türk Dili ve Edebiyatı 9 Ders Kitabı PDF](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/tde9.pdf) | [Metin](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/tde9.txt)
* 🇬🇧 [İngilizce 9 Ders Kitabı PDF](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/ingilizce9.pdf) | [Metin](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/ingilizce9.txt)
* 🕌 [Din Kültürü ve Ahlak Bilgisi 9 PDF](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/din9.pdf) | [Metin](file:///data/data/com.termux/files/home/projects/lise1-ogrenme-programi/data/meb_kitaplari/din9.txt)

---

## 📅 2. Resmî Maarif Modeli Yıllık Zümre Planları (`curriculum/yillik_planlar/`)
DefterDoldur.com kaynaklı 41 haftalık eksiksiz zümre planları depomuzda yer almaktadır:
1. 📐 [Matematik Yıllık Planı](curriculum/yillik_planlar/Matematik_Yillik_Plan_AL9.md)
2. ⚡ [Fizik Yıllık Planı](curriculum/yillik_planlar/Fizik_Yillik_Plan_AL9.md)
3. 🧪 [Kimya Yıllık Planı](curriculum/yillik_planlar/Kimya_Yillik_Plan_AL9.md)
4. 🧬 [Biyoloji Yıllık Planı](curriculum/yillik_planlar/Biyoloji_Yillik_Plan_AL9.md)
5. 🏛️ [Tarih Yıllık Planı](curriculum/yillik_planlar/Tarih_Yillik_Plan_AL9.md)
6. 🌍 [Coğrafya Yıllık Planı](curriculum/yillik_planlar/Cografya_Yillik_Plan_AL9.md)
7. 📖 [TDE Yıllık Planı](curriculum/yillik_planlar/TDE_Yillik_Plan_AL9.md)
8. 🇬🇧 [İngilizce Yıllık Planı](curriculum/yillik_planlar/İngilizce_Yillik_Plan_AL9.md)
9. 🇩🇪 [Almanca Yıllık Planı](curriculum/yillik_planlar/Almanca_Yillik_Plan_AL9.md)
* 🎯 **[4 Haftalık Maarif Modeli Çalışma & Pekiştirme Planı (StudyTracker Uyumlu)](curriculum/calisma_ve_ders_programi/9_sinif_4_haftalik_studytracker_calisma_plani.md)** *(Ders programı senkronu, ultra hafif etütler, 3 ders Anki destesi ve çözümlü mikro pekiştirme soruları)*
* 📅 **[40 Saatlik Resmî Haftalık Ders Programı Çizelgesi](curriculum/calisma_ve_ders_programi/9-sinif-haftalik-ders-programi-ve-koyrusu.md)**

---

## 🎬 3. Video Ders ve Oynatma Listesi Rehberleri (`curriculum/video_rehberleri/`)
* 📐 [1. Ay Matematik Khan Academy & Video Rehberi](curriculum/video_rehberleri/1_ay_matematik_khan_academy_videolari.md)
* ⚡ [1. Ay Fizik VIP Fizik & Özcan Aykın Rehberi](curriculum/video_rehberleri/1_ay_fizik_video_rehberi.md)
* 🧬 [1. Ay Biyoloji Khan Academy & Biosem / Selin Hoca Rehberi](curriculum/video_rehberleri/1_ay_biyoloji_video_rehberi.md)
* 🧪 [1. Ay Kimya Khan Academy & Görkem Şahin Rehberi](curriculum/video_rehberleri/1_ay_kimya_video_rehberi.md)
* 🏛️ [1. Ay Tarih Mehmet Celal Hoca & Video Rehberi](curriculum/video_rehberleri/1_ay_tarih_video_rehberi.md)
* 🌍 [1. Ay Coğrafya Coğrafyanın Kodları & Engin Eraydın Rehberi](curriculum/video_rehberleri/1_ay_cografya_video_rehberi.md)
* 🇬🇧 [1. Ay İngilizce Özer Kiraz & Hocalara Geldik Rehberi](curriculum/video_rehberleri/1_ay_ingilizce_video_rehberi.md)
* 🇩🇪 [1. Ay Almanca Almanca Kolay & Meltem Hoca Rehberi](curriculum/video_rehberleri/1_ay_almanca_video_rehberi.md)
* 🌐 [9. Sınıf Genel Video & Kanal Kürasyonu](data/video_curation/9_sinif_video_rehberi.md)

---

## 📇 4. Anki Kartları ve APKG Paketleri (`data/anki_decks/`)
* 📦 **Hazır APKG Paketleri (Görsel Sözlüklü + Otomatik TTS Sesli + Özel CSS Tasarımlı):**
  * 🇬🇧 [9_sinif_ingilizce_1_ay.apkg](data/anki_decks/9_sinif_ingilizce_1_ay.apkg) *(36 kart — Ünite bazlı alt desteler: Theme 1 & Theme 2, dahili günlük 15 kart limitli, Azure AriaNeural sesli)*
  * 🇩🇪 [9_sinif_almanca_1_ay.apkg](data/anki_decks/9_sinif_almanca_1_ay.apkg) *(21 kart — Ünite alt destesi: Modul 1: Hallo!, dahili günlük 15 kart limitli, Azure KatjaNeural sesli)*
* 📝 **Ham TSV/Metin Kartları:**
  * [Biyoloji Anki Deste Metni](data/anki_decks/9_sinif_biyoloji_anki.txt)
  * [Coğrafya Anki Deste Metni](data/anki_decks/9_sinif_cografya_anki.txt)
  * [Tarih Anki Deste Metni](data/anki_decks/9_sinif_tarih_anki.txt)
  * [İngilizce Anki Deste Metni](data/anki_decks/9_sinif_ingilizce_anki.txt)
  * [Almanca Anki Deste Metni](data/anki_decks/9_sinif_almanca_anki.txt)

---

## 🗂️ 5. Kelime Listeleri & Kavram Sözlükleri (`curriculum/kelime_listeleri/`)
* 🇬🇧 [1. Ay İngilizce Hedef Kelime ve Kalıp Listesi (Theme 1 & Theme 2)](curriculum/kelime_listeleri/1_ay_ingilizce_kelime_listesi.md)
* 🇩🇪 [1. Ay Almanca Temel İletişim & Kelime Rehberi (A1.1 Modül 1)](curriculum/kelime_listeleri/1_ay_almanca_kelime_listesi.md)
