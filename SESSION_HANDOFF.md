# LiseDers — SESSION_HANDOFF

Updated: 2026-10-08. Aker work branch: `feature/aker-tyt-turkce-2027`; Math 9 parallel agent owns its own track.

## Non-negotiable correction
- **StudyTracker V2 is topic/subtopic paced, not weekly or semester paced.** The earlier 18-week Aker schedule is INVALID and must not be reused.
- Aker TYT Türkçe is NOT the 9th-grade Maarif Modeli TDE course. Match each actual transcript segment to exact TDE outcome only where evidence supports it; classify direct/partial/unmatched, preserve gaps.
- Proposed 11 modules are provisional organizational buckets, NOT verified transcript boundaries or an official syllabus. Video completion != topic mastery; quiz/check required. No student progress resets.

## Verified and existing
- User-provided Aker Kartal 2027 archive: 71 Turkish caption files; prior local processing reported 49,297 cues, normalized ZIP 214 entries. Local artifacts included `lesson_summaries_and_alignment.json`, `course_plan.json`, and reviews; these are **drafts**, not validated against live StudyTracker schema.
- Branch contains `data/video_playlists/aker-kartal-tyt-turkce-2027/README.md` and `.github/workflows/validate-aker-turkce.yml`. Draft PR #1. ZIP binary upload intentionally postponed by user; do not block topic alignment on upload.
- Maarif source in this repo: `curriculum/yillik_planlar/TDE_Yillik_Plan_AL9.md`; sample specific processes include TDE2.2.2 contextual vocabulary, TDE2.2.3 inference, TDE4.3.5 language structures, TDE4.3.7 spelling and TDE4.3.8 punctuation. Source is a secondary annual-plan compilation; do not assert official verification without checking primary source.

## Next actions
1. Read source captions per lesson and produce timecoded topic/subtopic summaries, with confidence and unsupported areas marked.
2. Map to exact TDE process components, distinguishing TYT-only grammar/test preparation from curricular outcomes; never auto-assign everything.
3. Inspect actual StudyTracker V2 catalog and progress storage/migration contract; produce topic-driven replacement payload with stable IDs and non-destructive migration plan.
4. Validate counts, references, coverage and sample assessments before merging. No production replacement or progress mutation yet.
