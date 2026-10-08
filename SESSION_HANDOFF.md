# LiseDers — SESSION_HANDOFF

Updated: 2026-10-08 · `main`
Last inspected HEAD: `6d6d30b495` (Actions bot committed playlist-review data)

## Canonical purpose
MEB 9th-grade TYMM curriculum + external StudyTracker V2 content sourcing. Rules: `AGENTS.md`. The Android runtime/progress/QUIZ and live video item IDs belong to `TheOsmanYILDIRIM/study-tracker`.

## Latest completed: YouTube playlist → StudyTracker review bridge
- `.github/workflows/youtube-playlist.yml` checks out both repos, tests mapping/importer behavior, uses yt-dlp on playlist, attempts Turkish captions (preserves status and timecoded cues when accessible), proposes V2 lesson matches and exercises the StudyTracker import in **dry-run**.
- Default playlist: `PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II` (9th-grade math). The playlist includes İlyas Güneş and other teachers including Nurtaç Kozak. Do not label all videos as one teacher.
- `scripts/playlist_transcripts.py`: no fabricated transcripts; detects YouTube bot gate after two failures and marks unattempted videos `blocked`.
- `scripts/playlist_studytracker_bridge.py`: bilingual title/thematic matching to actual V2 math lessons; ambiguous subtopics remain `needs_review`. `scripts/test_playlist_pipeline.py` covers integration behavior.
- Successful live GitHub Action **run #10** `37824267157`: **8 tests passed**; 60 playlist videos; 12 topic-specific candidates, 48 review-needed. Turkish transcripts: 0 fetched, 2 bot errors, 58 blocked by circuit breaker.
- The run wrote source-controlled artifacts at `data/video_playlists/PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II/`: `playlist-catalog.json`, `topic-matches.json`, `transcript-status.json`. No full video or transcript is committed.
- `docs/PLAYLIST_TO_STUDYTRACKER.md` documents the integration and approval process. Full extraction runs on manual `workflow_dispatch` or scoped push containing `[playlist-run]`; ordinary code pushes run only fast unit tests.
- StudyTracker importer is `study-tracker/scripts/import-liseders-playlist.py`, with a separate reviewed-import Action. Unreviewed mappings MUST NOT overwrite V2 items or progress.

## Open work / next action
1. Access actual Turkish captions through an authorized, permitted source or manually supplied transcripts; GitHub runner YouTube bot block prevents transcript-backed fine-grained validation. Do not bypass platform controls.
2. Review per-video and per-teacher details, especially broad "Nicelikler ve Değişimler" and similar numbered series; fill only verified StudyTracker approvals.
3. Use StudyTracker reviewed-import Action in dry-run, then optional explicitly approved publishing. Validate compiled V2 catalog and check APK build independently.
4. Older independent follow-up: check `README.md`/`INDEX.md` device-local `file://` links and historical Anki card count discrepancies.

## Do not claim
Automated topic candidates are not verified individual learning outcomes. Zero captions means no transcript-grounded quiz. No StudyTracker lesson or student progress has yet been changed by this playlist.
