#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cloudflare Workers AI FLUX-2-Klein-4B Toplu Görsel Üretici
- Model: @cf/black-forest-labs/flux-2-klein-4b (multipart/form-data)
- 57 kelime için görsel sözlük kartı illüstrasyonları üretir
"""

import os
import sys
import json
import time
import subprocess
import base64

CF_TOKEN = os.environ.get("CLOUDFLARE_API_TOKEN", "")
CF_ACCOUNT_ID = os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")
MODEL = "@cf/black-forest-labs/flux-2-klein-4b"
FALLBACK_MODEL = "@cf/bytedance/stable-diffusion-xl-lightning"

PROMPTS = {
    "cf_en_country.jpg": "Vector art visual dictionary illustration of a colorful globe with international flags of different countries, educational flashcard style, clean white background, vibrant colors",
    "cf_en_nationality.jpg": "Vector art visual dictionary illustration of diverse multi-ethnic high school teenagers smiling together representing different nationalities, passport stamps, clean modern educational style",
    "cf_en_language.jpg": "Vector art visual dictionary illustration of speech bubbles containing different language greetings Hello Bonjour Hola Merhaba, communication concept, clean white background",
    "cf_en_native_lang.jpg": "Vector art visual dictionary illustration of a person speaking with mother tongue symbols, speech bubble, fluent language icon, educational flashcard",
    "cf_en_capital_city.jpg": "Vector art visual dictionary illustration of modern capital city skyline, landmark buildings, government palace, scenic travel illustration",
    "cf_en_where_from.jpg": "Vector art visual dictionary illustration of world map with location pin markers and luggage suitcase, Where are you from travel concept",
    "cf_en_south_korea.jpg": "Vector art visual dictionary illustration of South Korea Seoul N Seoul Tower, Hanbok traditional costume, Korean flag Taegeukgi, beautiful travel poster",
    "cf_en_norway.jpg": "Vector art visual dictionary illustration of Norway picturesque fjord, red wooden cabins, snowy mountains, northern lights, Norwegian flag",
    "cf_en_chile.jpg": "Vector art visual dictionary illustration of Chile Andes mountains, Moai statue Easter Island, Chilean flag, scenic landscape",
    "cf_en_morocco.jpg": "Vector art visual dictionary illustration of Morocco Marrakech historic Medina archway, colorful mosaic tiles, Sahara desert camel, Moroccan flag",
    "cf_en_peru.jpg": "Vector art visual dictionary illustration of Peru Machu Picchu ancient Inca citadel, llama in mountains, Peruvian flag",
    "cf_en_speak_fluently.jpg": "Vector art visual dictionary illustration of fluent public speaker confident on stage, sound waves and flying words, communication skill",
    "cf_en_tourist_attraction.jpg": "Vector art visual dictionary illustration of famous global tourist landmarks Eiffel Tower, Pyramids, Big Ben, Taj Mahal together, travel collage",
    "cf_en_historical_site.jpg": "Vector art visual dictionary illustration of ancient Roman amphitheater Colosseum ruins, archaeological historical site, sunny day",
    "cf_en_ancient.jpg": "Vector art visual dictionary illustration of ancient Egyptian pyramids and Sphinx in golden desert sands under sunny sky",
    "cf_en_modern.jpg": "Vector art visual dictionary illustration of futuristic modern smart city with glass skyscrapers, green rooftop gardens, clean architecture",
    "cf_en_fascinating.jpg": "Vector art visual dictionary illustration of an enchanted glowing ancient palace at twilight with sparkling stars, fascinating magical atmosphere",
    "cf_en_crowded.jpg": "Vector art visual dictionary illustration of a bustling crowded city street festival, happy people celebrating with confetti and balloons",
    "cf_en_peaceful.jpg": "Vector art visual dictionary illustration of a peaceful serene mountain lake with pine trees, reflection on calm water, peaceful nature",
    "cf_en_celebrate.jpg": "Vector art visual dictionary illustration of festive holiday celebration with colorful confetti, fireworks, bunting flags, cheering students",
    "cf_en_national_day.jpg": "Vector art visual dictionary illustration of national day parade celebration with waving national flags, military marching band, fireworks",
    "cf_en_gather_together.jpg": "Vector art visual dictionary illustration of happy family and friends gathering together around a banquet dinner table celebrating",
    "cf_en_traditional_clothes.jpg": "Vector art visual dictionary illustration of folklore dancers wearing ornate authentic traditional folk costumes, colorful embroidered vest",
    "cf_en_take_photos.jpg": "Vector art visual dictionary illustration of a tourist girl holding vintage camera taking photographs of scenic monument, flash sparkle",
    "cf_en_daily_routine.jpg": "Vector art visual dictionary illustration of daily routine circular infographic icons: alarm clock, breakfast, school bus, studying, sleeping",
    "cf_en_wake_up.jpg": "Vector art visual dictionary illustration of a teenage student waking up in cozy bedroom, stretching arms with morning sunshine through window, ringing alarm clock",
    "cf_en_have_breakfast.jpg": "Vector art visual dictionary illustration of healthy delicious morning breakfast: boiled eggs, toast, orange juice, tea, honey and cheese on wooden table",
    "cf_en_school_bus.jpg": "Vector art visual dictionary illustration of a bright yellow school bus picking up happy students with backpacks in morning",
    "cf_en_classmate.jpg": "Vector art visual dictionary illustration of friendly high school classmates sitting together at modern classroom desks studying and smiling",
    "cf_en_timetable.jpg": "Vector art visual dictionary illustration of organized weekly school timetable calendar planner schedule with colored subject icons: Math, Science, English",
    "cf_en_take_notes.jpg": "Vector art visual dictionary illustration of high school student hands writing neat notes in notebook with fountain pen and highlighter markers",
    "cf_en_pay_attention.jpg": "Vector art visual dictionary illustration of attentive student listening carefully to teacher in classroom, focused mind lightbulb idea",
    "cf_en_raise_hand.jpg": "Vector art visual dictionary illustration of eager student raising hand politely in modern school classroom to answer teacher question",
    "cf_en_chat_friends.jpg": "Vector art visual dictionary illustration of high school teenagers laughing and chatting happily together in school hallway locker break time",
    "cf_en_frequency_adverbs.jpg": "Vector art visual dictionary infographic chart showing frequency percentages: Always 100%, Usually 80%, Sometimes 50%, Never 0% with colored progress bars",
    "cf_en_how_often.jpg": "Vector art visual dictionary illustration of habit tracking calendar with checklist checkmarks asking How often do you study",
    "cf_de_guten_morgen.jpg": "Vector art visual dictionary illustration of bright morning sunrise over city hills, alarm clock showing 7:00 AM, steaming cup of coffee, Guten Morgen concept",
    "cf_de_guten_tag.jpg": "Vector art visual dictionary illustration of bright sunny midday afternoon in German town square, people greeting each other with a warm smile, Guten Tag",
    "cf_de_abend_nacht.jpg": "Vector art visual dictionary illustration split day-and-night: cozy evening sunset street lamps and starry night sky with glowing crescent moon over quiet bedroom, Guten Abend Gute Nacht",
    "cf_de_farewell.jpg": "Vector art visual dictionary illustration of friends waving goodbye at train station platform, Tschüss and Auf Wiedersehen farewell greeting concept",
    "cf_de_wie_heisst_du.jpg": "Vector art visual dictionary illustration of two new students introducing themselves, wearing Hello My Name Is name badges, friendly handshake",
    "cf_de_wer_bist_du.jpg": "Vector art visual dictionary illustration of student identification card with photo, name Lukas, school logo, Wer bist du identity concept",
    "cf_de_wie_gehts.jpg": "Vector art visual dictionary illustration of mood rating faces with speech bubbles: Super (very happy), Gut (smile), Es geht (neutral), Schlecht (sad)",
    "cf_de_courtesy.jpg": "Vector art visual dictionary illustration of polite student handing a gift or helping friend, Bitte Danke Entschuldigung courtesy etiquette icons",
    "cf_de_pronomen.jpg": "Vector art visual dictionary illustration showing grammatical personal pronouns icons: ich (pointing to self), du (pointing to you), er/sie/es (pointing to others), wir (group), ihr, Sie",
    "cf_de_estten.jpg": "Vector art visual dictionary educational infographic poster showing German regular verb endings E-ST-T-EN-T-EN with colorful building blocks",
    "cf_de_verb_sein.jpg": "Vector art visual dictionary grammar card for German verb sein: ich bin, du bist, er ist, wir sind, ihr seid, sie sind with stick figures",
    "cf_de_zahlen_0_10.jpg": "Vector art visual dictionary illustration of colorful numbers 0 to 10 with German number words: null, eins, zwei, drei, vier, funf, sechs, sieben, acht, neun, zehn",
    "cf_de_zahlen_11_20.jpg": "Vector art visual dictionary illustration of German numbers 11 to 20: elf, zwolf, dreizehn, vierzehn, funfzehn, sechzehn, siebzehn, zwanzig on chalkboard",
    "cf_de_wie_alt.jpg": "Vector art visual dictionary illustration of birthday cake with burning candles showing number 14, Wie alt bist du concept",
    "cf_de_telefonnummer.jpg": "Vector art visual dictionary illustration of smartphone screen showing keypad dialing numbers, calling contact, Wie ist deine Handynummer",
    "cf_de_woher_kommst_du.jpg": "Vector art visual dictionary illustration of airplane flying from Turkey to Germany with travel map and passports, Woher kommst du concept",
    "cf_de_aus_der_tuerkei.jpg": "Vector art visual dictionary illustration of Istanbul Bosphorus bridge and German Brandenburg Gate linked with German grammar tip aus der Turkei, aus Deutschland",
    "cf_de_deutschland_deutsch.jpg": "Vector art visual dictionary illustration of German flag with Brandenburg Gate, Berlin TV Tower, pretzel, Deutschland and Deutsch concept",
    "cf_de_wo_wohnst_du.jpg": "Vector art visual dictionary illustration of a cozy house in a neighborhood with location pin icon, Wo wohnst du address concept",
    "cf_de_welche_sprachen.jpg": "Vector art visual dictionary illustration of multilingual student with speech bubbles speaking Turkish, English and German flags",
    "cf_de_w_fragen.jpg": "Vector art visual dictionary educational infographic of German W-Questions: Wer? Wie? Woher? Wo? Was? Welche? with curious question mark symbols"
}


def generate_flux2(prompt, out_path):
    """Use flux-2-klein-4b via multipart/form-data - returns base64 JSON"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{MODEL}"
    cmd = [
        "curl", "-s", "-S",
        "--resolve", "api.cloudflare.com:443:104.19.192.29",
        "-X", "POST", url,
        "-H", f"Authorization: Bearer {CF_TOKEN}",
        "-F", f"prompt={prompt}",
        "-F", "steps=8",
        "-F", "guidance=7.5",
        "-F", "width=512",
        "-F", "height=512"
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=60)
        if res.returncode != 0:
            return False, f"curl error: {res.stderr.decode()[:80]}"
        raw = res.stdout
        # Try JSON base64
        try:
            data = json.loads(raw)
            if "result" in data and isinstance(data["result"], dict) and "image" in data["result"]:
                img_bytes = base64.b64decode(data["result"]["image"])
                with open(out_path, "wb") as f:
                    f.write(img_bytes)
                return True, f"FLUX2 JSON {len(img_bytes)}B"
            elif "errors" in data and data["errors"]:
                return False, str(data["errors"][0].get("message", ""))[:100]
        except Exception:
            pass
        # Binary fallback
        if len(raw) > 8000 and (raw[:2] == b'\xff\xd8' or raw[:8] == b'\x89PNG\r\n\x1a\n'):
            with open(out_path, "wb") as f:
                f.write(raw)
            return True, f"FLUX2 binary {len(raw)}B"
        return False, f"Unexpected response ({len(raw)}B): {raw[:60]}"
    except subprocess.TimeoutExpired:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)


def generate_sdxl_fallback(prompt, out_path):
    """Fallback: SDXL-Lightning"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/{FALLBACK_MODEL}"
    payload = json.dumps({"prompt": prompt, "num_steps": 4})
    cmd = [
        "curl", "-s", "-S",
        "--resolve", "api.cloudflare.com:443:104.19.192.29",
        "-X", "POST", url,
        "-H", f"Authorization: Bearer {CF_TOKEN}",
        "-H", "Content-Type: application/json",
        "-d", payload
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=45)
        raw = res.stdout
        if len(raw) > 8000:
            with open(out_path, "wb") as f:
                f.write(raw)
            return True, f"SDXL binary {len(raw)}B"
        return False, f"SDXL fail ({len(raw)}B)"
    except Exception as e:
        return False, str(e)


def main():
    media_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "anki_decks", "media"))
    os.makedirs(media_dir, exist_ok=True)

    total = len(PROMPTS)
    print(f"🚀 flux-2-klein-4b ile {total} görsel yeniden üretiliyor...")
    print("=" * 60)

    success = 0
    failed = []

    for i, (filename, prompt) in enumerate(PROMPTS.items(), 1):
        out_path = os.path.join(media_dir, filename)
        print(f"[{i:02d}/{total}] 🎨 {filename}")

        ok, msg = generate_flux2(prompt, out_path)
        if ok:
            print(f"       ✅ {msg}")
            success += 1
        else:
            print(f"       ⚠️  FLUX2 hata: {msg}")
            print(f"       🔄 SDXL fallback deneniyor...")
            ok2, msg2 = generate_sdxl_fallback(prompt, out_path)
            if ok2:
                print(f"       ✅ {msg2}")
                success += 1
            else:
                print(f"       ❌ SDXL de hata: {msg2}")
                failed.append(filename)

        time.sleep(0.5)

    print("=" * 60)
    print(f"🎉 Bitti! Başarılı: {success}/{total}")
    if failed:
        print(f"❌ Başarısız ({len(failed)}): {', '.join(failed)}")
    return len(failed) == 0


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
