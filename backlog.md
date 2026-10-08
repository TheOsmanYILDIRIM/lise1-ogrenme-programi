# Lise 1 (9. Sınıf) Ders Öğrenme Programı - Backlog

## Durum Özeti
- **Proje:** Lise 1 (9. Sınıf Anadolu Lisesi) Müfredat, Kitap Metinleri, Anki Kartları ve Video Öğrenme Ekosistemi
- **Tarih:** 2026-09-16
- **Aktif Durum:** [Tüm 9. Sınıf MEB Kitapları Resimli Markdown (.md) Olarak İndirildi ve Hazırlandı]

---

## 📋 Görev Listesi

### Aşama 2: Güncel MEB Öğrenci Ders Kitaplarını İndirme ve Plan Mutabakatı (TAMAMLANDI)
- [x] MEB TYMM (Türkiye Yüzyılı Maarif Modeli) portallarından güncel 10 adet 9. Sınıf Öğrenci Ders Kitabı (Biyoloji, Coğrafya, Din, Fizik, İngilizce, Kimya, Matematik 1 & 2, Tarih, TDE) resmî PDF'leri indirildi ve `pdftotext` ile metinleri ayrıştırıldı.
- [x] Yeni öğrenci kitaplarının 1. Ünite / İlk 4 Hafta içindekiler ve kazanım sıralaması 4 Haftalık Çalışma Planı ve Anki desteleri ile %100 mutabakat sağlandı.
- [x] Proje `INDEX.md`, `log.md` ve Vault kayıtları senkronize edildi.

### Aşama 2: Ders Kitapları İçerik & Müfredat Özeti
- [x] 9. Sınıf tüm ana derslerinin (Matematik, Fizik, Kimya, Biyoloji, Tarih, Coğrafya) ünite ve kritik konu başlıkları yapılandırıldı.

### Aşama 3: Video Oynatma Listeleri & Kanal Kürasyonu (TAMAMLANDI)
- [x] Sayısal (Mat, Fizik, Kimya) için Khan Academy Türkçe ve alternatif en iyi MEB uyumlu kanallar belirlendi.
- [x] Sözel/Görsel (Tarih, Coğrafya, Biyoloji) için Coğrafyanın Kodları, Biosem, Benim Hocam video eşleştirmesi hazırlandı (`data/video_curation/9_sinif_video_rehberi.md`).

### Aşama 4: Anki Kartları & Flashcard Sistemi (TAMAMLANDI)
- [x] `study-forge` skill motoru geliştirildi (`~/.agents/skills/study-forge/SKILL.md`).
- [x] Coğrafya 9 (1. Ay) - 24 Görsel/Sesli Nokta Atışı Kart (`9_sinif_cografya_1_ay.apkg`).
- [x] İngilizce 9 (1. Ay / Theme 1 & 2) - 62 Görsel Sözlüklü Kart (`9_sinif_ingilizce_1_ay.apkg`).
- [x] Almanca 9 (1. Ay / Modul 1) - 39 Görsel Sözlüklü Kart (`9_sinif_almanca_1_ay.apkg`).
- [x] Tek geçişli `CleanPackage` mimarisi ile AnkiDroid "Yüklenemedi" hatası çözüldü.
- [x] Görseller 512px / 40KB sıkıştırıldı; kart çevrilme kristal çan SFX'i eklendi.
- [x] Tüm APKG'ler `/storage/emulated/0/Download/` ve `~/vault/10-Projects/` altına senkronize edildi.

### Aşama 5: 4 Haftalık Maarif Modeli & StudyTracker Çalışma Planı (TAMAMLANDI)
- [x] Okul haftalık 40 saatlik ders çizelgesi ile senkronize 4 haftalık asıl çalışma ve pekiştirme planı oluşturuldu (`~/vault/10-Projects/9_sinif_4_haftalik_studytracker_calisma_plani.md`).
- [x] 3 hazır Anki destesi (Coğrafya, İngilizce, Almanca) ve çözümlü mikro pekiştirme soruları günde 35-70 dk'lık ultra hafif seanslara dağıtıldı.
- [x] StudyTracker DSL formatında 4 haftalık doğrudan içe aktarılabilir kod blokları üretildi.
