#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
study-forge: 9. Sınıf Coğrafya 1. Ay Anki APKG Paketi (Clean Single-Pass Builder)
- 24 Adet Nokta Atışı Coğrafya Kartı (Maksimum 1 Cümlelik Net Tanım)
- Sıfır Gereksiz Tekrar (Sentence ve Translation kaldırıldı)
- Hızlı ve Vurucu Türkçe Azure Neural TTS Stüdyo Sesleri (tr-TR-AhmetNeural)
- Kart Çevrildiğinde Kristal Çan SFX Efekti (sfx_chime.mp3)
- Sıkıştırılmış Cloudflare Workers AI Vektörel Görselleri (512px / ~40KB)
- AnkiDroid Uyumlu Temiz Single-Pass APKG Mimarisi
"""

import os
import sys
import json
import time
import asyncio
import subprocess
import hashlib
import edge_tts
import genanki
import shutil
from PIL import Image

CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
CF_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
VOICE_TR = "tr-TR-AhmetNeural"

class CleanPackage(genanki.Package):
    def __init__(self, decks, media_files=None, daily_limit=15):
        super().__init__(decks)
        self.media_files = media_files or []
        self.daily_limit = daily_limit

    def write_to_db(self, cursor, timestamp: float, id_gen):
        super().write_to_db(cursor, timestamp, id_gen)
        cursor.execute('SELECT dconf FROM col')
        row = cursor.fetchone()
        if row and row[0]:
            dconf = json.loads(row[0])
            for k in dconf:
                dconf[k]['new']['perDay'] = self.daily_limit
                dconf[k]['autoplay'] = True
                dconf[k]['replayq'] = True
            cursor.execute('UPDATE col SET dconf = ?', (json.dumps(dconf),))

COGRAFYA_DATA = [
    # 1. Hafta: Doğa, İnsan ve 4 Temel Ortam
    {
        "subdeck": "9. Sınıf Coğrafya::1. Hafta: Doğa, İnsan ve 4 Temel Ortam",
        "badge": "1. Hafta: Doğa & İnsan",
        "word": "Muhteşem Dörtlü (4 Temel Ortam)",
        "tts_text": "Doğal çevreyi oluşturan dört temel ortam litosfer, atmosfer, hidrosfer ve biyosferdir.",
        "phonetic": "",
        "word_type": "Temel Kavram",
        "type_class": "noun",
        "meaning": "Doğal çevreyi oluşturan dört temel ortam litosfer (taş), atmosfer (hava), hidrosfer (su) ve biyosferdir (canlı).",
        "sentence": "",
        "translation": "",
        "tip": "Bu dört küre birbirine bağımlıdır; birindeki değişim diğerlerini doğrudan etkiler.",
        "image": "flux_v3_cog_muhtesem_dortlu.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::1. Hafta: Doğa, İnsan ve 4 Temel Ortam",
        "badge": "1. Hafta: Doğa & İnsan",
        "word": "Litosfer (Taş Küre)",
        "tts_text": "Litosfer; kıtaları, dağları, ovaları ve kayaçları kapsayan katı yer kabuğudur.",
        "phonetic": "",
        "word_type": "Doğal Ortam",
        "type_class": "noun",
        "meaning": "Kıtaları, dağları, ovaları, kayaç ve toprakları kapsayan katı yer kabuğudur.",
        "sentence": "",
        "translation": "",
        "tip": "Jeomorfoloji bilimi litosfer üzerindeki yer şekillerini inceler.",
        "image": "flux_v3_cog_litosfer.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::1. Hafta: Doğa, İnsan ve 4 Temel Ortam",
        "badge": "1. Hafta: Doğa & İnsan",
        "word": "Atmosfer (Hava Küre)",
        "tts_text": "Atmosfer, Dünya'yı saran ve hava olaylarının gerçekleştiği gaz örtüsüdür.",
        "phonetic": "",
        "word_type": "Doğal Ortam",
        "type_class": "noun",
        "meaning": "Dünya'yı çevreleyen ve tüm hava olaylarının yaşandığı koruyucu gaz örtüsüdür.",
        "sentence": "",
        "translation": "",
        "tip": "Su buharının tamamı atmosferin en alt katmanı olan Troposfer'de bulunur.",
        "image": "flux_v3_cog_atmosfer.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::1. Hafta: Doğa, İnsan ve 4 Temel Ortam",
        "badge": "1. Hafta: Doğa & İnsan",
        "word": "Hidrosfer (Su Küre)",
        "tts_text": "Hidrosfer; okyanus, deniz, göl, akarsu ve yer altı sularından oluşan su tabakasıdır.",
        "phonetic": "",
        "word_type": "Doğal Ortam",
        "type_class": "noun",
        "meaning": "Okyanuslar, denizler, göller, akarsular, buzullar ve yer altı sularından oluşan su tabakasıdır.",
        "sentence": "",
        "translation": "",
        "tip": "Dünya yüzeyinin yaklaşık yüzde 71'ini kaplar.",
        "image": "flux_v3_cog_hidrosfer.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::1. Hafta: Doğa, İnsan ve 4 Temel Ortam",
        "badge": "1. Hafta: Doğa & İnsan",
        "word": "Biyosfer (Canlı Küre)",
        "tts_text": "Biyosfer, taş, hava ve su küre içinde yaşayan tüm canlılar topluluğudur.",
        "phonetic": "",
        "word_type": "Doğal Ortam",
        "type_class": "noun",
        "meaning": "Litosfer, atmosfer ve hidrosfer içerisinde yaşamını sürdüren tüm canlılar küresidir.",
        "sentence": "",
        "translation": "",
        "tip": "Tek başına bağımsız bir katman olmayıp diğer 3 ortamın kesişiminde var olur.",
        "image": "flux_v3_cog_biyosfer.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::1. Hafta: Doğa, İnsan ve 4 Temel Ortam",
        "badge": "1. Hafta: Doğa & İnsan",
        "word": "Dağılış İlkesi",
        "tts_text": "Dağılış ilkesi, coğrafi olayların yeryüzündeki yayılışını harita ile gösteren temel ilkedir.",
        "phonetic": "",
        "word_type": "Coğrafya İlkesi",
        "type_class": "gram",
        "meaning": "Coğrafi olayların yeryüzündeki yayılış alanlarını harita ile açıklayan, yalnızca coğrafyaya özgü temel ilkedir.",
        "sentence": "",
        "translation": "",
        "tip": "Metinde 'Nerede görülür?' sorusuna haritalı yanıt varsa dağılış ilkesidir.",
        "image": "flux_v3_cog_dagilis_ilkesi.jpg"
    },

    # 2. Hafta: Dünya'nın Şekli ve Günlük Hareket
    {
        "subdeck": "9. Sınıf Coğrafya::2. Hafta: Dünya'nın Şekli ve Günlük Hareket",
        "badge": "2. Hafta: Şekil & Hareket",
        "word": "Geoit Şekil ve Sonuçları",
        "tts_text": "Dünya kutuplardan basık olduğu için yer çekimi kutuplarda ekvatordan fazladır.",
        "phonetic": "",
        "word_type": "Fiziki Özellik",
        "type_class": "noun",
        "meaning": "Dünya kutuplardan basık, Ekvatordan şişkin olduğu için yer çekimi Kutuplarda daha fazladır.",
        "sentence": "",
        "translation": "",
        "tip": "3 Kanıt: Ekvator yarıçapı > Kutup yarıçapı, Ekvator çevresi > Kutuplar, Kutuplarda yer çekimi fazlalığı.",
        "image": "flux_v3_cog_geoit.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::2. Hafta: Dünya'nın Şekli ve Günlük Hareket",
        "badge": "2. Hafta: Şekil & Hareket",
        "word": "Çizgisel Hız",
        "tts_text": "Çizgisel hız ekvatorda en fazla olup kutuplara gidildikçe azalır.",
        "phonetic": "",
        "word_type": "Fiziki Kavram",
        "type_class": "noun",
        "meaning": "Dünya'nın dönüş hızı Ekvatorda maksimum, Kutuplarda sıfırdır; bu yüzden alacakaranlık süresi kutuplarda daha uzundur.",
        "sentence": "",
        "translation": "",
        "tip": "Açısal hız her enlemde aynıyken, çizgisel hız kutuplara gidildikçe azalır.",
        "image": "flux_v3_cog_cizgisel_hiz.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::2. Hafta: Dünya'nın Şekli ve Günlük Hareket",
        "badge": "2. Hafta: Şekil & Hareket",
        "word": "Günlük (Eksen) Hareketi",
        "tts_text": "Günlük hareket sonucunda gece gündüz ardalanır ve yerel saat farkları oluşur.",
        "phonetic": "",
        "word_type": "Hareket",
        "type_class": "verb",
        "meaning": "Dünya'nın batıdan doğuya 24 saatlik dönüşüyle gece-gündüz ardalanır, meltem rüzgarları ve yerel saat farkları oluşur.",
        "sentence": "",
        "translation": "",
        "tip": "Doğuda Güneş erken doğar ve yerel saat daima ileridir.",
        "image": "flux_v3_cog_gunluk_hareket.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::2. Hafta: Dünya'nın Şekli ve Günlük Hareket",
        "badge": "2. Hafta: Şekil & Hareket",
        "word": "Meltem Rüzgarları",
        "tts_text": "Meltem rüzgarları, gün içindeki sıcaklık ve basınç farkıyla yön değiştiren yerel rüzgarlardır.",
        "phonetic": "",
        "word_type": "Rüzgar Tipi",
        "type_class": "noun",
        "meaning": "Gün içinde karalar ile denizlerin farklı ısınıp soğumasıyla oluşan, yağış getirmeyen yerel rüzgarlardır.",
        "sentence": "",
        "translation": "",
        "tip": "Gündüz denizden karaya (deniz meltemi), gece karadan denize (kara meltemi) eser.",
        "image": "flux_v3_cog_meltem.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::2. Hafta: Dünya'nın Şekli ve Günlük Hareket",
        "badge": "2. Hafta: Şekil & Hareket",
        "word": "Koriolis (Sapma) Kuvveti",
        "tts_text": "Koriolis kuvvetiyle rüzgarlar Kuzey Yarımkürede sağa, Güney Yarımkürede sola sapar.",
        "phonetic": "",
        "word_type": "Fiziki Kuvvet",
        "type_class": "noun",
        "meaning": "Dünya'nın dönüşü nedeniyle sürekli rüzgarlar ve akıntılar Kuzey Yarımküre'de sağa, Güney Yarımküre'de sola sapar.",
        "sentence": "",
        "translation": "",
        "tip": "30° ve 60° dinamik basınç kuşaklarının oluşmasını sağlar.",
        "image": "flux_v3_cog_koriolis.jpg"
    },

    # 3. Hafta: Eksen Eğikliği ve Mevsimler
    {
        "subdeck": "9. Sınıf Coğrafya::3. Hafta: Eksen Eğikliği ve Mevsimler",
        "badge": "3. Hafta: Yıllık Hareket",
        "word": "Eksen Eğikliği (23° 27')",
        "tts_text": "Eksen eğikliği, mevsimlerin oluşmasını ve gece gündüz sürelerinin değişmesini sağlar.",
        "phonetic": "",
        "word_type": "Geometrik Konum",
        "type_class": "noun",
        "meaning": "Yer ekseninin 23° 27' eğik olması mevsimlerin oluşmasını ve gece-gündüz sürelerinin yıl boyunca değişmesini sağlar.",
        "sentence": "",
        "translation": "",
        "tip": "Eksen eğikliği olmasaydı her enlemde yıl boyunca tek bir mevsim yaşanırdı.",
        "image": "flux_v3_cog_eksen_egikligi.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::3. Hafta: Eksen Eğikliği ve Mevsimler",
        "badge": "3. Hafta: Yıllık Hareket",
        "word": "21 Mart ve 23 Eylül (Ekinokslar)",
        "tts_text": "Ekinoks tarihlerinde Güneş Ekvatora dik gelir ve tüm Dünya'da gece gündüz eşittir.",
        "phonetic": "",
        "word_type": "Özel Tarih",
        "type_class": "expr",
        "meaning": "Güneş ışınları Ekvator'a dik düşer ve tüm Dünya'da 12 saat gece, 12 saat gündüz eşitliği yaşanır.",
        "sentence": "",
        "translation": "",
        "tip": "Aydınlanma çemberi kutup noktalarından teğet geçer.",
        "image": "flux_v3_cog_ekinoks.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::3. Hafta: Eksen Eğikliği ve Mevsimler",
        "badge": "3. Hafta: Yıllık Hareket",
        "word": "21 Haziran (Yaz Solstisi)",
        "tts_text": "21 Haziran'da Kuzey Yarımkürede en uzun gündüz ve en kısa gece yaşanır.",
        "phonetic": "",
        "word_type": "Özel Tarih",
        "type_class": "expr",
        "meaning": "Güneş Yengeç Dönencesi'ne dik gelir; Kuzey Yarımküre'de en uzun gündüz, en kısa gece yaşanır.",
        "sentence": "",
        "translation": "",
        "tip": "Türkiye'de kuzeye (Sinop'a) gidildikçe gündüz süresi uzar.",
        "image": "flux_v3_cog_21_haziran.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::3. Hafta: Eksen Eğikliği ve Mevsimler",
        "badge": "3. Hafta: Yıllık Hareket",
        "word": "21 Aralık (Kış Solstisi)",
        "tts_text": "21 Aralık'ta Kuzey Yarımkürede en uzun gece yaşanır ve kış mevsimi başlar.",
        "phonetic": "",
        "word_type": "Özel Tarih",
        "type_class": "expr",
        "meaning": "Güneş Oğlak Dönencesi'ne dik gelir; Kuzey Yarımküre'de en uzun gece, en kısa gündüz yaşanır.",
        "sentence": "",
        "translation": "",
        "tip": "Türkiye'de güneye (Hatay'a) gidildikçe gündüz süresi uzar.",
        "image": "flux_v3_cog_21_aralik.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::3. Hafta: Eksen Eğikliği ve Mevsimler",
        "badge": "3. Hafta: Yıllık Hareket",
        "word": "Aydınlanma Çemberi",
        "tts_text": "Aydınlanma çemberi, Dünya'nın gündüz ile gece yarısını ayıran sınır çizgisidir.",
        "phonetic": "",
        "word_type": "Fiziki Sınır",
        "type_class": "noun",
        "meaning": "Dünya'nın Güneş gören aydınlık gündüz tarafı ile karanlık gece tarafını ayıran sınırdır.",
        "sentence": "",
        "translation": "",
        "tip": "Ekvator'u daima ikiye böldüğü için Ekvator'da yıl boyu 12 saat gündüz, 12 saat gece yaşanır.",
        "image": "flux_v3_cog_aydinlanma_cemberi.jpg"
    },

    # 4. Hafta: Harita Bilgisi ve İzohipsler
    {
        "subdeck": "9. Sınıf Coğrafya::4. Hafta: Harita Bilgisi ve İzohipsler",
        "badge": "4. Hafta: Harita Bilgisi",
        "word": "Paraleller ve Enlem",
        "tts_text": "Paraleller arası kuş uçuşu mesafe Dünya'nın her yerinde 111 kilometredir.",
        "phonetic": "",
        "word_type": "Koordinat",
        "type_class": "noun",
        "meaning": "Ekvator'a paralel uzanan hayali çemberlerdir ve ardışık iki paralel arası mesafe daima 111 kilometredir.",
        "sentence": "",
        "translation": "",
        "tip": "Toplam 180 paralel vardır; çevre uzunlukları kutuplara doğru daralır.",
        "image": "flux_v3_cog_paraleller.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::4. Hafta: Harita Bilgisi ve İzohipsler",
        "badge": "4. Hafta: Harita Bilgisi",
        "word": "Meridyenler ve Yerel Saat",
        "tts_text": "Ardışık iki meridyen arasındaki yerel saat farkı her yerde 4 dakikadır.",
        "phonetic": "",
        "word_type": "Koordinat",
        "type_class": "noun",
        "meaning": "Kutupları birleştiren 360 adet yarım çemberdir ve ardışık iki meridyen arası zaman farkı daima 4 dakikadır.",
        "sentence": "",
        "translation": "",
        "tip": "Başlangıç meridyeni Greenwich'tir (0°); doğuda yerel saat daima ileridir.",
        "image": "flux_v3_cog_meridyenler.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::4. Hafta: Harita Bilgisi ve İzohipsler",
        "badge": "4. Hafta: Harita Bilgisi",
        "word": "Türkiye'nin Mutlak Konumu",
        "tts_text": "Türkiye, 36-42 Kuzey paralelleri ve 26-45 Doğu meridyenleri arasındadır.",
        "phonetic": "",
        "word_type": "Matematik Konum",
        "type_class": "noun",
        "meaning": "Türkiye; 36°-42° Kuzey paralelleri ile 26°-45° Doğu meridyenleri arasında, Orta Kuşak'ta yer alır.",
        "sentence": "",
        "translation": "",
        "tip": "Kuzey-Güney mesafesi 666 km (6 x 111), Doğu-Batı zaman farkı 76 dakikadır (19 x 4).",
        "image": "flux_v3_cog_turkiye_konum.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::4. Hafta: Harita Bilgisi ve İzohipsler",
        "badge": "4. Hafta: Harita Bilgisi",
        "word": "Harita Projeksiyonları",
        "tts_text": "Konik projeksiyon Türkiye ve orta kuşağı, silindirik Ekvatoru en az hatayla çizer.",
        "phonetic": "",
        "word_type": "Harita Yöntemi",
        "type_class": "noun",
        "meaning": "Silindirik projeksiyon Ekvator'u, Konik projeksiyon orta kuşağı (Türkiye), Düzlem projeksiyon ise kutupları en az hatayla çizer.",
        "sentence": "",
        "translation": "",
        "tip": "Küre düzleme aktarılırken bozulma kaçınılmazdır; projeksiyonlar hatayı minimize eder.",
        "image": "flux_v3_cog_projeksiyonlar.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::4. Hafta: Harita Bilgisi ve İzohipsler",
        "badge": "4. Hafta: Harita Bilgisi",
        "word": "İzohipslerde Eğim ve Sıklaşma",
        "tts_text": "İzohipslerin sıklaştığı yerlerde eğim artar ve akarsu akış hızı yükselir.",
        "phonetic": "",
        "word_type": "Harita Kuralı",
        "type_class": "gram",
        "meaning": "Eş yükselti eğrilerinin sıklaştığı yerlerde eğim artar, akarsu hızlı akar ve kıyıda falez (yalıyar) oluşur.",
        "sentence": "",
        "translation": "",
        "tip": "Eğrilerin seyrekleştiği yerlerde arazi düzdür ve akarsu menderes çizer.",
        "image": "flux_v3_cog_izohips_egim.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::4. Hafta: Harita Bilgisi ve İzohipsler",
        "badge": "4. Hafta: Harita Bilgisi",
        "word": "İzohips: Vadi ve Sırt Ayrımı",
        "tts_text": "İzohipslerde V harfinin ucu yüksekliğe bakıyorsa vadi, alçaklığa bakıyorsa sırttır.",
        "phonetic": "",
        "word_type": "Yer Şekli",
        "type_class": "noun",
        "meaning": "V harfinin sivri ucu yüksekliğe (kaynağa) bakıyorsa vadi, alçaklığa bakıyorsa sırttır.",
        "sentence": "",
        "translation": "",
        "tip": "Haritada akarsu çizgisi varsa o şekil kesinlikle vadidir.",
        "image": "flux_v3_cog_vadi_sirt.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::4. Hafta: Harita Bilgisi ve İzohipsler",
        "badge": "4. Hafta: Harita Bilgisi",
        "word": "İzohips: Boyun, Çukur ve Falez",
        "tts_text": "İki tepe arasındaki düzlük boyun, içe oklar kapalı çanak çukurdur.",
        "phonetic": "",
        "word_type": "Yer Şekilleri",
        "type_class": "noun",
        "meaning": "İki tepe arası boyun, içe doğru oklar kapalı çukur (çanak), dik kıyı uçurumu ise falezdir.",
        "sentence": "",
        "translation": "",
        "tip": "Kapalı çukurda içe doğru ok boyunca yükselti azalır.",
        "image": "flux_v3_cog_boyun_falez.jpg"
    },
    {
        "subdeck": "9. Sınıf Coğrafya::4. Hafta: Harita Bilgisi ve İzohipsler",
        "badge": "4. Hafta: Harita Bilgisi",
        "word": "İzohips: Delta Ovası",
        "tts_text": "Delta ovası, akarsuyun denizi doldurmasıyla oluşan verimli üçgen birikintidir.",
        "phonetic": "",
        "word_type": "Yer Şekli",
        "type_class": "noun",
        "meaning": "Akarsuyun taşıdığı alüvyonları deniz kıyısında biriktirmesiyle oluşan verimli üçgen çıkıntıdır.",
        "sentence": "",
        "translation": "",
        "tip": "Delta olan kıyılarda kıyı sığdır (kıta sahanlığı geniştir) ve falez oluşamaz.",
        "image": "flux_v3_cog_delta.jpg"
    }
]

async def generate_concise_audio(items, media_dir):
    print("🎙️ Kısa & Öz Türkçe Azure Neural TTS stüdyo sesleri üretiliyor (Maks 1 Cümle)...")
    for idx, item in enumerate(items):
        fname = f"cog_{idx+1:02d}.mp3"
        fpath = os.path.join(media_dir, fname)
        if not (os.path.exists(fpath) and os.path.getsize(fpath) > 200):
            comm = edge_tts.Communicate(item["tts_text"], VOICE_TR)
            await comm.save(fpath)
        item["audio_fname"] = fname
        # Anki standard sequential sound tag: chime followed by voice
        item["audio_tag"] = f"[sound:sfx_chime.mp3][sound:{fname}]"
    print("✅ 24 Kısa & Öz ses dosyası tamamlandı.")

def compress_and_optimize_image(img_path, max_dim=512, quality=75):
    try:
        im = Image.open(img_path)
        im = im.convert('RGB')
        im.thumbnail((max_dim, max_dim), Image.Resampling.LANCZOS)
        im.save(img_path, format='JPEG', quality=quality, optimize=True)
    except Exception as e:
        print(f"Uyarı: Görsel sıkıştırma hatası ({img_path}):", e)

def build_cografya_apkg():
    media_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "anki_decks", "media"))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "anki_decks"))
    os.makedirs(media_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Sesler (Kısa & Öz)
    asyncio.run(generate_concise_audio(COGRAFYA_DATA, media_dir))
    
    # 2. Şablonlar & CSS
    skill_dir = os.path.expanduser("~/.agents/skills/study-forge/templates")
    with open(os.path.join(skill_dir, "card_styles.css"), "r", encoding="utf-8") as f:
        card_css = f.read()
    with open(os.path.join(skill_dir, "front_template.html"), "r", encoding="utf-8") as f:
        front_html = f.read()
    with open(os.path.join(skill_dir, "back_template.html"), "r", encoding="utf-8") as f:
        back_html = f.read()
        
    cog_model = genanki.Model(
        2026091703,
        '9. Sınıf Coğrafya Görsel Sözlük',
        fields=[
            {'name': 'Word'},
            {'name': 'Phonetic'},
            {'name': 'WordType'},
            {'name': 'WordTypeClass'},
            {'name': 'Meaning'},
            {'name': 'ExampleSentence'},
            {'name': 'ExampleTranslation'},
            {'name': 'ExtraTip'},
            {'name': 'SubdeckName'},
            {'name': 'Image'},
            {'name': 'Audio'}
        ],
        templates=[
            {
                'name': 'Coğrafya Kartı',
                'qfmt': front_html,
                'afmt': back_html,
            }
        ],
        css=card_css
    )
    
    main_deck = genanki.Deck(2026091700, "9. Sınıf Coğrafya")
    subdecks = {
        "9. Sınıf Coğrafya::1. Hafta: Doğa, İnsan ve 4 Temel Ortam": genanki.Deck(2026091703, "9. Sınıf Coğrafya::1. Hafta: Doğa, İnsan ve 4 Temel Ortam"),
        "9. Sınıf Coğrafya::2. Hafta: Dünya'nın Şekli ve Günlük Hareket": genanki.Deck(2026091703, "9. Sınıf Coğrafya::2. Hafta: Dünya'nın Şekli ve Günlük Hareket"),
        "9. Sınıf Coğrafya::3. Hafta: Eksen Eğikliği ve Mevsimler": genanki.Deck(2026091704, "9. Sınıf Coğrafya::3. Hafta: Eksen Eğikliği ve Mevsimler"),
        "9. Sınıf Coğrafya::4. Hafta: Harita Bilgisi ve İzohipsler": genanki.Deck(2026091705, "9. Sınıf Coğrafya::4. Hafta: Harita Bilgisi ve İzohipsler"),
    }
    
    media_files = []
    sfx_path = os.path.join(media_dir, "sfx_chime.mp3")
    if os.path.exists(sfx_path):
        media_files.append(sfx_path)
        
    for item in COGRAFYA_DATA:
        sname = item["subdeck"]
        badge_name = item.get("badge", sname.split("::")[-1])
        
        aud_path = os.path.join(media_dir, item["audio_fname"])
        if os.path.exists(aud_path) and aud_path not in media_files:
            media_files.append(aud_path)
            
        img_path = os.path.join(media_dir, item["image"])
        item["image_tag"] = f'<img src="{item["image"]}" class="vd-img">'
        if os.path.exists(img_path):
            compress_and_optimize_image(img_path, max_dim=512, quality=75)
            if img_path not in media_files:
                media_files.append(img_path)
            
        guid_val = hashlib.sha256(f"cografya_9_{item['word']}".encode('utf-8')).hexdigest()[:10]
        note = genanki.Note(
            model=cog_model,
            fields=[
                item["word"],
                item["phonetic"],
                item["word_type"],
                item["type_class"],
                item["meaning"],
                item["sentence"],
                item["translation"],
                item["tip"],
                badge_name,
                item["image_tag"],
                item["audio_tag"]
            ],
            guid=guid_val
        )
        subdecks[sname].add_note(note)
        
    out_apkg = os.path.join(output_dir, "9_sinif_cografya_1_ay.apkg")
    pkg = CleanPackage([main_deck] + list(subdecks.values()), media_files=media_files, daily_limit=15)
    pkg.write_to_file(out_apkg)
    print(f"📦 Coğrafya APKG tek geçişte temiz derlendi: {out_apkg} (Toplam Medya: {len(media_files)})")
    
    # Deploy to Download and Vault
    dl_path = os.path.join("/storage/emulated/0/Download", "9_sinif_cografya_1_ay.apkg")
    vault_path = os.path.join("/data/data/com.termux/files/home/vault/10-Projects", "9_sinif_cografya_1_ay.apkg")
    
    if os.path.exists("/storage/emulated/0/Download"):
        shutil.copy2(out_apkg, dl_path)
        print(f"✅ Download klasörüne aktarıldı: {dl_path} ({os.path.getsize(dl_path)} bytes)")
    if os.path.exists("/data/data/com.termux/files/home/vault/10-Projects"):
        shutil.copy2(out_apkg, vault_path)
        print(f"✅ Vault'a aktarıldı: {vault_path}")

if __name__ == "__main__":
    build_cografya_apkg()
