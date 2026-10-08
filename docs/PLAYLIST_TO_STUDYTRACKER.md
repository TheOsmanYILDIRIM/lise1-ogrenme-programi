# Playlist → StudyTracker V2

Source: İlyas Güneş 9. sınıf Matematik, playlist `PLSYiXUktJiZeqUJyNFUgFHwOUNydbC-II`.

## Pipeline
The [GitHub Action](../.github/workflows/youtube-playlist.yml) checks out both repositories, runs offline regression tests, obtains the full playlist with yt-dlp, attempts Turkish human/auto VTT subtitles for **each** video, normalizes them into text/timecoded cues, and matches videos to the real StudyTracker mathematics V2 lessons and source topics. It runs the StudyTracker importer in dry-run mode; no live content is changed.

Artifacts: `playlist-catalog.json`, `raw-playlist.json`, `transcripts/manifest.json`, `transcripts/<videoid>.tr.txt`, `transcripts/<videoid>.tr.cues.json`, `studytracker-mapping.json`, `studytracker-import-dry-run.json`.

Caption statuses are fetched/missing/empty/error. **No unavailable transcript is invented.** Automated topic scores are review hints, not curriculum verification. Video media and full transcripts are not committed to Git.

## StudyTracker publishing
Download the Actions artifact; inspect titles, captions and proposed lesson matches. Place reviewed approvals in `study-tracker/content/v2/playlist-imports/ilyas-gunes-mat9.approvals.json`. Each approval requires `video_id`, `lesson_id`, `reviewed: true`, and written `reason`. `publish: false` is default; selecting another lesson requires `override: true`.

From the StudyTracker checkout run:
```bash
python scripts/import-liseders-playlist.py --mapping /path/to/studytracker-mapping.json --approvals content/v2/playlist-imports/ilyas-gunes-mat9.approvals.json
python scripts/import-liseders-playlist.py --mapping /path/to/studytracker-mapping.json --approvals content/v2/playlist-imports/ilyas-gunes-mat9.approvals.json --apply
node scripts/compile-v2-catalog.cjs
node scripts/generate-video-audit.cjs
```

New videos get stable item IDs and are appended to the approved existing lesson. Existing IDs, links, quizzes, progress, and quiz grounding are preserved. A new VIDEO does not automatically get a transcript-grounded QUIZ. Publishing to another repository requires explicit review and credentials, so the Action does not silently push to StudyTracker.
