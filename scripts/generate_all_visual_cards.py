#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Görsel Sözlük (Visual Dictionary) Kart Görselleri Üretici
- Gerçek görsel sözlük illüstrasyonları, kırpılmış sahneler ve yüksek çözünürlüklü tematik kartlar
"""

import os
from PIL import Image, ImageDraw, ImageFont

media_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "anki_decks", "media"))
os.makedirs(media_dir, exist_ok=True)

def create_vd_card(filename, title, subtitle, bg_color, accent_color, icon_draw_fn):
    W, H = 600, 420
    img = Image.new("RGB", (W, H), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Outer Card Border & Inner Frame
    draw.rounded_rectangle([15, 15, W-15, H-15], radius=24, outline=accent_color, width=4)
    draw.rounded_rectangle([25, 25, W-25, 75], radius=14, fill=accent_color)
    
    # Header Title
    draw.text((W//2, 50), title.upper(), fill="#ffffff", anchor="mm")
    
    # Custom Center Illustration
    icon_draw_fn(draw, W, H, accent_color)
    
    # Footer Subtitle Pill
    draw.rounded_rectangle([W//2 - 180, H-60, W//2 + 180, H-25], radius=12, fill="#ffffff", outline=accent_color, width=2)
    draw.text((W//2, H-42), subtitle, fill=accent_color, anchor="mm")
    
    out_path = os.path.join(media_dir, filename)
    img.save(out_path, quality=95)
    return out_path

# 1. German Greetings (Guten Morgen, Tag, Abend, Nacht)
def draw_guten_morgen(draw, W, H, acc):
    # Sun rising over green hills
    draw.pieslice([W//2 - 60, 110, W//2 + 60, 230], 180, 360, fill="#f59e0b", outline="#d97706", width=3)
    # Sun rays
    for angle in [200, 230, 270, 310, 340]:
        import math
        rad = math.radians(angle)
        x1 = W//2 + int(65 * math.cos(rad))
        y1 = 170 + int(65 * math.sin(rad))
        x2 = W//2 + int(90 * math.cos(rad))
        y2 = 170 + int(90 * math.sin(rad))
        draw.line([x1, y1, x2, y2], fill="#f59e0b", width=4)
    # Hills & Alarm Clock
    draw.chord([W//2 - 160, 210, W//2 + 160, 390], 180, 360, fill="#10b981")
    draw.rounded_rectangle([W//2 - 40, 240, W//2 + 40, 310], radius=10, fill="#ffffff", outline="#1e293b", width=3)
    draw.text((W//2, 275), "07:00", fill="#0f172a", anchor="mm")

create_vd_card("vd_de_guten_morgen.jpg", "GUTEN MORGEN! ☀️", "06:00 - 11:00 • Günaydın!", "#fffbeb", "#d97706", draw_guten_morgen)

def draw_guten_tag(draw, W, H, acc):
    # Bright midday sun & school building
    draw.ellipse([W//2 - 50, 100, W//2 + 50, 200], fill="#eab308", outline="#ca8a04", width=4)
    draw.rounded_rectangle([W//2 - 120, 210, W//2 + 120, 320], radius=8, fill="#ffffff", outline="#3b82f6", width=3)
    draw.polygon([(W//2 - 130, 210), (W//2, 160), (W//2 + 130, 210)], fill="#ef4444")
    draw.text((W//2, 260), "SCHULE / GÜN BOYU", fill="#1e3a8a", anchor="mm")

create_vd_card("vd_de_guten_tag.jpg", "GUTEN TAG! 🌤️", "11:00 - 18:00 • İyi Günler / Merhaba!", "#eff6ff", "#2563eb", draw_guten_tag)

def draw_guten_abend_nacht(draw, W, H, acc):
    # Moon and stars
    draw.ellipse([W//2 - 80, 110, W//2 + 10, 200], fill="#fde047")
    draw.ellipse([W//2 - 60, 105, W//2 + 20, 185], fill="#0f172a") # Crescent shadow
    # Bed / Sleep
    draw.rounded_rectangle([W//2 - 100, 220, W//2 + 100, 300], radius=12, fill="#1e293b", outline="#38bdf8", width=3)
    draw.text((W//2, 260), "GUTE NACHT (Schlafen 🌙)", fill="#38bdf8", anchor="mm")

create_vd_card("vd_de_abend_nacht.jpg", "GUTEN ABEND & GUTE NACHT 🌙", "Akşam & Gece / İyi Uykular!", "#0f172a", "#38bdf8", draw_guten_abend_nacht)

def draw_tschuss_aufwiedersehen(draw, W, H, acc):
    # Waving hands and speech bubbles
    draw.rounded_rectangle([W//2 - 140, 110, W//2 - 10, 210], radius=16, fill="#ecfdf5", outline="#059669", width=3)
    draw.text((W//2 - 75, 160), "Tschüss!\n(Freunde)", fill="#059669", anchor="mm")
    draw.rounded_rectangle([W//2 + 10, 110, W//2 + 140, 210], radius=16, fill="#eff6ff", outline="#2563eb", width=3)
    draw.text((W//2 + 75, 160), "Auf\nWiedersehen!", fill="#2563eb", anchor="mm")
    draw.text((W//2, 270), "👋 GÖRÜŞMEK ÜZERE 👋", fill="#1e293b", anchor="mm")

create_vd_card("vd_de_farewell.jpg", "TSCHÜSS & AUF WIEDERSEHEN 👋", "Samimi & Resmî Vedalaşma", "#f0fdf4", "#059669", draw_tschuss_aufwiedersehen)

def draw_de_numbers_0_10(draw, W, H, acc):
    # Colorful number badges
    nums = ["0 null", "1 eins", "2 zwei", "3 drei", "4 vier", "5 fünf", "6 sechs", "7 sieben", "8 acht", "9 neun", "10 zehn"]
    for i, num in enumerate(nums[:6]):
        x = 50 + i * 85
        draw.rounded_rectangle([x, 110, x + 75, 180], radius=10, fill="#dbeafe", outline="#2563eb", width=2)
        draw.text((x + 37, 145), num, fill="#1e40af", anchor="mm")
    for i, num in enumerate(nums[6:]):
        x = 90 + i * 85
        draw.rounded_rectangle([x, 200, x + 75, 270], radius=10, fill="#fef3c7", outline="#d97706", width=2)
        draw.text((x + 37, 235), num, fill="#b45309", anchor="mm")

create_vd_card("vd_de_numbers_0_10.jpg", "DIE ZAHLEN 0 - 10 🔢", "Almanca Sayılar (0-10)", "#f8fafc", "#2563eb", draw_de_numbers_0_10)

def draw_de_numbers_11_20(draw, W, H, acc):
    nums = ["11 elf", "12 zwölf", "13 dreizehn", "14 vierzehn", "15 fünfzehn", "16 sechzehn ⚠️", "17 siebzehn ⚠️", "18 achtzehn", "19 neunzehn", "20 zwanzig"]
    for i, num in enumerate(nums[:5]):
        x = 55 + i * 100
        draw.rounded_rectangle([x, 110, x + 90, 180], radius=10, fill="#e0f2fe", outline="#0284c7", width=2)
        draw.text((x + 45, 145), num, fill="#0369a1", anchor="mm")
    for i, num in enumerate(nums[5:]):
        x = 55 + i * 100
        draw.rounded_rectangle([x, 200, x + 90, 270], radius=10, fill="#fee2e2", outline="#dc2626", width=2)
        draw.text((x + 45, 235), num, fill="#b91c1c", anchor="mm")

create_vd_card("vd_de_numbers_11_20.jpg", "DIE ZAHLEN 11 - 20 🔢", "16: sechzehn (s yok) • 17: siebzehn (en yok)", "#fef2f2", "#dc2626", draw_de_numbers_11_20)

def draw_de_countries(draw, W, H, acc):
    # Flags & Country Badges
    items = [
        ("🇩🇪 Deutschland", "Deutsch", "#0f172a"),
        ("🇹🇷 die Türkei ⚠️", "Türkisch (aus der...)", "#dc2626"),
        ("🇦🇹 Österreich", "Deutsch", "#ef4444"),
        ("🇨🇭 die Schweiz ⚠️", "Deutsch / Franz. (aus der...)", "#b91c1c")
    ]
    for i, (cntry, lang, col) in enumerate(items):
        x = 60 if i % 2 == 0 else 320
        y = 105 if i < 2 else 205
        draw.rounded_rectangle([x, y, x + 220, y + 80], radius=12, fill="#ffffff", outline=col, width=3)
        draw.text((x + 110, y + 28), cntry, fill=col, anchor="mm")
        draw.text((x + 110, y + 55), lang, fill="#64748b", anchor="mm")

create_vd_card("vd_de_countries_flags.jpg", "LÄNDER UND SPRACHEN 🌍", "Ülkeler, Diller ve Artikelli Ülkeler Kuralı", "#f8fafc", "#0f172a", draw_de_countries)

def draw_de_grammar_estten(draw, W, H, acc):
    rules = [
        ("ich", "-e", "lerne / wohne"),
        ("du", "-st", "lernst / wohnst"),
        ("er/sie/es", "-t", "lernt / wohnt"),
        ("wir", "-en", "lernen / wohnen"),
        ("ihr", "-t", "lernt / wohnt"),
        ("sie/Sie", "-en", "lernen / wohnen")
    ]
    for i, (pers, ending, ex) in enumerate(rules):
        x = 50 + (i % 3) * 170
        y = 110 if i < 3 else 205
        draw.rounded_rectangle([x, y, x + 155, y + 75], radius=10, fill="#fdf2f8", outline="#db2777", width=2)
        draw.text((x + 77, y + 22), f"{pers} ➔ {ending}", fill="#be185d", anchor="mm")
        draw.text((x + 77, y + 50), ex, fill="#475569", anchor="mm")

create_vd_card("vd_de_grammar_estten.jpg", "ESTTEN KURALI (Düzenli Fiil Çekimi) ✍️", "E - ST - T - EN - T - EN Kuralı", "#fdf2f8", "#db2777", draw_de_grammar_estten)

def draw_de_sein(draw, W, H, acc):
    seins = [
        ("ich bin", "Ben ...yim"),
        ("du bist", "Sen ...sin"),
        ("er/sie/es ist", "O ...dir"),
        ("wir sind", "Biz ...yiz"),
        ("ihr seid", "Sizler ...siniz"),
        ("sie/Sie sind", "Onlar / Sizsiniz")
    ]
    for i, (de, tr) in enumerate(seins):
        x = 50 + (i % 3) * 170
        y = 110 if i < 3 else 205
        draw.rounded_rectangle([x, y, x + 155, y + 75], radius=10, fill="#f0fdf4", outline="#16a34a", width=2)
        draw.text((x + 77, y + 25), de, fill="#15803d", anchor="mm")
        draw.text((x + 77, y + 52), tr, fill="#64748b", anchor="mm")

create_vd_card("vd_de_verb_sein.jpg", "SEIN (Olmak Fiili) 🌟", "Düzensiz Olmak Fiili Çekimi", "#f0fdf4", "#16a34a", draw_de_sein)

def draw_de_w_fragen(draw, W, H, acc):
    questions = [
        ("Wer?", "Kim?"),
        ("Wie?", "Nasıl? / Ne?"),
        ("Woher?", "Nereden?"),
        ("Wo?", "Nerede?"),
        ("Was?", "Ne?"),
        ("Welche?", "Hangi?")
    ]
    for i, (q, tr) in enumerate(questions):
        x = 50 + (i % 3) * 170
        y = 110 if i < 3 else 205
        draw.rounded_rectangle([x, y, x + 155, y + 75], radius=10, fill="#ede9fe", outline="#7c3aed", width=2)
        draw.text((x + 77, y + 25), q, fill="#6d28d9", anchor="mm")
        draw.text((x + 77, y + 52), tr, fill="#475569", anchor="mm")

create_vd_card("vd_de_w_fragen.jpg", "W-FRAGEN (Soru Kelimeleri) ❓", "Almanca W ile Başlayan Soru Sözcükleri", "#ede9fe", "#7c3aed", draw_de_w_fragen)

def draw_en_frequency(draw, W, H, acc):
    bars = [
        ("Always (%100)", "#10b981", 420),
        ("Usually (%80)", "#3b82f6", 340),
        ("Often (%60)", "#8b5cf6", 260),
        ("Sometimes (%50)", "#f59e0b", 210),
        ("Never (%0)", "#ef4444", 60)
    ]
    for i, (lbl, col, bar_w) in enumerate(bars):
        y = 105 + i * 36
        draw.text((50, y + 10), lbl, fill="#1e293b", anchor="lm")
        draw.rounded_rectangle([200, y, 200 + bar_w, y + 20], radius=6, fill=col)

create_vd_card("vd_en_frequency_adverbs.jpg", "FREQUENCY ADVERBS (Sıklık Zarfları) 📊", "Always > Usually > Often > Sometimes > Never", "#f8fafc", "#10b981", draw_en_frequency)

def draw_en_notes_habits(draw, W, H, acc):
    habits = [
        ("✍️ Take Notes", "Ders boyu not almak"),
        ("🙋 Raise Hand", "Söz isteyip parmak kaldırmak"),
        ("👂 Pay Attention", "Öğretmeni dikkatle dinlemek"),
        ("💬 Chat with Friends", "Teneffüste arkadaşlarla sohbet")
    ]
    for i, (act, desc) in enumerate(habits):
        x = 55 if i % 2 == 0 else 315
        y = 110 if i < 2 else 205
        draw.rounded_rectangle([x, y, x + 230, y + 75], radius=10, fill="#ffffff", outline="#0284c7", width=2)
        draw.text((x + 115, y + 24), act, fill="#0369a1", anchor="mm")
        draw.text((x + 115, y + 50), desc, fill="#64748b", anchor="mm")

create_vd_card("vd_en_classroom_habits.jpg", "CLASSROOM HABITS & INTERACTIONS 🏫", "Sınıf İçi Alışkanlıklar ve Kurallar", "#f0f9ff", "#0284c7", draw_en_notes_habits)

print("All dedicated Visual Dictionary graphic cards created successfully!")
