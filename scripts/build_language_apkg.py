#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
9. Sınıf İngilizce ve Almanca 1. Ay Anki APKG Üretici
- Gerçek Görsel Sözlük (Visual Dictionary) Resimleri (.jpg)
- Microsoft Azure Neural TTS Stüdyo Sesleri ([sound:xxx.mp3])
- Ünite Bazlı Alt Desteler (Theme 1, Theme 2 / Modul 1)
- Dahili Günlük 15 Yeni Kart Limiti (dconf new.perDay = 15)
- Modern Dark & Light CSS Kart Tasarımı
"""

import os
import sys
import asyncio
import re
import json
import zipfile
import sqlite3
import tempfile
import shutil
import hashlib
import genanki
import edge_tts

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

VOICE_EN = "en-US-AriaNeural"
VOICE_DE = "de-DE-KatjaNeural"

CARD_CSS = """
.card {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 16px;
    text-align: center;
    color: #1e293b;
    background-color: #f8fafc;
    padding: 12px;
    margin: 0;
    line-height: 1.5;
}

@media (prefers-color-scheme: dark) {
    .card {
        color: #f1f5f9;
        background-color: #0f172a;
    }
}

.anki-container {
    max-width: 440px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 20px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08), 0 8px 10px -6px rgba(0, 0, 0, 0.04);
    border: 1px solid #e2e8f0;
    overflow: hidden;
    padding: 20px 18px;
    transition: all 0.3s ease;
}

@media (prefers-color-scheme: dark) {
    .anki-container {
        background: #1e293b;
        border-color: #334155;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
    }
}

.deck-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #475569;
    background: #f1f5f9;
    padding: 4px 12px;
    border-radius: 9999px;
    margin-bottom: 12px;
    border: 1px solid #e2e8f0;
}

@media (prefers-color-scheme: dark) {
    .deck-tag {
        color: #94a3b8;
        background: #334155;
        border-color: #475569;
    }
}

.visual-box {
    margin: 10px auto 14px;
    width: 100%;
    max-width: 360px;
    border-radius: 14px;
    overflow: hidden;
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}

@media (prefers-color-scheme: dark) {
    .visual-box {
        background: #1e293b;
        border-color: #334155;
    }
}

.visual-box img, .vd-img {
    width: 100% !important;
    max-width: 100% !important;
    height: auto !important;
    max-height: 240px !important;
    min-height: 140px !important;
    object-fit: cover !important;
    display: block !important;
    margin: 0 auto !important;
    border-radius: 12px !important;
}

.target-word {
    font-size: 26px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
    margin: 6px 0 2px;
}

@media (prefers-color-scheme: dark) {
    .target-word {
        color: #38bdf8;
    }
}

.voice-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    font-weight: 600;
    color: #0284c7;
    background: #e0f2fe;
    padding: 2px 8px;
    border-radius: 6px;
    margin-bottom: 6px;
}

@media (prefers-color-scheme: dark) {
    .voice-badge {
        color: #38bdf8;
        background: #0369a133;
    }
}

.phonetic-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: #64748b;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 3px 10px;
    border-radius: 8px;
    margin-bottom: 10px;
}

@media (prefers-color-scheme: dark) {
    .phonetic-pill {
        color: #cbd5e1;
        background: #0f172a;
        border-color: #334155;
    }
}

.badge {
    display: inline-block;
    font-size: 12px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 6px;
    margin-left: 6px;
}

.badge-noun { background: #e0f2fe; color: #0284c7; }
.badge-verb { background: #dcfce7; color: #16a34a; }
.badge-adj { background: #f3e8ff; color: #9333ea; }
.badge-expr { background: #fef3c7; color: #d97706; }
.badge-gram { background: #ffe4e6; color: #e11d48; }

.divider {
    height: 1px;
    background: #e2e8f0;
    margin: 16px 0;
}

@media (prefers-color-scheme: dark) {
    .divider { background: #334155; }
}

.meaning-card {
    background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    border: 1px solid #bfdbfe;
    border-radius: 14px;
    padding: 12px 14px;
    margin-bottom: 14px;
}

@media (prefers-color-scheme: dark) {
    .meaning-card {
        background: linear-gradient(135deg, #1e3a8a33 0%, #1e40af44 100%);
        border-color: #1d4ed8;
    }
}

.meaning-title {
    font-size: 19px;
    font-weight: 800;
    color: #1d4ed8;
    margin-bottom: 2px;
}

@media (prefers-color-scheme: dark) {
    .meaning-title {
        color: #60a5fa;
    }
}

.example-box {
    text-align: left;
    background: #f8fafc;
    border-left: 4px solid #3b82f6;
    border-radius: 0 10px 10px 0;
    padding: 12px 14px;
    margin-top: 12px;
}

@media (prefers-color-scheme: dark) {
    .example-box {
        background: #0f172a;
        border-left-color: #38bdf8;
    }
}

.example-sentence {
    font-size: 14px;
    font-weight: 600;
    color: #334155;
    margin-bottom: 4px;
}

@media (prefers-color-scheme: dark) {
    .example-sentence {
        color: #e2e8f0;
    }
}

.example-translation {
    font-size: 13px;
    color: #64748b;
    font-style: italic;
}

@media (prefers-color-scheme: dark) {
    .example-translation {
        color: #94a3b8;
    }
}

.tip-banner {
    background: #fefce8;
    border: 1px dashed #facc15;
    border-radius: 8px;
    padding: 8px 10px;
    margin-top: 10px;
    font-size: 12px;
    color: #854d0e;
    text-align: left;
}

@media (prefers-color-scheme: dark) {
    .tip-banner {
        background: #713f1233;
        border-color: #ca8a04;
        color: #fde047;
    }
}
"""

FRONT_TEMPLATE = """
<div class="anki-container">
    <div class="deck-tag">{{SubdeckName}}</div>
    <div class="visual-box">
        {{Image}}
    </div>
    <div class="target-word">{{Word}}</div>
    <div>
        <span class="phonetic-pill">🔊 {{Phonetic}}</span>
        <span class="badge badge-{{WordTypeClass}}">{{WordType}}</span>
    </div>
</div>
"""

BACK_TEMPLATE = """
<div class="anki-container">
    <div class="deck-tag">{{SubdeckName}}</div>
    <div class="visual-box">
        {{Image}}
    </div>
    <div class="target-word">{{Word}}</div>
    <div>
        <span class="phonetic-pill">🔊 {{Phonetic}}</span>
        <span class="badge badge-{{WordTypeClass}}">{{WordType}}</span>
    </div>

    <div class="divider"></div>

    <div class="meaning-card">
        <div class="meaning-title">{{Meaning}}</div>
    </div>

    <div class="example-box">
        <div class="example-sentence">{{ExampleSentence}}</div>
        <div class="example-translation">{{ExampleTranslation}}</div>
    </div>

    {{#ExtraTip}}
    <div class="tip-banner">💡 <b>Not:</b> {{ExtraTip}}</div>
    {{/ExtraTip}}
    
    <div style="display:none;">{{Audio}}</div>
</div>
"""

ENGLISH_DATA = [
    # Theme 1: School Life & Celebrations
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "Country",
        "tts_text": "Country",
        "phonetic": "/ˈkʌntri/ (kant-ri)",
        "word_type": "Noun",
        "type_class": "noun",
        "meaning": "Ülke",
        "sentence": "Students from different <b>countries</b> talk about their cultures.",
        "translation": "Farklı ülkelerden öğrenciler kültürleri hakkında konuşurlar.",
        "tip": "Çoğulu 'countries' şeklinde yazılır (-y düşer, -ies gelir).",
        "image": "cf_en_country.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "Nationality",
        "tts_text": "Nationality",
        "phonetic": "/ˌnæʃəˈnæləti/ (neşeneliti)",
        "word_type": "Noun",
        "type_class": "noun",
        "meaning": "Milliyet, Uyruk",
        "sentence": "What is his <b>nationality</b>? He is South Korean.",
        "translation": "Onun milliyeti nedir? O Güney Korelidir.",
        "tip": "Soru kalıbı: 'What is your nationality?'",
        "image": "cf_en_nationality.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "Language",
        "tts_text": "Language",
        "phonetic": "/ˈlæŋɡwɪdʒ/ (lengvic)",
        "word_type": "Noun",
        "type_class": "noun",
        "meaning": "Dil, Lisan",
        "sentence": "What <b>languages</b> can she speak fluently?",
        "translation": "Hangi dilleri akıcı bir şekilde konuşabiliyor?",
        "tip": "Native language = Ana dil demektir.",
        "image": "cf_en_language.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "Native language",
        "tts_text": "Native language",
        "phonetic": "/ˈneɪtɪv ˈlæŋɡwɪdʒ/ (neytiv lengvic)",
        "word_type": "Noun",
        "type_class": "noun",
        "meaning": "Ana Dil",
        "sentence": "My <b>native language</b> is Turkish, but I also speak English.",
        "translation": "Benim ana dilim Türkçedir ama İngilizce de konuşurum.",
        "tip": "'Mother tongue' ifadesiyle eş anlamlıdır.",
        "image": "cf_en_native_lang.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "Capital city",
        "tts_text": "Capital city",
        "phonetic": "/ˈkæpɪtl ˈsɪti/ (kepitıl siti)",
        "word_type": "Noun",
        "type_class": "noun",
        "meaning": "Başkent",
        "sentence": "The <b>capital</b> of Norway is Oslo.",
        "translation": "Norveç'in başkenti Oslo'dur.",
        "tip": "Kısaca sadece 'capital' olarak da kullanılır.",
        "image": "cf_en_capital_city.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "Where are you from?",
        "tts_text": "Where are you from?",
        "phonetic": "/weər ɑːr juː frɒm/ (ver ar yu from)",
        "word_type": "Question",
        "type_class": "expr",
        "meaning": "Nerelisin?",
        "sentence": "— <b>Where are you from?</b><br>— I am from Türkiye.",
        "translation": "— Nerelisin?<br>— Türkiyeliyim.",
        "tip": "'from' edatı -den/-dan eki katar.",
        "image": "cf_en_where_from.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "South Korea / South Korean",
        "tts_text": "South Korea, South Korean",
        "phonetic": "/saʊθ kəˈriːə/ (sawt koriya)",
        "word_type": "Country / Nat.",
        "type_class": "noun",
        "meaning": "Güney Kore / Güney Koreli",
        "sentence": "Min-ho is from <b>South Korea</b> and he is <b>South Korean</b>.",
        "translation": "Min-ho Güney Kore'dendir ve Güney Korelidir.",
        "tip": "Dili ise 'Korean' (Korece) şeklindedir.",
        "image": "cf_en_south_korea.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "Norway / Norwegian",
        "tts_text": "Norway, Norwegian",
        "phonetic": "/ˈnɔːweɪ / nɔːˈwiːdʒən/ (norvey / norvicın)",
        "word_type": "Country / Nat.",
        "type_class": "noun",
        "meaning": "Norveç / Norveçli, Norveççe",
        "sentence": "Aisha is from <b>Norway</b> and speaks <b>Norwegian</b>.",
        "translation": "Aisha Norveç'tendir ve Norveççe konuşur.",
        "tip": "Başkenti Oslo'dur.",
        "image": "cf_en_norway.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "Chile / Chilean",
        "tts_text": "Chile, Chilean",
        "phonetic": "/ˈtʃɪli / ˈtʃɪliən/ (çili / çiliyın)",
        "word_type": "Country / Nat.",
        "type_class": "noun",
        "meaning": "Şili / Şilili",
        "sentence": "Mateo is from <b>Chile</b> and he speaks Spanish.",
        "translation": "Mateo Şili'dendir ve İspanyolca konuşur.",
        "tip": "Güney Amerika ülkesidir, resmi dili İspanyolcadır.",
        "image": "cf_en_chile.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "Morocco / Moroccan",
        "tts_text": "Morocco, Moroccan",
        "phonetic": "/məˈrɒkəʊ / məˈrɒkən/ (moroko / morokın)",
        "word_type": "Country / Nat.",
        "type_class": "noun",
        "meaning": "Fas / Faslı",
        "sentence": "<b>Moroccan</b> students can speak Arabic and French.",
        "translation": "Faslı öğrenciler Arapça ve Fransızca konuşabilirler.",
        "tip": "Başkenti Rabat'tır.",
        "image": "cf_en_morocco.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "Peru / Peruvian",
        "tts_text": "Peru, Peruvian",
        "phonetic": "/pəˈruː / pəˈruːviən/ (peruu / peruviyın)",
        "word_type": "Country / Nat.",
        "type_class": "noun",
        "meaning": "Peru / Perulu",
        "sentence": "Machu Picchu is a historic city in <b>Peru</b>.",
        "translation": "Machu Picchu, Peru'da tarihi bir şehirdir.",
        "tip": "Başkenti Lima'dır.",
        "image": "cf_en_peru.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: School Life",
        "word": "Speak fluently",
        "tts_text": "Speak fluently",
        "phonetic": "/spiːk ˈfluːəntli/ (spiik fluuntli)",
        "word_type": "Phrase / Verb",
        "type_class": "verb",
        "meaning": "Akıcı bir şekilde konuşmak",
        "sentence": "She can <b>speak English fluently</b>.",
        "translation": "O, İngilizceyi akıcı bir şekilde konuşabiliyor.",
        "tip": "'fluent' (akıcı) sıfatından türemiş zarftır.",
        "image": "cf_en_speak_fluently.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "Tourist attraction",
        "tts_text": "Tourist attraction",
        "phonetic": "/ˈtʊərɪst əˈtrækʃn/ (turist etrekşın)",
        "word_type": "Noun",
        "type_class": "noun",
        "meaning": "Turistik cazibe merkezi / Gezilecek yer",
        "sentence": "Seoul has many famous <b>tourist attractions</b>.",
        "translation": "Seul'un birçok ünlü turistik yeri vardır.",
        "tip": "Turistlerin yoğun ilgi gösterdiği yapılar ve mekanlar.",
        "image": "cf_en_tourist_attraction.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "Historical site",
        "tts_text": "Historical site",
        "phonetic": "/hɪˈstɒrɪkl saɪt/ (historikıl sayt)",
        "word_type": "Noun",
        "type_class": "noun",
        "meaning": "Tarihî alan / Sit alanı",
        "sentence": "Visitors can explore <b>historical sites</b> in Peru.",
        "translation": "Ziyaretçiler Peru'daki tarihî alanları keşfedebilir.",
        "tip": "Site = Alan, mekan, yerleşke demektir.",
        "image": "cf_en_historical_site.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "Ancient",
        "tts_text": "Ancient",
        "phonetic": "/ˈeɪnʃənt/ (eynşınt)",
        "word_type": "Adjective",
        "type_class": "adj",
        "meaning": "Antik, Çok Eski",
        "sentence": "Machu Picchu is an <b>ancient</b> mountain city.",
        "translation": "Machu Picchu antik bir dağ şehridir.",
        "tip": "'Modern' kelimesinin zıt anlamlısıdır.",
        "image": "cf_en_ancient.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "Modern",
        "tts_text": "Modern",
        "phonetic": "/ˈmɒdn/ (modın)",
        "word_type": "Adjective",
        "type_class": "adj",
        "meaning": "Modern, Çağdaş",
        "sentence": "Oslo has <b>modern</b> architecture and quiet parks.",
        "translation": "Oslo modern bir mimariye ve sakin parklara sahiptir.",
        "tip": "Günümüz tasarım ve teknolojisine uygun.",
        "image": "cf_en_modern.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "Fascinating",
        "tts_text": "Fascinating",
        "phonetic": "/ˈfæsɪneɪtɪŋ/ (fesıneytink)",
        "word_type": "Adjective",
        "type_class": "adj",
        "meaning": "Büyüleyici, Hayranlık Uyandırıcı",
        "sentence": "The history of the palace is <b>fascinating</b>.",
        "translation": "Sarayın tarihi büyüleyicidir.",
        "tip": "'Very interesting / attractive' anlamına gelir.",
        "image": "cf_en_fascinating.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "Crowded",
        "tts_text": "Crowded",
        "phonetic": "/ˈkraʊdɪd/ (kravdid)",
        "word_type": "Adjective",
        "type_class": "adj",
        "meaning": "Kalabalık",
        "sentence": "The city center is very <b>crowded</b> during the festival.",
        "translation": "Festival sırasında şehir merkezi çok kalabalıktır.",
        "tip": "Crowd = Kalabalık (isim), Crowded = Kalabalık (sıfat).",
        "image": "cf_en_crowded.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "Peaceful",
        "tts_text": "Peaceful",
        "phonetic": "/ˈpiːsfl/ (piisful)",
        "word_type": "Adjective",
        "type_class": "adj",
        "meaning": "Huzurlu, Sakin",
        "sentence": "The lakeside park is very quiet and <b>peaceful</b>.",
        "translation": "Göl kenarındaki park çok sessiz ve huzurludur.",
        "tip": "Peace = Barış/Huzur, Peaceful = Huzur dolu.",
        "image": "cf_en_peaceful.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "Celebrate",
        "tts_text": "Celebrate",
        "phonetic": "/ˈselɪbreɪt/ (selibreyt)",
        "word_type": "Verb",
        "type_class": "verb",
        "meaning": "Kutlamak",
        "sentence": "People <b>celebrate</b> Republic Day on October 29.",
        "translation": "İnsanlar 29 Ekim'de Cumhuriyet Bayramı'nı kutlarlar.",
        "tip": "Fiil halidir. İsim hali 'celebration'dır.",
        "image": "cf_en_celebrate.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "National day",
        "tts_text": "National day",
        "phonetic": "/ˈnæʃnəl deɪ/ (neşenıl dey)",
        "word_type": "Noun",
        "type_class": "noun",
        "meaning": "Milli Bayram / Ulusal Gün",
        "sentence": "We prepare special ceremonies on <b>national days</b>.",
        "translation": "Milli bayramlarda özel törenler hazırlarız.",
        "tip": "Örn: 29 Ekim Cumhuriyet Bayramı.",
        "image": "cf_en_national_day.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "Gather together",
        "tts_text": "Gather together",
        "phonetic": "/ˈɡæðər təˈɡeðər/ (gedır tugedır)",
        "word_type": "Phrasal Verb",
        "type_class": "verb",
        "meaning": "Bir araya gelmek, Toplanmak",
        "sentence": "Families <b>gather together</b> and have festive meals.",
        "translation": "Aileler bir araya gelir ve bayram yemekleri yerler.",
        "tip": "Together = Birlikte demektir.",
        "image": "cf_en_gather_together.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "Wear traditional clothes",
        "tts_text": "Wear traditional clothes",
        "phonetic": "/weər trəˈdɪʃənl kləʊðz/ (ver tredişınl kloğz)",
        "word_type": "Phrase",
        "type_class": "expr",
        "meaning": "Geleneksel kıyafetler giymek",
        "sentence": "Dancers <b>wear traditional clothes</b> in the parade.",
        "translation": "Dansçılar geçit töreninde geleneksel kıyafetler giyerler.",
        "tip": "Wear = Giymek, Clothes = Kıyafetler.",
        "image": "cf_en_traditional_clothes.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 1: School Life & Celebrations",
        "badge": "Theme 1: Celebrations",
        "word": "Take photos",
        "tts_text": "Take photos",
        "phonetic": "/teɪk ˈfəʊtəʊz/ (teyk fotouz)",
        "word_type": "Phrase / Verb",
        "type_class": "verb",
        "meaning": "Fotoğraf çekmek",
        "sentence": "Tourists <b>take photos</b> of ancient monuments.",
        "translation": "Turistler antik anıtların fotoğraflarını çekerler.",
        "tip": "'take a photo' / 'take pictures' olarak da kullanılır.",
        "image": "cf_en_take_photos.jpg"
    },

    # Theme 2: Classroom Life & Routines
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "Daily routine",
        "tts_text": "Daily routine",
        "phonetic": "/ˈdeɪli ruːˈtiːn/ (deyli ruutiin)",
        "word_type": "Noun",
        "type_class": "noun",
        "meaning": "Günlük Rutin (Her gün yapılan işler)",
        "sentence": "What is your <b>daily routine</b> on weekdays?",
        "translation": "Hafta içi günlerde günlük rutinin nedir?",
        "tip": "Geniş Zaman (Simple Present) ile ifade edilir.",
        "image": "cf_en_daily_routine.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "Wake up / Get up",
        "tts_text": "Wake up, get up",
        "phonetic": "/weɪk ʌp / ɡet ʌp/ (veyk ap / get ap)",
        "word_type": "Phrasal Verb",
        "type_class": "verb",
        "meaning": "Uyanmak / Yataktan kalkmak",
        "sentence": "I <b>wake up</b> early at 6:30 every morning.",
        "translation": "Her sabah 6:30'da erken uyanırım.",
        "tip": "Wake up = Gözünü açmak; Get up = Yataktan kalkmak.",
        "image": "cf_en_wake_up.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "Have breakfast",
        "tts_text": "Have breakfast",
        "phonetic": "/hæv ˈbrekfəst/ (hev brekfıst)",
        "word_type": "Phrase / Verb",
        "type_class": "verb",
        "meaning": "Kahvaltı yapmak",
        "sentence": "We <b>have breakfast</b> before leaving for school.",
        "translation": "Okula gitmeden önce kahvaltı yaparız.",
        "tip": "'eat breakfast' şeklinde de söylenebilir.",
        "image": "cf_en_have_breakfast.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "Take the school bus",
        "tts_text": "Take the school bus",
        "phonetic": "/teɪk ðə skuːl bʌs/ (teyk dı skuul bas)",
        "word_type": "Phrase / Verb",
        "type_class": "verb",
        "meaning": "Okul servisine binmek",
        "sentence": "She <b>takes the school bus</b> at 7:30.",
        "translation": "O, saat 7:30'da okul servisine biner.",
        "tip": "Taşıtlara binmek için 'take' fiili kullanılır.",
        "image": "cf_en_school_bus.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "Classmate",
        "tts_text": "Classmate",
        "phonetic": "/ˈklɑːsmeɪt/ (klaasmeyt)",
        "word_type": "Noun",
        "type_class": "noun",
        "meaning": "Sınıf Arkadaşı",
        "sentence": "My <b>classmates</b> help me with my math homework.",
        "translation": "Sınıf arkadaşlarım matematik ödevimde bana yardım eder.",
        "tip": "Class (sınıf) + mate (arkadaş/eş).",
        "image": "cf_en_classmate.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "Timetable / Schedule",
        "tts_text": "Timetable, schedule",
        "phonetic": "/ˈtaɪmteɪbl / ˈʃedjuːl/ (taymteybl / şecul)",
        "word_type": "Noun",
        "type_class": "noun",
        "meaning": "Ders Programı / Zaman Çizelgesi",
        "sentence": "Let's check our weekly <b>timetable</b> for tomorrow.",
        "translation": "Yarın için haftalık ders programımıza bakalım.",
        "tip": "Ders saatlerini gösteren çizelgedir.",
        "image": "cf_en_timetable.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "Take notes",
        "tts_text": "Take notes",
        "phonetic": "/teɪk nəʊts/ (teyk nouts)",
        "word_type": "Phrase / Verb",
        "type_class": "verb",
        "meaning": "Not almak, Not tutmak",
        "sentence": "I always <b>take notes</b> during the lesson.",
        "translation": "Ders sırasında her zaman not tutarım.",
        "tip": "İyi ders çalışma alışkanlıklarındandır.",
        "image": "cf_en_take_notes.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "Pay attention",
        "tts_text": "Pay attention",
        "phonetic": "/peɪ əˈtenʃn/ (pey etenşın)",
        "word_type": "Phrase / Verb",
        "type_class": "verb",
        "meaning": "Dikkatini vermek, Dikkatle dinlemek",
        "sentence": "<b>Pay attention</b> to the teacher's instructions.",
        "translation": "Öğretmenin yönergelerine dikkat kesilin.",
        "tip": "'pay attention to' kalıbıyla kullanılır.",
        "image": "cf_en_pay_attention.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "Raise hand",
        "tts_text": "Raise hand",
        "phonetic": "/reɪz hænd/ (reyz hend)",
        "word_type": "Phrase / Verb",
        "type_class": "verb",
        "meaning": "Parmak / El kaldırmak",
        "sentence": "Please <b>raise your hand</b> before speaking in class.",
        "translation": "Lütfen sınıfta konuşmadan önce parmak kaldırınız.",
        "tip": "Sınıf içi kurallardandır.",
        "image": "cf_en_raise_hand.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "Chat with friends",
        "tts_text": "Chat with friends",
        "phonetic": "/tʃæt wɪð frendz/ (çet vid frendz)",
        "word_type": "Phrase / Verb",
        "type_class": "verb",
        "meaning": "Arkadaşlar ile sohbet etmek",
        "sentence": "We <b>chat with friends</b> during break time.",
        "translation": "Teneffüste arkadaşlarımızla sohbet ederiz.",
        "tip": "Break time = Teneffüs, ara demektir.",
        "image": "cf_en_chat_friends.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "Always / Usually / Sometimes / Never",
        "tts_text": "Always, usually, sometimes, never",
        "phonetic": "/ˈɔːlweɪz, ˈjuːʒuəli, ˈsʌmtaɪmz, ˈnevər/",
        "word_type": "Frequency Adverbs",
        "type_class": "gram",
        "meaning": "Sıklık Zarfları (Daima / Genellikle / Bazen / Asla)",
        "sentence": "I <b>always</b> review lessons, but I <b>never</b> sleep late.",
        "translation": "Dersleri daima tekrar ederim ama asla geç uyumam.",
        "tip": "%100 (Always) > %80 (Usually) > %50 (Sometimes) > %0 (Never).",
        "image": "cf_en_frequency_adverbs.jpg"
    },
    {
        "subdeck": "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines",
        "badge": "Theme 2: Classroom Life",
        "word": "How often...?",
        "tts_text": "How often do you study?",
        "phonetic": "/haʊ ˈɒfn/ (hav ofın)",
        "word_type": "Question",
        "type_class": "expr",
        "meaning": "Ne sıklıkla...?",
        "sentence": "— <b>How often</b> do you study English?<br>— I study English every day.",
        "translation": "— Ne sıklıkla İngilizce çalışırsın?<br>— Her gün İngilizce çalışırım.",
        "tip": "Cevaplarda sıklık zarfları veya 'every day' kullanılır.",
        "image": "cf_en_how_often.jpg"
    }
]

GERMAN_DATA = [
    # Modul 1: Hallo! (Informationen zur Person)
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Guten Morgen!",
        "tts_text": "Guten Morgen!",
        "phonetic": "[guutın morgın]",
        "word_type": "Greeting",
        "type_class": "expr",
        "meaning": "Günaydın!",
        "sentence": "<b>Guten Morgen!</b> Wie geht es dir heute?",
        "translation": "Günaydın! Bugün nasılsın?",
        "tip": "Sabah 06:00 - 11:00 saatleri arasında kullanılır.",
        "image": "cf_de_guten_morgen.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Guten Tag!",
        "tts_text": "Guten Tag!",
        "phonetic": "[guutın taak]",
        "word_type": "Greeting",
        "type_class": "expr",
        "meaning": "İyi Günler! / Merhaba!",
        "sentence": "<b>Guten Tag</b>, Herr Müller!",
        "translation": "İyi günler Bay Müller!",
        "tip": "Gün boyu (11:00 - 18:00) genel selamlaşmadır.",
        "image": "cf_de_guten_tag.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Guten Abend! / Gute Nacht!",
        "tts_text": "Guten Abend! Gute Nacht!",
        "phonetic": "[guutın aabınt / guute naht]",
        "word_type": "Greeting",
        "type_class": "expr",
        "meaning": "İyi Akşamlar! / İyi Geceler!",
        "sentence": "<b>Guten Abend!</b> — Schlafe gut, <b>Gute Nacht!</b>",
        "translation": "İyi akşamlar! — İyi uyu, iyi geceler!",
        "tip": "Gute Nacht ayrılırken/yatarken söylenir (Nacht dişil olduğu için 'Gute' denir).",
        "image": "cf_de_abend_nacht.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Tschüss! / Auf Wiedersehen!",
        "tts_text": "Tschüss! Auf Wiedersehen!",
        "phonetic": "[çyüs / auf viidır-zeeyın]",
        "word_type": "Farewell",
        "type_class": "expr",
        "meaning": "Hoşça kal! (Samimi) / Görüşmek üzere! (Resmî)",
        "sentence": "Tschüss Ali! — <b>Auf Wiedersehen</b>, Frau Schneider!",
        "translation": "Güle güle Ali! — Görüşmek üzere Bayan Schneider!",
        "tip": "Tschüss arkadaşlar arasında, Auf Wiedersehen büyüklerle/resmî kullanılır.",
        "image": "cf_de_farewell.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Wie heißt du?",
        "tts_text": "Wie heißt du? Ich heiße Mehmet.",
        "phonetic": "[vii hays-tu]",
        "word_type": "Question",
        "type_class": "expr",
        "meaning": "Adın ne?",
        "sentence": "— <b>Wie heißt du?</b><br>— <b>Ich heiße</b> Mehmet.",
        "translation": "— Adın ne?<br>— Benim adım Mehmet.",
        "tip": "heißen fiili adında olmak demektir (ich heiße, du heißt).",
        "image": "cf_de_wie_heisst_du.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Wer bist du? / Mein Name ist...",
        "tts_text": "Wer bist du? Mein Name ist Lukas.",
        "phonetic": "[veer bist du / mayn naame ist]",
        "word_type": "Phrase",
        "type_class": "expr",
        "meaning": "Sen kimsin? / Benim adım ...'dir",
        "sentence": "— <b>Wer bist du?</b><br>— <b>Ich bin</b> Lukas / <b>Mein Name ist</b> Lukas.",
        "translation": "— Sen kimsin?<br>— Ben Lukas'ım / Benim adım Lukas'tır.",
        "tip": "İsim söylemenin 3 yolu: Ich heiße..., Ich bin..., Mein Name ist...",
        "image": "cf_de_wer_bist_du.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Wie geht's? / Wie geht es dir?",
        "tts_text": "Wie geht es dir? Danke, sehr gut!",
        "phonetic": "[vii geets / vii geet es diir]",
        "word_type": "Question",
        "type_class": "expr",
        "meaning": "Nasılsın? / Nasıl gidiyor?",
        "sentence": "— <b>Wie geht es dir?</b><br>— <b>Danke, sehr gut! Und dir?</b>",
        "translation": "— Nasılsın?<br>— Teşekkürler, çok iyi! Ya sen?",
        "tip": "Cevaplar: Sehr gut (Çok iyi), Gut (İyi), Es geht (Fena değil), Schlecht (Kötü).",
        "image": "cf_de_wie_gehts.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Bitte / Danke / Entschuldigung",
        "tts_text": "Bitte schön! Danke schön! Entschuldigung!",
        "phonetic": "[bite / danke / ent-şuldigung]",
        "word_type": "Courtesy",
        "type_class": "expr",
        "meaning": "Lütfen/Rica ederim / Teşekkürler / Özür dilerim",
        "sentence": "<b>Danke schön!</b> — <b>Bitte sehr!</b>",
        "translation": "Çok teşekkürler! — Bir şey değil!",
        "tip": "En temel nezaket sözcükleridir.",
        "image": "cf_de_courtesy.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Personalpronomen (Kişi Zamirleri)",
        "tts_text": "ich, du, er, sie, es, wir, ihr, sie, Sie",
        "phonetic": "[ich, du, er, sie, es, wir, ihr, sie, Sie]",
        "word_type": "Grammar",
        "type_class": "gram",
        "meaning": "Ben, Sen, O (Erkek/Kadın/Nötr), Biz, Sizler, Onlar, Siz (Nezaket)",
        "sentence": "<b>ich</b> (ben), <b>du</b> (sen), <b>er/sie/es</b> (o), <b>wir</b> (biz), <b>ihr</b> (sizler), <b>Sie</b> (kibar siz).",
        "translation": "Kişi zamirleri fiil çekiminin temelidir.",
        "tip": "Büyük harfle yazılan 'Sie' her zaman kibar/resmî 'Siz' anlamındadır.",
        "image": "cf_de_pronomen.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "ESTTEN Kuralı (Düzenli Fiil Çekimi)",
        "tts_text": "ich lerne, du lernst, er lernt, wir lernen, ihr lernt, sie lernen",
        "phonetic": "[-e, -st, -t, -en, -t, -en]",
        "word_type": "Grammar Rule",
        "type_class": "gram",
        "meaning": "Düzenli fiil köküne gelen şahıs ekleri kuralı",
        "sentence": "lernen (öğrenmek):<br>ich lern<b>e</b>, du lern<b>st</b>, er lern<b>t</b>, wir lern<b>en</b>, ihr lern<b>t</b>, sie lern<b>en</b>.",
        "translation": "Tüm düzenli fiiller bu kalıpla çekimlenir.",
        "tip": "Hafıza kodu: E - ST - T - EN - T - EN (ESTTEN).",
        "image": "cf_de_estten.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "sein (Olmak Fiili)",
        "tts_text": "ich bin, du bist, er ist, wir sind, ihr seid, sie sind",
        "phonetic": "[ich bin, du bist, er ist, wir sind, ihr seid, sie sind]",
        "word_type": "Irregular Verb",
        "type_class": "verb",
        "meaning": "Olmak (İngilizcedeki 'To be')",
        "sentence": "<b>Ich bin</b> Schüler. <b>Du bist</b> mein Freund. <b>Er ist</b> 14 Jahre alt.",
        "translation": "Ben öğrenciyim. Sen benim arkadaşımsın. O 14 yaşındadır.",
        "tip": "Düzensizdir, ezberlenmesi zorunludur.",
        "image": "cf_de_verb_sein.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Zahlen 0 - 10 (Sayılar 0-10)",
        "tts_text": "null, eins, zwei, drei, vier, fünf, sechs, sieben, acht, neun, zehn",
        "phonetic": "[null, ayns, tsvay, dray, fiyır, fünf, zeks, ziibın, aht, noyn, tseen]",
        "word_type": "Numbers",
        "type_class": "noun",
        "meaning": "null (0), eins (1), zwei (2), drei (3), vier (4), fünf (5), sechs (6), sieben (7), acht (8), neun (9), zehn (10)",
        "sentence": "Eins, zwei, drei... ich kann bis zehn zählen!",
        "translation": "Bir, iki, üç... ona kadar sayabiliyorum!",
        "tip": "z harfi 'ts' (sert) okunur: zwei [tsvay], zehn [tseen].",
        "image": "cf_de_zahlen_0_10.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Zahlen 11 - 20 (Sayılar 11-20)",
        "tts_text": "elf, zwölf, dreizehn, vierzehn, fünfzehn, sechzehn, siebzehn, achtzehn, neunzehn, zwanzig",
        "phonetic": "[elf, tsvölf, draytseen... zvantzih]",
        "word_type": "Numbers",
        "type_class": "noun",
        "meaning": "elf (11), zwölf (12), dreizehn (13), vierzehn (14), fünfzehn (15), sechzehn (16⚠️), siebzehn (17⚠️), achtzehn (18), neunzehn (19), zwanzig (20)",
        "sentence": "Ich habe <b>fünfzehn</b> Bücher.",
        "translation": "Benim on beş kitabım var.",
        "tip": "16 = sechzehn ('s' düşer!), 17 = siebzehn ('en' düşer!).",
        "image": "cf_de_zahlen_11_20.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Wie alt bist du?",
        "tts_text": "Wie alt bist du? Ich bin vierzehn Jahre alt.",
        "phonetic": "[vii alt bist du]",
        "word_type": "Question",
        "type_class": "expr",
        "meaning": "Kaç yaşındasın?",
        "sentence": "— <b>Wie alt bist du?</b><br>— <b>Ich bin 14 (vierzehn) Jahre alt.</b>",
        "translation": "— Kaç yaşındasın?<br>— 14 yaşındayım.",
        "tip": "Jahre alt = Yaşında demektir.",
        "image": "cf_de_wie_alt.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Wie ist deine Telefonnummer?",
        "tts_text": "Wie ist deine Handynummer? Meine Handynummer ist null, eins, sieben, sechs.",
        "phonetic": "[vii ist dayne telefonnumır]",
        "word_type": "Question",
        "type_class": "expr",
        "meaning": "Telefon numaran nedir?",
        "sentence": "— <b>Wie ist deine Handynummer?</b><br>— <b>Meine Handynummer ist 0176...</b>",
        "translation": "— Cep numaran nedir?<br>— Cep numaram 0176...",
        "tip": "Numaralar tek tek Almanca sayılarla söylenir.",
        "image": "cf_de_telefonnummer.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Woher kommst du?",
        "tts_text": "Woher kommst du? Ich komme aus der Türkei.",
        "phonetic": "[vo-heer komst du]",
        "word_type": "Question",
        "type_class": "expr",
        "meaning": "Nereden geliyorsun? / Nerelisin?",
        "sentence": "— <b>Woher kommst du?</b><br>— <b>Ich komme aus der Türkei</b> / <b>aus Deutschland</b>.",
        "translation": "— Nerelisin?<br>— Türkiye'denim / Almanya'danım.",
        "tip": "'aus' edatı -den/-dan anlamı katar.",
        "image": "cf_de_woher_kommst_du.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "die Türkei / die Schweiz (Artikelli Ülkeler)",
        "tts_text": "Ich komme aus der Türkei. Ich komme aus der Schweiz.",
        "phonetic": "[aus der türkay / aus der şvayts]",
        "word_type": "Grammar Rule",
        "type_class": "gram",
        "meaning": "Türkiye ve İsviçre artikelli olduğu için 'aus der ...' şeklinde kullanılır!",
        "sentence": "✅ Ich komme <b>aus der Türkei</b>.<br>❌ Ich komme aus Türkei (YANLIŞ).",
        "translation": "Türkiye'den geliyorum.",
        "tip": "Deutschland ve England artikelsizdir: 'aus Deutschland'.",
        "image": "cf_de_aus_der_tuerkei.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Deutschland / Deutsch",
        "tts_text": "Deutschland, Deutsch. Lukas kommt aus Deutschland und spricht Deutsch.",
        "phonetic": "[doyçlant / doyç]",
        "word_type": "Country / Lang.",
        "type_class": "noun",
        "meaning": "Almanya / Almanca",
        "sentence": "Lukas kommt aus <b>Deutschland</b> und spricht <b>Deutsch</b>.",
        "translation": "Lukas Almanya'dandır ve Almanca konuşur.",
        "tip": "Başkenti Berlin'dir.",
        "image": "cf_de_deutschland_deutsch.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Wo practical/Wohnort: Wo wohnst du?",
        "tts_text": "Wo wohnst du? Ich wohne in Berlin.",
        "phonetic": "[vo voonst du]",
        "word_type": "Question",
        "type_class": "expr",
        "meaning": "Nerede oturuyorsun / ikamet ediyorsun?",
        "sentence": "— <b>Wo wohnst du?</b><br>— <b>Ich wohne in Ankara / in Berlin.</b>",
        "translation": "— Nerede oturuyorsun?<br>— Ankara'da / Berlin'de oturuyorum.",
        "tip": "'wohnen' oturmak fiilidir, şehirlerin önüne 'in' gelir.",
        "image": "cf_de_wo_wohnst_du.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "Welche Sprachen sprichst du?",
        "tts_text": "Welche Sprachen sprichst du? Ich spreche Türkisch, Englisch und ein bisschen Deutsch.",
        "phonetic": "[velhe şpraahın şprihst du]",
        "word_type": "Question",
        "type_class": "expr",
        "meaning": "Hangi dilleri konuşuyorsun?",
        "sentence": "<b>Ich spreche Türkisch, Englisch und ein bisschen Deutsch.</b>",
        "translation": "Türkçe, İngilizce ve biraz Almanca konuşuyorum.",
        "tip": "sprechen fiili düzensizdir (ich spreche, du sprichst, er spricht).",
        "image": "cf_de_welche_sprachen.jpg"
    },
    {
        "subdeck": "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)",
        "badge": "Modul 1: Hallo!",
        "word": "W-Fragen (Soru Kelimeleri)",
        "tts_text": "Wer, Wie, Woher, Wo, Was, Welche",
        "phonetic": "[Wer, Wie, Woher, Wo, Was, Welche]",
        "word_type": "Grammar",
        "type_class": "gram",
        "meaning": "Almanca Soru Sözcükleri (Kim, Nasıl, Nereden, Nerede, Ne, Hangi)",
        "sentence": "<b>Wer</b> (Kim?), <b>Wie</b> (Nasıl?), <b>Woher</b> (Nereden?), <b>Wo</b> (Nerede?), <b>Was</b> (Ne?), <b>Welche</b> (Hangi?).",
        "translation": "Tüm bilgi soruları W harfiyle başlar.",
        "tip": "Cümlede her zaman 1. sıraya gelir, hemen ardından fiil gelir.",
        "image": "cf_de_w_fragen.jpg"
    }
]

def sanitize_filename(text):
    clean = re.sub(r'[^a-zA-Z0-9_-]', '_', text.lower())
    clean = re.sub(r'_+', '_', clean).strip('_')
    return clean[:32]

async def generate_audio(text, voice, out_path):
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100:
        return
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_path)

def update_apkg_dconf(apkg_path, new_limit=15):
    tmpdir = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(apkg_path, 'r') as z:
            z.extractall(tmpdir)
        db_path = os.path.join(tmpdir, 'collection.anki2')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT dconf FROM col')
        dconf = json.loads(cur.fetchone()[0])
        for k in dconf:
            dconf[k]['new']['perDay'] = new_limit
            dconf[k]['autoplay'] = True
            dconf[k]['replayq'] = True
        cur.execute('UPDATE col SET dconf = ?', (json.dumps(dconf),))
        conn.commit()
        conn.close()
        
        tmp_zip = apkg_path + '.tmp'
        with zipfile.ZipFile(tmp_zip, 'w', zipfile.ZIP_DEFLATED) as z_out:
            for root, dirs, files in os.walk(tmpdir):
                for f in files:
                    full_p = os.path.join(root, f)
                    rel_p = os.path.relpath(full_p, tmpdir)
                    z_out.write(full_p, rel_p)
        shutil.move(tmp_zip, apkg_path)
    finally:
        shutil.rmtree(tmpdir)

async def build_all():
    media_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "anki_decks", "media"))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "anki_decks"))
    os.makedirs(media_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    print("🎙️ Ses ve Görseller Derleniyor...")
    
    # 1. Ses Dosyaları
    en_media_files = []
    from PIL import Image

    def compress_img(p):
        try:
            im = Image.open(p)
            im = im.convert('RGB')
            im.thumbnail((512, 512), Image.Resampling.LANCZOS)
            im.save(p, format='JPEG', quality=75, optimize=True)
        except Exception as e:
            pass

    for idx, item in enumerate(ENGLISH_DATA):
        slug = sanitize_filename(item["word"])
        fname = f"en_{idx+1:02d}_{slug}.mp3"
        fpath = os.path.join(media_dir, fname)
        await generate_audio(item["tts_text"], VOICE_EN, fpath)
        item["audio_fname"] = fname
        item["audio_tag"] = f"[sound:{fname}]"
        en_media_files.append(fpath)
        img_path = os.path.join(media_dir, item["image"])
        # Use full img HTML in field so AnkiDroid scans it for media
        item["image_tag"] = f'<img src="{item["image"]}" class="vd-img">'
        if os.path.exists(img_path):
            compress_img(img_path)
            if img_path not in en_media_files:
                en_media_files.append(img_path)

    de_media_files = []
    for idx, item in enumerate(GERMAN_DATA):
        slug = sanitize_filename(item["word"])
        fname = f"de_{idx+1:02d}_{slug}.mp3"
        fpath = os.path.join(media_dir, fname)
        await generate_audio(item["tts_text"], VOICE_DE, fpath)
        item["audio_fname"] = fname
        item["audio_tag"] = f"[sound:{fname}]"
        de_media_files.append(fpath)
        img_path = os.path.join(media_dir, item["image"])
        # Use full img HTML in field so AnkiDroid scans it for media
        item["image_tag"] = f'<img src="{item["image"]}" class="vd-img">'
        if os.path.exists(img_path):
            compress_img(img_path)
            if img_path not in de_media_files:
                de_media_files.append(img_path)


    sfx_path = os.path.join(media_dir, "sfx_chime.mp3")
    if os.path.exists(sfx_path):
        if sfx_path not in en_media_files:
            en_media_files.append(sfx_path)
        if sfx_path not in de_media_files:
            de_media_files.append(sfx_path)

    # 2. Şablonlar & CSS
    skill_dir = os.path.expanduser("~/.agents/skills/study-forge/templates")
    with open(os.path.join(skill_dir, "card_styles.css"), "r", encoding="utf-8") as f:
        card_css = f.read()
    with open(os.path.join(skill_dir, "front_template.html"), "r", encoding="utf-8") as f:
        front_html = f.read()
    with open(os.path.join(skill_dir, "back_template.html"), "r", encoding="utf-8") as f:
        back_html = f.read()

    en_model = genanki.Model(
        1892019311,
        '9. Sınıf İngilizce Görsel Sözlük v5',
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
                'name': 'İngilizce Kart',
                'qfmt': front_html,
                'afmt': back_html,
            }
        ],
        css=card_css
    )

    en_main_deck = genanki.Deck(1938472910, "9. Sınıf İngilizce")
    en_subdecks = {
        "9. Sınıf İngilizce::Theme 1: School Life & Celebrations": genanki.Deck(1938472911, "9. Sınıf İngilizce::Theme 1: School Life & Celebrations"),
        "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines": genanki.Deck(1938472912, "9. Sınıf İngilizce::Theme 2: Classroom Life & Routines"),
    }

    for item in ENGLISH_DATA:
        sname = item["subdeck"]
        badge_name = item.get("badge", sname.split("::")[-1])
        guid_val = hashlib.sha256(f"english_9_{item['word']}".encode('utf-8')).hexdigest()[:10]
        # Sequential audio tag: chime + speech
        audio_val = f"[sound:sfx_chime.mp3][sound:{item['audio_fname']}]"
        note = genanki.Note(
            model=en_model,
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
                audio_val
            ],
            guid=guid_val
        )
        en_subdecks[sname].add_note(note)

    en_apkg_path = os.path.join(output_dir, "9_sinif_ingilizce_1_ay.apkg")
    en_package = CleanPackage([en_main_deck] + list(en_subdecks.values()), media_files=en_media_files, daily_limit=15)
    en_package.write_to_file(en_apkg_path)
    print(f"✅ İngilizce Görsel Sözlüklü APKG üretildi: {en_apkg_path} (Medya: {len(en_media_files)} dosya)")

    # 3. Almanca Modeli ve Paketi
    de_model = genanki.Model(
        2026091731,
        '9. Sınıf Almanca Görsel Sözlük',
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
                'name': 'Almanca Kart',
                'qfmt': front_html,
                'afmt': back_html,
            }
        ],
        css=card_css
    )

    de_main_deck = genanki.Deck(2026091730, "9. Sınıf Almanca")
    de_subdecks = {
        "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)": genanki.Deck(2026091732, "9. Sınıf Almanca::Modul 1: Hallo! (Informationen zur Person)"),
    }

    for item in GERMAN_DATA:
        sname = item["subdeck"]
        badge_name = item.get("badge", sname.split("::")[-1])
        guid_val = hashlib.sha256(f"german_9_{item['word']}".encode('utf-8')).hexdigest()[:10]
        audio_val = f"[sound:sfx_chime.mp3][sound:{item['audio_fname']}]"
        note = genanki.Note(
            model=de_model,
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
                audio_val
            ],
            guid=guid_val
        )
        de_subdecks[sname].add_note(note)

    de_apkg_path = os.path.join(output_dir, "9_sinif_almanca_1_ay.apkg")
    de_package = CleanPackage([de_main_deck] + list(de_subdecks.values()), media_files=de_media_files, daily_limit=15)
    de_package.write_to_file(de_apkg_path)
    print(f"✅ Almanca Görsel Sözlüklü APKG üretildi: {de_apkg_path} (Medya: {len(de_media_files)} dosya)")

if __name__ == "__main__":
    asyncio.run(build_all())
