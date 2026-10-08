# LiseDers — SESSION_HANDOFF

Updated: 2026-10-08 · `main`

## Current task: replace existing StudyTracker Math 9 video sources
- User specifically requested **only changing disliked teacher videos in existing Math 9 cards**, not adding courses or new items. New VIDEO append importer was retired from current Actions flow.
- Playlist `PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II`: 60 videos, includes İlyas Güneş and other teachers (Nurtaç Kozak). Source-controlled metadata under `data/video_playlists/<playlist-id>/{playlist-catalog.json,topic-matches.json,transcript-status.json}`.
- `.github/workflows/youtube-playlist.yml` performs scoped code/test push; full yt-dlp extraction only on manual dispatch or `[playlist-run]` commit. A full successful live run #`37824267157` collected all 60 video metadata records and reported 0 Turkish transcripts: 2 bot errors, 58 circuit-breaker blocked.
- Title/playlist theme mapping suggests topics; it does **not** prove video subtopic contents without review. `scripts/playlist_studytracker_bridge.py` and `scripts/playlist_transcripts.py` own preparation and evidence statuses.
- Updated workflow now uses StudyTracker `scripts/replace-liseders-math-videos.py` **dry-run** to generate `math9-video-replacement-candidates.csv` and replacement summary instead of proposing to append new items. New upstream code/test push **run #11 `37826324720` passed**.
- StudyTracker has **29 current Math 9 video cards**, 28 linked quizzes. Of 29, 24 have thematic candidates and 5 have none. 207 candidate CSV rows; all remain subject to manual review.
- Downstream workflow `study-tracker/.github/workflows/import-liseders-playlist.yml` is renamed internally **Review and replace existing Math 9 videos**; git push is dry-run only; `workflow_dispatch(apply_replacements=true)` acts only on human-reviewed `replacements.json` approvals. Verified StudyTracker first replacement workflow run #`37826050373`: 10 tests + V2 catalog/CLI tests passed, no live content changes.
- Documentation: `docs/PLAYLIST_TO_STUDYTRACKER.md` and StudyTracker `docs/LISEDERS_PLAYLIST_IMPORT.md`.

## Next steps
1. Manually match each old video item to a new playlist video using actual lecture evidence; review existing quiz coverage and historical transcript references.
2. Save approvals in StudyTracker `content/v2/playlist-imports/ilyas-gunes-mat9.replacements.json` with old URL optimistic-lock, explicit review evidence and quiz review, then dry-run before explicitly applying.
3. Retain all existing VIDEO item IDs / lesson ordering / quiz content / student progress; do not claim new transcript verification while bot gate persists.
4. Changes committed to StudyTracker GitHub catalog do not automatically update live Cloudflare KV; a safe existing V2 seed/diff/apply and device check must follow publication.
5. Separate older work: repair `README.md`/`INDEX.md` local file links and historical Anki card counts.

## Known limitations
YouTube hosted runners require bot verification; no bypass is implemented, no fake captions are emitted. Playlist themes can include multiple curricular subtopics. Initial candidate suggestions are not verified lesson-level assignments.
