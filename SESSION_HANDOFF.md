# LiseDers — SESSION_HANDOFF

Updated: 2026-10-08 · `main`

## Current state
- MEB 9th-grade TYMM educational source repository; StudyTracker owns V2 catalog and all student attempts/progress. User had changed direction to rebuild Mathematics 9 from scratch, then explicitly STOPPED that work. **Do not resume rebuilding without a fresh instruction.** Previous replacement-only approach is superseded by that later user request, but remains in GitHub history.
- Playlist: `PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II`, 60 video metadata records, mixed İlyas Güneş and Nurtaç Kozak. Data: `data/video_playlists/<id>/{playlist-catalog.json,topic-matches.json,transcript-status.json}`.
- Topic matching from titles only is NOT verified exact content; never fabricate captions or transcript-grounded quizzes.

## 2026-10-08 yt-dlp diagnosis & actual live test
- Original Actions command `pip install 'yt-dlp>=2025.1.0'` installed **2026.08.19 stable** (confirmed GitHub job logs). It was missing `[default]` EJS dependency installation and Deno setup.
- Updated `.github/workflows/youtube-playlist.yml` to `pip install --upgrade --pre 'yt-dlp[default]'` and `denoland/setup-deno@v2`; outputs yt-dlp / yt-dlp-ejs / Deno versions and flags zero accessible subtitles.
- Added `.github/workflows/yt-dlp-diagnostics.yml`: one-video Turkish caption probe, read-only; GitHub Actions [run #37828581593](https://github.com/TheOsmanYILDIRIM/lise1-ogrenme-programi/actions/runs/37828581593) **failed due to YouTube access**, not package installation. Artifact ID `11572666734` contains full `probe.log`.
- Probe log independently confirms **yt-dlp nightly@2026.09.27.232945**, **yt_dlp_ejs 0.8.0**, **Deno 2.9.7**; JavaScript Challenge provider `deno` active.
- Despite all prerequisites, YouTube player responses were `LOGIN_REQUIRED` and extractor emitted `Sign in to confirm you're not a bot`. Do NOT claim installation fixed extraction or that GitHub IP restriction is conclusively the only cause.
- Full 60-video transcript extraction was **not** re-run with nightly; a targeted one-video test showed the access restriction persists. Previous 60-video run reported 0 subtitles, 2 errors and 58 unattempted due to circuit breaker.

## Next steps
1. Obtain captions from a user-authorized accessible source or user-supplied files; do not attempt stealth bot-verification bypass or claim transcription without evidence.
2. If the YouTube environment becomes accessible, re-run **one-video diagnostic** before processing the full playlist. Prefer versioned, bounded retries with status logging.
3. Only after a separate user instruction, resume requested Mathematics 9 rebuild with verified video-to-curriculum mapping and protected student records. Work must not silently reset old progress.

## Older unrelated work
- `README.md`/`INDEX.md` contain nonportable device-local links and historical Anki count conflicts; independent audit remains open.
