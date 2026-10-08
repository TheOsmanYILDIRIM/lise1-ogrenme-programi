#!/usr/bin/env python3
"""Purely offline tests for Android YTDLnis subtitle export ingestion."""
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from import_ytdlnis_subtitles import import_subtitles, match_name, load_catalog

VTT = (
    "WEBVTT\n\n"
    "00:00:01.000 --> 00:00:02.500\nMerhaba &amp; hoş geldiniz\n\n"
    "00:00:02.501 --> 00:00:03.000\nMerhaba &amp; hoş geldiniz\n\n"
    "00:00:04.000 --> 00:00:06.000\nÜslü sayılar\n"
)
SRT = (
    "1\n00:00:01,000 --> 00:00:03,000\nDoğrusal fonksiyon\n\n"
    "2\n00:00:04,000 --> 00:00:07,000\nMutlak değer\n"
)

class YTDLnisImportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.catalog_path = self.root / "playlist-catalog.json"
        self.catalog = {
            "playlist_id": "PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II",
            "videos": [
                {"position": 1, "id": "mHq3Dz1Kyw4",
                 "title": "1.Ders | 9. Sınıf Üslü Sayılar -1 | Maarif Modeli Matematik Konu Anlatımı | İlyas Güneş"},
                {"position": 2, "id": "IsD7EfCBZik",
                 "title": "2.Ders | 9. Sınıf Üslü Sayılar-2 | İlyas Güneş"},
                {"position": 3, "id": "BVc7pkpAx7E",
                 "title": "6)9.Sınıf - Matematik - Üçgende Açı - Kenar Bağıntıları - Nurtaç KOZAK"},
                {"position": 4, "id": "VWSO0XMx7tQ",
                 "title": "9.Sınıf - Matematik- Geometrik Dönüşümler - Nurtaç KOZAK"}
            ]
        }
        self.catalog_path.write_text(json.dumps(self.catalog, ensure_ascii=False), encoding="utf-8")
        self.dir = self.root / "download"
        self.dir.mkdir()
        self.out = self.root / "normalized"

    def add(self, file, contents):
        p = self.dir / file
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(contents, encoding="utf-8")

    def test_id_based_file_mapping_and_timecoded_cues(self):
        self.add("Matematik/001 - mHq3Dz1Kyw4 - Üslü sayılar.tr.vtt", VTT)
        m = import_subtitles(self.catalog_path, self.dir, self.out)
        self.assertEqual(m["status_counts"]["fetched"], 1)
        self.assertEqual(m["status_counts"]["missing"], 3)
        self.assertEqual(m["videos"][0]["matching_method"], "video_id")
        self.assertEqual(m["videos"][0]["cue_count"], 2)
        t = (self.out / "transcripts/mHq3Dz1Kyw4.tr.txt").read_text()
        self.assertEqual(t, "Merhaba & hoş geldiniz\nÜslü sayılar\n")
        cues = json.loads((self.out / "transcripts/mHq3Dz1Kyw4.tr.cues.json").read_text())["cues"]
        self.assertEqual(cues[0]["start"], "00:00:01.000")
        self.assertEqual(cues[1]["start"], "00:00:04.000")

    def test_original_ytdlnis_template_without_video_ids_can_match_index_and_exact_title(self):
        title = self.catalog["videos"][1]["title"]
        self.add(f"9.SINIF/2 - {title}.tr.vtt", VTT)
        m = import_subtitles(self.catalog_path, self.dir, self.out)
        self.assertEqual(m["videos"][1]["matching_method"], "index_and_verified_title")
        self.assertEqual(m["videos"][1]["status"], "fetched")

    def test_mismatching_title_must_not_use_playlist_index_alone(self):
        self.add("1 - Kimya konulari - bambaşka kanal.tr.vtt", VTT)
        m = import_subtitles(self.catalog_path, self.dir, self.out)
        self.assertEqual(m["status_counts"]["fetched"], 0)
        self.assertEqual(len(m["unmatched_files"]), 1)
        self.assertIn("title mismatch", m["unmatched_files"][0]["reason"])

    def test_explicit_video_id_takes_priority_over_mismatching_title(self):
        self.add("001 - IsD7EfCBZik - farklı dosya ismi.tr.vtt", VTT)
        m = import_subtitles(self.catalog_path, self.dir, self.out)
        self.assertEqual(m["videos"][1]["status"], "fetched")
        self.assertEqual(m["videos"][0]["status"], "missing")

    def test_never_ingest_english_captions_as_turkish(self):
        self.add("001 - mHq3Dz1Kyw4 - Üslü sayılar.en.vtt", VTT)
        m = import_subtitles(self.catalog_path, self.dir, self.out)
        self.assertEqual(m["status_counts"]["fetched"], 0)
        self.assertEqual(len(m["unmatched_files"]), 1)

    def test_duplicate_subtitle_files_are_not_silently_merged(self):
        self.add("001 - mHq3Dz1Kyw4 - Üslü sayılar.tr.vtt", VTT)
        self.add("001 - mHq3Dz1Kyw4 - Üslü sayılar.tr.srt", SRT)
        m = import_subtitles(self.catalog_path, self.dir, self.out)
        self.assertEqual(m["status_counts"]["duplicate"], 1)
        self.assertFalse((self.out / "transcripts/mHq3Dz1Kyw4.tr.txt").exists())

    def test_srt_support_and_zip_nested_playlist_subdir(self):
        zipped = self.root / "captions.zip"
        with zipfile.ZipFile(zipped, "w") as archive:
            archive.writestr("9.SINIF/003 - BVc7pkpAx7E - Açılar.tr.srt", SRT)
        m = import_subtitles(self.catalog_path, zipped, self.out)
        self.assertEqual(m["status_counts"]["fetched"], 1)
        self.assertEqual(m["videos"][2]["cue_count"], 2)
        self.assertTrue((self.out / "transcripts/BVc7pkpAx7E.tr.cues.json").exists())

    def test_reject_zip_path_traversal(self):
        zipped = self.root / "bad.zip"
        with zipfile.ZipFile(zipped, "w") as archive:
            archive.writestr("../evil.tr.vtt", VTT)
        with self.assertRaisesRegex(ValueError, "Unsafe ZIP member"):
            import_subtitles(self.catalog_path, zipped, self.out)

    def test_empty_or_invalid_vtt_is_reported(self):
        self.add("mHq3Dz1Kyw4 - Üslü sayılar.tr.vtt", "WEBVTT\nnot real cues\n")
        m = import_subtitles(self.catalog_path, self.dir, self.out)
        self.assertEqual(m["status_counts"]["fetched"], 0)
        self.assertEqual(len(m["invalid_files"]), 1)

    def test_real_catalog_has_stable_video_ids_and_positions(self):
        external = HERE.parent / "data/video_playlists/PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II/playlist-catalog.json"
        if not external.exists():
            self.skipTest("Repo playlist source not available in fixture checkout")
        catalog, by_id, by_position = load_catalog(external)
        self.assertEqual(len(by_id), 60)
        self.assertEqual(by_position[1]["id"], "mHq3Dz1Kyw4")
        self.assertEqual(by_position[60]["id"], "YFLa4qHIfls")

if __name__ == "__main__":
    unittest.main(verbosity=2)
