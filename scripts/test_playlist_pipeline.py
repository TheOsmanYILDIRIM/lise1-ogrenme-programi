#!/usr/bin/env python3
"""Offline integration checks for LiseDers -> StudyTracker V2 video bridge."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import playlist_studytracker_bridge as mapping
from playlist_transcripts import normalize_vtt

class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for part in ("courses", "lessons", "items"):
            (self.root / "content/v2" / part).mkdir(parents=True)
        self.write("courses/course_mat_9.json", {
            "id": "course_mat_9",
            "lessons": ["lesson_mat9_uslu", "lesson_mat9_fonksiyon"]
        })
        self.write("lessons/lesson_mat9_uslu.json", {
            "id": "lesson_mat9_uslu", "courseId": "course_mat_9",
            "title": "Gerçek Sayıların Üslü ve Köklü Gösterimleri",
            "sourceMeta": {"sourceTopics": ["Üslü ve köklü sayılar"]},
            "items": ["item_existing"]
        })
        self.write("lessons/lesson_mat9_fonksiyon.json", {
            "id": "lesson_mat9_fonksiyon", "courseId": "course_mat_9",
            "title": "Doğrusal Fonksiyonlar ve Nitel Özellikleri",
            "sourceMeta": {"sourceTopics": ["Doğrusal fonksiyonlar"]},
            "items": []
        })
        self.write("items/item_existing.json", {
            "id": "item_existing", "itemType": "VIDEO",
            "orderKey": 100, "contentUrl": "https://www.youtube.com/watch?v=ZZZZZZZZZZZ"
        })
        self.catalog = {
            "playlist_id": "PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II",
            "source_url": "https://youtube.com/playlist?list=PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II",
            "videos": [
                {"id": "Abcdefghijk", "position": 1, "title": "Üslü ve Köklü Sayılar 9. Sınıf"},
                {"id": "ABCDEFGHIJK", "position": 2, "title": "Doğrusal Fonksiyonlar 9. Sınıf"},
                {"id": "12345678901", "position": 3, "title": "9. Sınıf 3. Ders"}
            ]
        }
    def write(self, path, obj):
        target = self.root / "content/v2" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")

    def test_vtt_cues_preserve_timestamps_and_no_adjacent_duplicates(self):
        vtt = ("WEBVTT\n\n00:00:01.000 --> 00:00:02.000\nMerhaba &amp; selam\n\n"
               "00:00:02.000 --> 00:00:03.000\nMerhaba &amp; selam\n\n"
               "00:00:04.000 --> 00:00:05.000\n<b>Üslü sayılar</b>\n")
        cues = normalize_vtt(vtt)
        self.assertEqual(len(cues), 2)
        self.assertEqual(cues[0], {"start": "00:00:01.000", "text": "Merhaba & selam"})
        self.assertEqual(cues[1]["text"], "Üslü sayılar")

    def test_curriculum_matching_and_ambiguity(self):
        result = mapping.match_playlist(self.catalog, self.root)
        self.assertEqual(result["summary"]["videos"], 3)
        self.assertEqual(result["videos"][0]["best_match"]["lesson_id"], "lesson_mat9_uslu")
        self.assertEqual(result["videos"][1]["best_match"]["lesson_id"], "lesson_mat9_fonksiyon")
        self.assertEqual(result["videos"][2]["review_status"], "needs_review")
        self.assertNotEqual(result["videos"][0]["review_status"], "already_present")

    def test_existing_url_prevents_remap(self):
        self.catalog["videos"][0]["id"] = "ZZZZZZZZZZZ"
        result = mapping.match_playlist(self.catalog, self.root)
        self.assertEqual(result["videos"][0]["review_status"], "already_present")

    def test_import_is_review_gated_and_preserves_existing_items(self):
        importer = self.root / "studytracker_importer.py"
        source = Path(sys.argv[0]).resolve().parent.parent / "study-tracker/scripts/import-liseders-playlist.py"
        self.assertTrue(source.exists(), f"Missing StudyTracker importer checkout: {source}")
        result = mapping.match_playlist(self.catalog, self.root)
        manifest = self.root / "mapping.json"
        manifest.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
        approvals = self.root / "approvals.json"
        approvals.write_text(json.dumps({"approvals": [{
            "video_id": "Abcdefghijk", "lesson_id": "lesson_mat9_uslu",
            "reviewed": True, "reason": "Manually compared source title and lesson",
            "publish": False
        }]}), encoding="utf-8")
        cmd = [sys.executable, str(source), "--root", str(self.root),
               "--mapping", str(manifest), "--approvals", str(approvals)]
        dry = subprocess.run(cmd, text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(dry.stdout)["added"], 1)
        lesson = json.loads((self.root / "content/v2/lessons/lesson_mat9_uslu.json").read_text())
        self.assertEqual(lesson["items"], ["item_existing"])
        applied = subprocess.run(cmd + ["--apply"], text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(applied.stdout)["drafts"], 1)
        lesson = json.loads((self.root / "content/v2/lessons/lesson_mat9_uslu.json").read_text())
        self.assertEqual(len(lesson["items"]), 2)
        self.assertEqual(lesson["items"][0], "item_existing")
        new = json.loads((self.root / "content/v2/items" / (lesson["items"][1] + ".json")).read_text())
        self.assertEqual(new["publishingStatus"], "draft")
        self.assertEqual(new["contentUrl"], "https://www.youtube.com/watch?v=Abcdefghijk")
        again = subprocess.run(cmd + ["--apply"], text=True, capture_output=True, check=True)
        self.assertEqual(json.loads(again.stdout)["existing"], 1)

    def test_invalid_approval_rejected(self):
        from importlib.util import spec_from_file_location, module_from_spec
        p = Path(sys.argv[0]).resolve().parent.parent / "study-tracker/scripts/import-liseders-playlist.py"
        spec = spec_from_file_location("st_import", p)
        mod = module_from_spec(spec)
        spec.loader.exec_module(mod)
        result = mapping.match_playlist(self.catalog, self.root)
        with self.assertRaises(ValueError):
            mod.prepare(result, {"approvals": [{
                "video_id": "Abcdefghijk", "lesson_id": "lesson_mat9_wrong",
                "reviewed": True, "reason": "wrong"
            }]}, self.root)

if __name__ == "__main__":
    unittest.main(verbosity=2)
