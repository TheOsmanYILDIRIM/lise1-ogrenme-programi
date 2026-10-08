import re

with open("scripts/build_language_apkg.py", "r", encoding="utf-8") as f:
    code = f.read()

en_map = {
    "Country": "cf_en_country.jpg",
    "Nationality": "cf_en_nationality.jpg",
    "Language": "cf_en_language.jpg",
    "Native language": "cf_en_native_lang.jpg",
    "Capital city": "cf_en_capital_city.jpg",
    "Where are you from?": "cf_en_where_from.jpg",
    "South Korea / South Korean": "cf_en_south_korea.jpg",
    "Norway / Norwegian": "cf_en_norway.jpg",
    "Chile / Chilean": "cf_en_chile.jpg",
    "Morocco / Moroccan": "cf_en_morocco.jpg",
    "Peru / Peruvian": "cf_en_peru.jpg",
    "Speak fluently": "cf_en_speak_fluently.jpg",
    "Tourist attraction": "cf_en_tourist_attraction.jpg",
    "Historical site": "cf_en_historical_site.jpg",
    "Ancient": "cf_en_ancient.jpg",
    "Modern": "cf_en_modern.jpg",
    "Fascinating": "cf_en_fascinating.jpg",
    "Crowded": "cf_en_crowded.jpg",
    "Peaceful": "cf_en_peaceful.jpg",
    "Celebrate": "cf_en_celebrate.jpg",
    "National day": "cf_en_national_day.jpg",
    "Gather together": "cf_en_gather_together.jpg",
    "Wear traditional clothes": "cf_en_traditional_clothes.jpg",
    "Take photos": "cf_en_take_photos.jpg",
    "Daily routine": "cf_en_daily_routine.jpg",
    "Wake up / Get up": "cf_en_wake_up.jpg",
    "Have breakfast": "cf_en_have_breakfast.jpg",
    "Take the school bus": "cf_en_school_bus.jpg",
    "Classmate": "cf_en_classmate.jpg",
    "Timetable / Schedule": "cf_en_timetable.jpg",
    "Take notes": "cf_en_take_notes.jpg",
    "Pay attention": "cf_en_pay_attention.jpg",
    "Raise hand": "cf_en_raise_hand.jpg",
    "Chat with friends": "cf_en_chat_friends.jpg",
    "Always / Usually / Sometimes / Never": "cf_en_frequency_adverbs.jpg",
    "How often...?": "cf_en_how_often.jpg"
}

de_map = {
    "Guten Morgen!": "cf_de_guten_morgen.jpg",
    "Guten Tag!": "cf_de_guten_tag.jpg",
    "Guten Abend! / Gute Nacht!": "cf_de_abend_nacht.jpg",
    "Tschüss! / Auf Wiedersehen!": "cf_de_farewell.jpg",
    "Wie heißt du?": "cf_de_wie_heisst_du.jpg",
    "Wer bist du? / Mein Name ist...": "cf_de_wer_bist_du.jpg",
    "Wie geht's? / Wie geht es dir?": "cf_de_wie_gehts.jpg",
    "Bitte / Danke / Entschuldigung": "cf_de_courtesy.jpg",
    "Personalpronomen (Kişi Zamirleri)": "cf_de_pronomen.jpg",
    "ESTTEN Kuralı (Düzenli Fiil Çekimi)": "cf_de_estten.jpg",
    "sein (Olmak Fiili)": "cf_de_verb_sein.jpg",
    "Zahlen 0 - 10 (Sayılar 0-10)": "cf_de_zahlen_0_10.jpg",
    "Zahlen 11 - 20 (Sayılar 11-20)": "cf_de_zahlen_11_20.jpg",
    "Wie alt bist du?": "cf_de_wie_alt.jpg",
    "Wie ist deine Telefonnummer?": "cf_de_telefonnummer.jpg",
    "Woher kommst du?": "cf_de_woher_kommst_du.jpg",
    "die Türkei / die Schweiz (Artikelli Ülkeler)": "cf_de_aus_der_tuerkei.jpg",
    "Deutschland / Deutsch": "cf_de_deutschland_deutsch.jpg",
    "Wo practical/Wohnort: Wo wohnst du?": "cf_de_wo_wohnst_du.jpg",
    "Welche Sprachen sprichst du?": "cf_de_welche_sprachen.jpg",
    "W-Fragen (Soru Kelimeleri)": "cf_de_w_fragen.jpg"
}

all_maps = {**en_map, **de_map}
replaced_count = 0

for word, img in all_maps.items():
    pattern = re.compile(r'("word":\s*"' + re.escape(word) + r'",.*?"image":\s*")[^"]+(")', re.DOTALL)
    new_code, count = pattern.subn(r'\g<1>' + img + r'\g<2>', code)
    if count > 0:
        code = new_code
        replaced_count += count
    else:
        print("Warning: word not matched:", word)

with open("scripts/build_language_apkg.py", "w", encoding="utf-8") as f:
    f.write(code)

print(f"Successfully mapped {replaced_count} words to Cloudflare AI images in scripts/build_language_apkg.py")
