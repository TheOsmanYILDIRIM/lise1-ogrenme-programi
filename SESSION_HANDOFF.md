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
