#!/usr/bin/env python3
"""Propose playlist-to-StudyTracker V2 lesson mappings without changing live content.

Uses the real modular lesson catalog and sourceMeta, plus YouTube titles and optional
Turkish subtitle text. Conservative scoring is only a review aid, NOT validation.
"""
import argparse
import collections
import json
import math
import re
import unicodedata
from pathlib import Path

STOP = {
    "9", "sinif", "sinifi", "matematik", "ders", "dersi", "konu", "anlatimi",
    "anlatim", "yeni", "maarif", "modeli", "model", "mufredat", "video", "test",
    "soru", "cozumu", "cozum", "bolum", "tema", "2025", "2026", "2027",
    "ilyas", "gunes", "ve", "ile", "icin", "bir", "ornek", "ornekler",
    "pdf", "kampi", "kamp", "tum", "tam", "sinavi", "ilk"
}
STEMS = {
    "say": "sayi", "uslu": "uslu", "uss": "uslu", "kok": "kok",
    "aralik": "aralik", "kume": "kume", "fonksi": "fonksiyon",
    "mutlak": "mutlak", "dogrusal": "dogrusal", "esitsiz": "esitsizlik",
    "denklem": "denklem", "benzer": "benzerlik", "eslik": "eslik",
    "ucgen": "ucgen", "istatis": "istatistik", "olasil": "olasilik",
    "cebir": "cebir", "geomet": "geometri", "donus": "donusum",
    "pisag": "pisagor", "tales": "tales", "oklid": "oklid",
    "algori": "algoritma", "mantik": "mantik", "veri": "veri",
    "islem": "islem", "ozelli": "ozellik", "gercek": "gercek",
    "esitle": "esitlik", "nicel": "nicelik"
}

# Explicit playlist themes: infer only thematic scope when the title is generic.
# Never guess a subtopic such as linear vs absolute-value functions from a
# "Quantities and Changes - 4" title without spoken transcript evidence.
THEMES = [
    (r"exponent|uslu|usslu|radical|koklu", "Sayılar / Üslü ve Köklü",
     ["lesson_mat9_sayilar_uslu_koklu"], True),
    (r"quantities\s+and\s+changes|nicelikler\s+ve\s+degisimler",
     "Nicelikler ve Değişimler",
     ["lesson_mat9_topic_05_dogrusal_fonksiyonlar_ve_nitel_ozellikleri",
      "lesson_mat9_topic_06_mutlak_deger_fonksiyonu_ve_nitel_ozellikleri",
      "lesson_mat9_topic_07_dogrusal_fonksiyonlarla_denklem_ve_esitsizlik_proble"], False),
    (r"geometrik\s+donusum|geometric\s+transfor", "Geometri / Dönüşümler",
     ["lesson_mat9_topic_09_geometrik_donusumler"], True),
    (r"ucgende\s+aci\s+kenar|ucgende\s+acilar|dogruda\s+acilar",
     "Geometri / Açılar", ["lesson_mat9_ucgende_acilar_kenarlar"], False),
    (r"ucgende\s+eslik|ucgende\s+benzerlik|eslik\s+ve\s+benzerlik|dik\s+ucgen",
     "Geometri / Eşlik ve Benzerlik",
     ["lesson_mat9_eslik_ve_benzerlik",
      "lesson_mat9_topic_11_benzer_ucgenler_olusturma",
      "lesson_mat9_topic_12_tales_oklid_ve_pisagor_teoremleri",
      "lesson_mat9_topic_13_eslik_ve_benzerlik_problemleri"], False),
    (r"geometrik\s+sekiller|geometric\s+shapes",
     "Geometri / Karma", ["lesson_mat9_ucgende_acilar_kenarlar",
                           "lesson_mat9_eslik_ve_benzerlik"], False),
    (r"algorithm|algoritma|informatics|bilisim", "Algoritma ve Bilişim",
     ["lesson_mat9_algoritma_ve_mantik",
      "lesson_mat9_topic_14_algoritma_temelli_problemler"], False),
    (r"istatistik|statistics|statistical|research\s+process",
     "İstatistiksel Araştırma Süreci",
     ["lesson_mat9_istatistik_veri_dagilimi",
      "lesson_mat9_topic_17_tek_nicel_degiskenli_veri_dagilimlari",
      "lesson_mat9_topic_18_hazir_veri_dagilimlarini_inceleme_ve_yorumlama"], False),
    (r"veriden\s+olasiliga|probability\s+from\s+data", "Veriden Olasılığa",
     ["lesson_mat9_veriden_olasiliga", "lesson_mat9_topic_19_deneysel_olasilik"], False),
]
def thematic_scope(title, existing_lessons):
    normalized = " ".join(norm(title))
    if re.search(r"yazili|exam|sinav\s+hazirlik", normalized):
        return {"theme": "Genel Tekrar / Yazılı Hazırlığı",
                "lesson_ids": [], "topic_specific": False}
    for pattern, theme, lesson_ids, specific in THEMES:
        if re.search(pattern, normalized):
            return {"theme": theme, "lesson_ids": [
                x for x in lesson_ids if x in existing_lessons],
                "topic_specific": specific}
    return {"theme": "Belirsiz", "lesson_ids": [], "topic_specific": False}

def teacher_of(video):
    name = " ".join(norm(video.get("title", "")))
    channel = " ".join(norm(video.get("channel", "")))
    if "nurtac kozak" in name:
        return "Nurtaç Kozak"
    if "ilyas gunes" in name or "ilyas gunes" in channel:
        return "İlyas Güneş"
    return None

def norm(text):
    text = str(text or "").translate(str.maketrans(
        {"ı": "i", "İ": "I", "ğ": "g", "Ğ": "G", "ş": "s", "Ş": "S",
         "ö": "o", "Ö": "O", "ü": "u", "Ü": "U", "ç": "c", "Ç": "C"}))
    text = "".join(c for c in unicodedata.normalize("NFKD", text)
                   if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", text.lower())

def signals(text):
    tokens = []
    for token in norm(text):
        if token in STOP or len(token) < 3 or token.isdigit():
            continue
        stem = next((v for k, v in STEMS.items() if token.startswith(k)), token)
        if stem not in STOP:
            tokens.append(stem)
    return set(tokens)

def studytracker_lessons(root, course_id):
    course_path = root / "content/v2/courses" / f"{course_id}.json"
    course = json.loads(course_path.read_text(encoding="utf-8"))
    if course["id"] != course_id:
        raise ValueError("Course ID mismatch")
    lessons = []
    for lesson_id in course["lessons"]:
        path = root / "content/v2/lessons" / f"{lesson_id}.json"
        lesson = json.loads(path.read_text(encoding="utf-8"))
        if lesson["id"] != lesson_id or lesson.get("courseId") != course_id:
            raise ValueError(f"Lesson ID or parent mismatch: {lesson_id}")
        lessons.append(lesson)
    if not lessons:
        raise ValueError("Course has no lessons")
    return lessons

def existing_video_urls(root):
    out = collections.defaultdict(list)
    for path in (root / "content/v2/items").glob("*.json"):
        item = json.loads(path.read_text(encoding="utf-8"))
        if item.get("itemType") == "VIDEO":
            match = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})",
                              item.get("contentUrl") or "")
            if match:
                out[match.group(1)].append(item["id"])
    return out

def score_one(title_tokens, transcript_tokens, lesson, document_frequency, total):
    target = signals(lesson["title"])
    sources = signals(" ".join(lesson.get("sourceMeta", {}).get("sourceTopics", [])))
    shared = title_tokens & target
    if not title_tokens or not target or not shared:
        return 0.0, []
    def weight(t):
        return 1.0 + math.log((total + 1) / (document_frequency[t] + 1))
    numerator = sum(weight(x) for x in shared)
    precision = numerator / sum(weight(x) for x in title_tokens)
    recall = numerator / sum(weight(x) for x in target)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    source_hit = len(title_tokens & sources) / max(len(title_tokens), 1)
    caption_hit = len(transcript_tokens & target) / max(len(target), 1) if transcript_tokens else 0
    confidence = min(1.0, round(0.88 * f1 + 0.07 * source_hit + 0.05 * caption_hit, 4))
    return confidence, sorted(shared)

def match_playlist(catalog, root, course_id="course_mat_9", transcript_dir=None):
    videos = catalog.get("videos") or []
    if not isinstance(videos, list) or not videos:
        raise ValueError("Empty playlist catalog")
    lessons = studytracker_lessons(root, course_id)
    df = collections.Counter()
    for lesson in lessons:
        df.update(signals(lesson["title"]))
    present = existing_video_urls(root)
    transcript_dir = Path(transcript_dir) if transcript_dir else None
    manifest_lookup = {}
    if transcript_dir and (transcript_dir / "manifest.json").exists():
        manifest = json.loads((transcript_dir / "manifest.json").read_text(encoding="utf-8"))
        manifest_lookup = {r["id"]: r for r in manifest["videos"]}
    results = []
    seen = set()
    for video in videos:
        vid = str(video.get("id") or "")
        if not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid) or vid in seen:
            raise ValueError(f"Invalid or duplicate video id: {vid}")
        seen.add(vid)
        title = str(video.get("title") or "")
        meta = manifest_lookup.get(vid, {})
        text_path = transcript_dir / f"{vid}.tr.txt" if transcript_dir else None
        caption_tokens = signals(text_path.read_text(encoding="utf-8")[:10000]) if (
            text_path and text_path.is_file()) else set()
        tokens = signals(title)
        candidates = []
        for lesson in lessons:
            s, shared = score_one(tokens, caption_tokens, lesson, df, len(lessons))
            candidates.append({
                "lesson_id": lesson["id"], "lesson_title": lesson["title"],
                "score": s, "shared_signals": shared
            })
        candidates.sort(key=lambda x: (-x["score"], x["lesson_id"]))
        best = candidates[0]
        gap = best["score"] - candidates[1]["score"] if len(candidates) > 1 else best["score"]
        theme = thematic_scope(title, {x["id"] for x in lessons})
        themed = theme["lesson_ids"]
        # An explicit subject like "Exponents" or "Geometric Transformations"
        # identifies its module, but does not establish transcript-grounding.
        if theme["topic_specific"] and len(themed) == 1:
            lesson = next(x for x in lessons if x["id"] == themed[0])
            best = {
                "lesson_id": lesson["id"], "lesson_title": lesson["title"],
                "score": max(best["score"], 0.7), "shared_signals": ["explicit-title-topic"],
                "method": "title_topic_rule"
            }
            category = "candidate"
        elif themed:
            # Broad theme ≠ exact lecture-to-lesson match.
            best = None
            category = "needs_review"
        else:
            category = ("candidate" if (best["score"] >= 0.50 and gap >= 0.12
                                        and len(best["shared_signals"]) >= 2)
                        else "needs_review")
        if vid in present:
            category = "already_present"
        results.append({
            "video_id": vid, "position": video.get("position"), "title": title,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "channel": video.get("channel"), "teacher": teacher_of(video),
            "theme": theme["theme"], "theme_lesson_ids": themed,
            "matching_scope": "specific_title_topic" if theme["topic_specific"] else "theme_only",
            "transcript_status": meta.get("status", "not_attempted"),
            "transcript_fingerprint": meta.get("fingerprint"),
            "existing_item_ids": present.get(vid, []),
            "review_status": category,
            "best_match": best if best and best["score"] else None,
            "candidates": [c for c in candidates[:3] if c["score"]]
        })
    counts = dict(collections.Counter(r["review_status"] for r in results))
    counts.update({"transcripts_fetched": sum(r["transcript_status"] == "fetched" for r in results)})
    return {
        "schema_version": 1,
        "playlist_id": catalog.get("playlist_id"),
        "source_url": catalog.get("source_url"),
        "target_repo": "TheOsmanYILDIRIM/study-tracker",
        "course_id": course_id,
        "matching_method": "explicit bilingual theme/title rules plus token ranking; all matches require review",
        "summary": {"videos": len(results), **counts},
        "videos": results
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", required=True)
    p.add_argument("--studytracker-dir", required=True)
    p.add_argument("--course", default="course_mat_9")
    p.add_argument("--transcripts")
    p.add_argument("--output", required=True)
    args = p.parse_args()
    src = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    result = match_playlist(src, Path(args.studytracker_dir), args.course, args.transcripts)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False))
    for x in result["videos"]:
        match = x["best_match"]
        print(f"{str(x['position']).rjust(2)} {x['review_status']:<15} {x['video_id']} "
              f"{(match or {}).get('score', 0):.2f} -> {(match or {}).get('lesson_title', '-')}: "
              f"{x['title'][:65]}", flush=True)

if __name__ == "__main__":
    main()
