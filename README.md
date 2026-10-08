# 📚 Lise 1 (9. Sınıf Anadolu Lisesi) Öğrenme Ekosistemi & Maarif Müfredat Atlası

Bu depo, MEB **Türkiye Yüzyılı Maarif Modeli (TYMM)** 9. Sınıf Anadolu Lisesi (AL-9) müfredatına tam uyumlu **yıllık zümre planları, video ders kürasyonları, Anki aralıklı tekrar desteleri, haftalık okul çalışma çizelgeleri ve ders özetlerini** tek bir standart altında toplayan açık eğitim atölyesidir.

> [!TIP]
> Bu depo, öğrenci takip ve sınav uygulaması olan **[StudyTracker](https://github.com/TheOsmanYILDIRIM/study-tracker)** Android ekosisteminin resmî müfredat ve içerik kaynağıdır (Content Source of Truth). Hem yapay zeka ajanları (AI) hem de öğrenciler/öğretmenler için doğrudan okunabilir Markdown ve JSON formatında düzenlenmiştir.

---

## 🧭 Proje Dizin Mimarisi

```text
lise1-ogrenme-programi/
├── README.md                                 # Ana kılavuz ve proje rehberi (Bu dosya)
├── INDEX.md                                  # İçerik dizini ve kazanım haritası
├── curriculum/                               # 📌 Resmî Maarif Modeli Müfredat Belgeleri
│   ├── yillik_planlar/                       # 9 Dersin 39-41 haftalık eksiksiz zümre planları (.md)
│   ├── video_rehberleri/                     # 1. Ay (ilk 4 hafta) video ders rehberleri (.md)
│   ├── calisma_ve_ders_programi/             # 40 saatlik okul çizelgesi ve StudyTracker köprü planı
│   ├── kelime_listeleri/                     # Yabancı dil (İngilizce/Almanca) hedef kelime listeleri
│   └── meb_kitap_baglantilari.md             # 10 adet resmî MEB öğrenci kitabının doğrudan indirme linkleri
├── data/
│   ├── defterdoldur_tum_dersler_9al.json     # 9 Dersin 41 haftalık doğrulanmış resmî JSON veritabanı
│   ├── defterdoldur_ilk_4_hafta_resmi_plan.md# İlk 4 haftanın tüm dersler resmî zümre plan özeti
│   ├── anki_decks/                           # Aralıklı tekrar soru-cevap desteleri (.txt ve .apkg)
│   ├── haftalik_planlar/                     # StudyTracker uyumlu .studyplan paketleri
│   └── meb_kitaplari/                        # MEB ders kitapları yapılandırılmış metin özetleri (.md)
└── scripts/
    ├── download_student_textbooks.py         # Resmî MEB PDF'lerini tek komutla indiren betik
    └── verify_anki_decks.py                  # Anki kart sözdizimi ve bütünlük doğrulama aracı
```

---

## 📅 1. Maarif Modeli Yıllık Zümre Planları (`curriculum/yillik_planlar/`)

DefterDoldur.com kaynaklı 9 akademik branşın 39-41 haftalık eksiksiz planları:

1. [📐 Matematik Yıllık Planı](curriculum/yillik_planlar/Matematik_Yillik_Plan_AL9.md) (41 Hafta - Sayılar & Gerçek Sayılar)
2. [⚡ Fizik Yıllık Planı](curriculum/yillik_planlar/Fizik_Yillik_Plan_AL9.md) (39 Hafta - Fizik Bilimi, Kuvvet & Hareket)
3. [🧪 Kimya Yıllık Planı](curriculum/yillik_planlar/Kimya_Yillik_Plan_AL9.md) (41 Hafta - Etkileşim & Güvenlik)
4. [🧬 Biyoloji Yıllık Planı](curriculum/yillik_planlar/Biyoloji_Yillik_Plan_AL9.md) (41 Hafta - Yaşam & Dönüm Noktaları)
5. [🏛️ Tarih Yıllık Planı](curriculum/yillik_planlar/Tarih_Yillik_Plan_AL9.md) (41 Hafta - Geçmişin İnşa Sürecinde Tarih)
6. [🌍 Coğrafya Yıllık Planı](curriculum/yillik_planlar/Cografya_Yillik_Plan_AL9.md) (41 Hafta - Coğrafyanın Doğası & Mekânsal Bilgi)
7. [📖 Türk Dili ve Edebiyatı Yıllık Planı](curriculum/yillik_planlar/TDE_Yillik_Plan_AL9.md) (41 Hafta - Sözün İnceliği & Anlatmaya Bağlı Metinler)
8. [🇬🇧 İngilizce Yıllık Planı](curriculum/yillik_planlar/İngilizce_Yillik_Plan_AL9.md) (41 Hafta - Orientation & School Life)
9. [🇩🇪 Almanca Yıllık Planı](curriculum/yillik_planlar/Almanca_Yillik_Plan_AL9.md) (41 Hafta - Modul 1: Hallo! & Begrüßung)

---

## 🎬 2. Video Ders ve Öğretmen Kürasyonları (`curriculum/video_rehberleri/`)

- [📐 1. Ay Matematik Video Rehberi](curriculum/video_rehberleri/1_ay_matematik_khan_academy_videolari.md) (Khan Academy Türkçe)
- [⚡ 1. Ay Fizik Video Rehberi](curriculum/video_rehberleri/1_ay_fizik_video_rehberi.md) (Khan Academy, VIP Fizik, Özcan Aykın)
- [🧪 1. Ay Kimya Video Rehberi](curriculum/video_rehberleri/1_ay_kimya_video_rehberi.md) (Khan Academy, Görkem Şahin)
- [🧬 1. Ay Biyoloji Video Rehberi](curriculum/video_rehberleri/1_ay_biyoloji_video_rehberi.md) (Khan Academy, Biosem, Selin Hoca)
- [🏛️ 1. Ay Tarih Video Rehberi](curriculum/video_rehberleri/1_ay_tarih_video_rehberi.md) (Mehmet Celal ÖZYILDIZ)
- [🌍 1. Ay Coğrafya Video Rehberi](curriculum/video_rehberleri/1_ay_cografya_video_rehberi.md) (Coğrafyanın Kodları, Engin Eraydın)
- [🇬🇧 1. Ay İngilizce Video Rehberi](curriculum/video_rehberleri/1_ay_ingilizce_video_rehberi.md) (Özer Kiraz, Hocalara Geldik)
- [🇩🇪 1. Ay Almanca Video Rehberi](curriculum/video_rehberleri/1_ay_almanca_video_rehberi.md) (Almanca Kolay, Meltem Hoca)

---

## 📖 3. Resmî MEB Ders Kitapları Politikası (Hafif Depo İlkesi)

Git reposunun hızlı klonlanabilmesi ve depolama limitlerine takılmaması amacıyla **1.3 GB'lık PDF kitap dosyaları bu depoya binary olarak yüklenmez**.
Bunun yerine:
1. Resmî doğrudan indirme bağlantıları tablosuna **[`curriculum/meb_kitap_baglantilari.md`](curriculum/meb_kitap_baglantilari.md)** üzerinden erişilebilir.
2. Yerel ortamda çalışırken tüm kitaplar tek komutla otomatik olarak çekilebilir:
   ```bash
   python3 scripts/download_student_textbooks.py
   ```
3. Ders kitaplarından çıkarılmış temiz metin özetleri ve ünite markdown'ları doğrudan [`data/meb_kitaplari/`](data/meb_kitaplari/) altında incelenebilir.

---

## 🌉 4. StudyTracker Entegrasyonu

Bu depodaki tüm yıllık planlar, kazanım ID'leri (`MAT.9.1.1`, `FİZ.9.2.1` vb.) ve quiz soruları, **[TheOsmanYILDIRIM/study-tracker](https://github.com/TheOsmanYILDIRIM/study-tracker)** mobil uygulamasının `content/9-sinif-v2-catalog.json` kataloğu ile birebir mutabıktır.
Haftalık ders saati senkronizasyonu için [40 Saatlik Resmî Haftalık Ders Programı Çizelgesi](curriculum/calisma_ve_ders_programi/9-sinif-haftalik-ders-programi-ve-koyrusu.md) kullanılmaktadır.
