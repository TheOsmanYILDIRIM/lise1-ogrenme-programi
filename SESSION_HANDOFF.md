# LiseDers — SESSION_HANDOFF

Updated: 2026-10-08 · `main`
Repository: `TheOsmanYILDIRIM/lise1-ogrenme-programi`

## Current goal and scope
- User wants transcripts of playlist `PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II` (60 videos) to inspect lesson content. Mathematics 9 rebuild was explicitly STOPPED; **do not change StudyTracker course or progress without a fresh instruction.**
- Last successful GitHub-hosted playlist metadata action collected 60 records. The 1-video nightly probe `37828581593` used yt-dlp nightly, yt-dlp-ejs and Deno but got YouTube `LOGIN_REQUIRED / not a bot`; **no captions have been retrieved via GitHub runner**. Video IDs and titles remain in `data/video_playlists/<playlist-id>/playlist-catalog.json`.

## Android / YTDLnis fallback (implemented)
- User supplied existing YTDLnis command template that saves local Turkish captions. Official YTDLnis docs: Command templates contain yt-dlp **arguments only**, no URL; the app adds the supplied playlist link.
- Importable corrected template: `configs/ytdlnis_playlist_subtitles.json`. Includes `%(id)s` in file names, playlist index/title, Turkish caption languages and `--skip-download`.
- New safe offline processor: `scripts/import_ytdlnis_subtitles.py`; reads Android subtitle ZIP or folder without extracting ZIP paths, matches stable video IDs or original template's **index + verified title** (never index alone), handles `.tr.vtt`/`.tr.srt`, produces timecoded `.cues.json`, text and manifest under `output/ytdlnis/transcripts/`. No network requests, no invented captions.
- New tests `scripts/test_ytdlnis_import.py`; the scoped test-only workflow [run #37832964092](https://github.com/TheOsmanYILDIRIM/lise1-ogrenme-programi/actions/runs/37832964092) **success**: 10/10 YTDLnis tests, 8/8 existing bridge tests, 11/11 StudyTracker replacement-contract tests. Full YouTube extraction was not triggered.
- Documentation: `docs/YTDLNIS_ANDROID_SUBTITLES.md`. `.gitignore` protects `/output/` and caption data from accidental commits.
- Source playlist includes teacher/channel diversity (İlyas Güneş; Nurtaç Kozak) and ambiguous titles; do not infer finer lesson topics from generic numbered labels.

## Next step
1. User imports corrected YTDLnis template in Android, selects the playlist in app's Command mode, and checks whether caption files are actually produced on-device. This remains **unverified**.
2. User provides ZIP of downloaded subtitle files (or runs the offline importer in Termux); record exact coverage/failures. No secrets/cookies in ZIP.
3. If coverage exists, call `scripts/playlist_studytracker_bridge.py --transcripts output/ytdlnis/transcripts` for evidence-assisted matching. Keep student/course data unchanged until explicitly asked.
4. Unrelated older backlog: fix local `file://` links and inconsistent Anki counts.

## 2026-10-08 — user supplied full transcript ZIP
- User uploaded `9.SINIF VİDEO DERS KİTABI KONU ANLATIM.zip`, containing exactly 60 Turkish VTT captions (one per playlist index 1–60). Verified offline: 64,720 timecoded cues, 3,566,940 normalized characters, no missing positions. Original 11 MB captions are not committed to public Git.
- New `data/video_playlists/PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II/transcript_evidence.json` records 8-theme coverage and term-frequency signals; do not mistake frequency for exact MEB outcomes.
- `scripts/import_ytdlnis_subtitles.py --complete-index-archive` now handles the uploaded ZIP's index/title-only filenames despite YouTube-localized catalog titles; requires full unique positions, no partial silent mapping. Tests expanded, GitHub Actions run `37838156685` succeeded.
- Normalized complete transcript ZIP generated as a conversation artifact for subsequent processing, not uploaded to public Git. StudyTracker plan is `docs/MATH9_TRANSCRIPT_REBUILD_PLAN.md`.
- Next: use timecoded transcripts for 60-video subtopic/curriculum alignment and verified quiz drafts; preserve old student attempts and progress. Do not claim a deployed new Math 9 course.

## 2026-10-08 — User approved public ZIP storage
- User explicitly authorized committing the 3,754,495-byte `math9_normalized_transcripts.zip` into LiseDers. Expected path: `data/video_playlists/PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II/math9_normalized_transcripts.zip`; SHA-256 `1c45d1b1e8d4caec312f117dcba4a6bc53b69aa5047d062a42a9c746f830f1d9`, 182 members, CRC valid, 60 complete VTT/TXT/CUES triples.
- **Binary ZIP has not yet been uploaded to GitHub:** available GitHub connector supports text content updates or base64 blob strings but cannot read the local 3.75MB binary directly. Do not claim remote presence. User can use GitHub web Add file → Upload files at the path; then CI will validate.
- Added `.github/workflows/validate-math9-transcripts.yml` for SHA/CRC/coverage validation. StudyTracker plan `docs/MATH9_TRANSCRIPT_REBUILD_PLAN.md` updated with P0–P5 acceptance criteria and progress-safe versioning.
- Next: verify binary remote presence and CI, then implement timestamp-level curriculum alignment and V2 draft.
