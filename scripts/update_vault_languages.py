import json, os

vault_dir = "/storage/emulated/0/Documents/AGY-Vault/10-Projects/Lise-1-Yillik-Planlar"

# 1. Ingilizce Plan Dosyasi
ing_md = """# 9. Sınıf İngilizce (Birinci Yabancı Dil - 4 Saat) - Maarif Modeli Yıllık Planı

> **Kaynak:** MEB 9. Sınıf Maarif Modeli Öğretim Programı & Zenginleştirilmiş İngilizce Ders Kitabı
> **Ders:** İngilizce (AL-9) | **Haftalık Saat:** 4 Saat

---

## 📍 1. Hafta (14-18 Eylül) - 4 Saat
- **Ünite / Tema:** `Theme 1: SCHOOL LIFE`
- **Konu:** *Meet the Students of an International School* (Uluslararası Öğrenciler & Tanışma)
- **Kazanım:** `ENG.9.1.R2` & `ENG.9.1.R4`
- **Süreç ve Beceriler:** Ülkeler (*Countries*), milliyetler (*Nationalities*), diller (*Languages*), başkentler ve kendini tanıtma kalıpları (*Introducing oneself*).

---

## 📍 2. Hafta (21-25 Eylül) - 4 Saat
- **Ünite / Tema:** `Theme 1: SCHOOL LIFE`
- **Konu:** *Countries, Capitals & Tourist Attractions* (Başkentler ve Turistik Mekanlar)
- **Kazanım:** `ENG.9.1.W3`
- **Süreç ve Beceriler:** Başkentlerdeki aktiviteler, milli bayramlar ve kutlamalar (*National days & celebrations*) hakkında kısa paragraflar yazma.

---

## 📍 3. Hafta (05-09 Ekim) - 4 Saat
- **Ünite / Tema:** `Theme 2: CLASSROOM LIFE`
- **Konu:** *The Bell Rings, the Day Begins* (Günlük Rutinler ve Arkadaşlıklar)
- **Kazanım:** `ENG.9.2.L1` & `ENG.9.2.L2`
- **Süreç ve Beceriler:** Sınıf arkadaşları, dostluklar, günlük çalışma rutinleri ve okul alışkanlıkları (*Simple Present Tense* ile dinleme/anlama).

---

## 📍 4. Hafta (12-16 Ekim) - 4 Saat
- **Ünite / Tema:** `Theme 2: CLASSROOM LIFE`
- **Konu:** *Study Habits & Classroom Interactions* (*Guess Who?*)
- **Kazanım:** `ENG.9.2.S6`
- **Süreç ve Beceriler:** Sınıf içi etkileşimler, ders çalışma alışkanlıkları ve rutinler üzerine konuşma pratikleri (*Speaking*).
"""

# 2. Almanca Plan Dosyasi
alm_md = """# 9. Sınıf Almanca (İkinci Yabancı Dil - 2 Saat) - Maarif Modeli Yıllık Planı

> **Kaynak:** MEB 9. Sınıf İkinci Yabancı Dil Almanca Öğretim Programı & Modül 1
> **Ders:** Almanca (AL-9) | **Haftalık Saat:** 2 Saat

---

## 📍 1. Hafta (14-18 Eylül) - 2 Saat
- **Modül / Ünite:** `Modul 1: HALLO! (Informationen zur Person)`
- **Konu:** *Guten Tag!* (Selamlaşma, Vedalaşma ve Almanca Alfabe)
- **Kazanım:** `ALM.9.1.1`
- **Süreç ve Beceriler:** *Guten Morgen, Hallo, Tschüss, Auf Wiedersehen* kalıpları ve isim harfleme (*Buchstabieren*).

---

## 📍 2. Hafta (21-25 Eylül) - 2 Saat
- **Modül / Ünite:** `Modul 1: HALLO! (Informationen zur Person)`
- **Konu:** *Erste Kontakte* (Kendini ve Başkalarını Tanıtma)
- **Kazanım:** `ALM.9.1.2`
- **Süreç ve Beceriler:** *Wie heißt du? - Ich heiße... / Wer bist du? - Ich bin...* ve *sein / heißen* fiil çekimleri.

---

## 📍 3. Hafta (05-09 Ekim) - 2 Saat
- **Modül / Ünite:** `Modul 1: HALLO! (Informationen zur Person)`
- **Konu:** *Zahlen (Sayılar 0-20) & Telefon Numarası*
- **Kazanım:** `ALM.9.1.3`
- **Süreç ve Beceriler:** Sayılar (*null bis zwanzig*) ve telefon numarası sorma (*Wie ist deine Telefonnummer?*).

---

## 📍 4. Hafta (12-16 Ekim) - 2 Saat
- **Modül / Ünite:** `Modul 1: HALLO! (Informationen zur Person)`
- **Konu:** *Länder und Sprachen* (Ülkeler ve Diller)
- **Kazanım:** `ALM.9.1.4`
- **Süreç ve Beceriler:** *Woher kommst du? - Ich komme aus... / Welche Sprachen sprichst du? - Ich spreche...*
"""

with open(os.path.join(vault_dir, "İngilizce_Birinci_Yabancı_Dil_Yillik_Plan_AL9.md"), "w", encoding="utf-8") as f:
    f.write(ing_md.strip())

with open(os.path.join(vault_dir, "Almanca_İkinci_Yabancı_Dil_Yillik_Plan_AL9.md"), "w", encoding="utf-8") as f:
    f.write(alm_md.strip())

print("✅ İngilizce ve Almanca planları Vault içerisinde güncellendi.")
