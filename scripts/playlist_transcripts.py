#!/usr/bin/env python3
"""Fetch Turkish YouTube captions for a yt-dlp playlist catalog.

No video downloads, generated speech, cookies, or fabricated captions. Each video
has an explicit fetched/missing/error/blocked status. Captions stay in workflow artifacts.
"""
import argparse
import hashlib
import html
import json
import re
import subprocess
import time
from pathlib import Path

VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
TIMING = re.compile(r"(?P<start>(?:\d{2}:)?\d{2}:\d{2}[.,]\d{3})\s+-->\s+")
TAG = re.compile(r"<[^>]*>")

def normalize_vtt(source):
    """Return timestamped, adjacent-deduplicated cues, preserving spoken content."""
    text = source.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff")
    results = []
    for block in re.split(r"\n\s*\n", text):
        lines = block.strip().splitlines()
        index = next((i for i, line in enumerate(lines) if TIMING.search(line)), None)
        if index is None:
            continue
        match = TIMING.search(lines[index])
        spoken = " ".join(
            html.unescape(TAG.sub("", x)).replace("\u200b", "").strip()
            for x in lines[index + 1:] if x.strip()
        )
        spoken = re.sub(r"\s+", " ", spoken).strip()
        if spoken and (not results or spoken != results[-1]["text"]):
            results.append({"start": match.group("start").replace(",", "."), "text": spoken})
    return results

def collect(catalog, output, max_videos=200, delay=0.3, timeout=90):
    output.mkdir(parents=True, exist_ok=True)
    videos = catalog.get("videos")
    if not isinstance(videos, list) or not videos:
        raise ValueError("Playlist catalog has no videos")
    if len(videos) > max_videos:
        raise ValueError(f"Playlist has {len(videos)} videos; max allowed {max_videos}")
    details = []
    consecutive_bot_blocks = 0
    for video in videos:
        video_id = str(video.get("id") or "")
        if not VIDEO_ID.fullmatch(video_id):
            raise ValueError(f"Invalid YouTube video id: {video_id!r}")
        if consecutive_bot_blocks >= 2:
            details.append({"id": video_id, "status": "blocked",
                            "reason": "GitHub runner rejected by YouTube bot verification; not attempted"})
            continue
        template = str(output / (video_id + ".%(language)s.%(ext)s"))
        args = [
            "yt-dlp", "--skip-download", "--write-subs", "--write-auto-subs",
            "--sub-langs", "tr,tr-*", "--sub-format", "vtt",
            "--no-playlist", "--no-warnings", "--socket-timeout", "15",
            "--retries", "1", "--extractor-retries", "1",
            "--output", template, "--",
            f"https://www.youtube.com/watch?v={video_id}",
        ]
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
            files = list(output.glob(video_id + ".*.vtt"))
            files.sort(key=lambda p: (
                0 if p.name.endswith(".tr.vtt") else 1,
                len(p.name), p.name
            ))
            if not files:
                status = "missing" if result.returncode == 0 else "error"
                error_text = (result.stderr or result.stdout)
                if "sign in to confirm" in error_text.lower() and "not a bot" in error_text.lower():
                    consecutive_bot_blocks += 1
                    reason = "YouTube requests sign-in/bot verification for this runner"
                else:
                    consecutive_bot_blocks = 0
                    reason = "No accessible Turkish captions" if status == "missing" else error_text[-350:].strip()
                details.append({"id": video_id, "status": status, "reason": reason})
                print(f"{video_id}: {status} ({reason[:70]})", flush=True)
                continue
            consecutive_bot_blocks = 0
            cues = normalize_vtt(files[0].read_text(encoding="utf-8-sig"))
            if not cues:
                details.append({"id": video_id, "status": "empty", "language": "tr"})
                print(f"{video_id}: empty", flush=True)
                continue
            plain = "\n".join(cue["text"] for cue in cues)
            fingerprint = hashlib.sha256(plain.encode("utf-8")).hexdigest()[:16]
            (output / f"{video_id}.tr.txt").write_text(plain + "\n", encoding="utf-8")
            (output / f"{video_id}.tr.cues.json").write_text(
                json.dumps({"id": video_id, "cues": cues}, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            details.append({"id": video_id, "status": "fetched", "language": "tr",
                            "fingerprint": fingerprint, "cue_count": len(cues),
                            "source_file": files[0].name})
            print(f"{video_id}: fetched ({len(cues)} cues)", flush=True)
        except (subprocess.TimeoutExpired, OSError) as exc:
            details.append({"id": video_id, "status": "error", "reason": type(exc).__name__})
            print(f"{video_id}: error ({type(exc).__name__})", flush=True)
        time.sleep(max(0, delay))
    counts = {status: sum(1 for d in details if d["status"] == status)
              for status in ("fetched", "missing", "empty", "error", "blocked")}
    manifest = {"schema_version": 1, "playlist_id": catalog.get("playlist_id"),
                "video_count": len(videos), "status_counts": counts, "videos": details,
                "bot_verification_blocked": consecutive_bot_blocks >= 2}
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--max-videos", type=int, default=200)
    p.add_argument("--delay", type=float, default=0.3)
    args = p.parse_args()
    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    manifest = collect(catalog, Path(args.output), args.max_videos, args.delay)
    print(json.dumps(manifest["status_counts"], ensure_ascii=False))

if __name__ == "__main__":
    main()
