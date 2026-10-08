#!/usr/bin/env python3
"""Convert yt-dlp flat playlist JSON into a stable learning catalog."""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

def convert(raw, source):
    entries = raw.get("entries") or []
    videos = []
    for position, entry in enumerate(entries, 1):
        if not isinstance(entry, dict) or not entry.get("id"):
            continue
        vid = str(entry["id"])
        videos.append({
            "position": position,
            "id": vid,
            "title": entry.get("title") or "",
            "url": f"https://www.youtube.com/watch?v={vid}",
            "duration_seconds": entry.get("duration"),
            "channel": entry.get("channel") or entry.get("uploader"),
        })
    if not videos:
        raise ValueError("No videos returned; playlist may be unavailable or blocked")
    return {
        "schema_version": 1,
        "source_url": source,
        "playlist_id": raw.get("id"),
        "playlist_title": raw.get("title"),
        "video_count": len(videos),
        "videos": videos,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--source", required=True)
    args = parser.parse_args()
    raw = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = convert(raw, args.source)
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {result['video_count']} videos to {target}")

if __name__ == "__main__":
    main()
