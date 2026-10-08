#!/usr/bin/env python3
"""Safely import user-provided YTDLnis Turkish subtitles into a playlist catalog.

Accepts a ZIP or local directory. Matches by video ID when present in filenames,
otherwise by *playlist index plus verified normalized title*. Never associates a
generic index alone with a video and never fabricates transcripts.

Source: official YTDLnis command template exports .tr.vtt/.tr.srt files.
This importer makes no network requests and does not update StudyTracker.
"""
import argparse
import hashlib
import json
import re
import unicodedata
import zipfile
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path, PurePosixPath

from playlist_transcripts import normalize_vtt

VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")
CAPTION = re.compile(r"(?i)\.(vtt|srt)$")
LANG_SUFFIX = re.compile(r"(?i)\.tr(?:[-_][a-z0-9-]+)?$")
INDEX_TITLE = re.compile(r"^(\d{1,4})\s*[-–]\s*(.+)$")
MAX_FILES = 1000
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_TOTAL_BYTES = 100 * 1024 * 1024


def normalize_title(text):
    txt = str(text or "").replace("ı", "i").replace("İ", "I")
    txt = "".join(
        char for char in unicodedata.normalize("NFKD", txt)
        if not unicodedata.combining(char)
    )
    return " ".join(re.findall(r"[a-z0-9]+", txt.casefold()))


def candidate_files(source):
    """Yield (original_name, bytes) without extracting ZIP members to disk."""
    source = Path(source)
    if not source.exists():
        raise FileNotFoundError(source)
    count = 0
    total = 0
    if source.is_file() and source.suffix.lower() == ".zip":
        with zipfile.ZipFile(source, "r") as archive:
            for item in archive.infolist():
                if item.is_dir() or not CAPTION.search(item.filename):
                    continue
                pure = PurePosixPath(item.filename.replace("\\", "/"))
                if pure.is_absolute() or ".." in pure.parts or ":" in pure.parts[0]:
                    raise ValueError(f"Unsafe ZIP member name: {item.filename}")
                count += 1
                total += item.file_size
                if count > MAX_FILES or item.file_size > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                    raise ValueError("Subtitle ZIP exceeds safe file count or size limits")
                yield item.filename, archive.read(item)
    elif source.is_dir():
        for path in sorted(source.rglob("*")):
            if path.is_symlink() or not path.is_file() or not CAPTION.search(path.name):
                continue
            count += 1
            size = path.stat().st_size
            total += size
            if count > MAX_FILES or size > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                raise ValueError("Subtitle folder exceeds safe file count or size limits")
            yield str(path.relative_to(source)), path.read_bytes()
    else:
        raise ValueError("Input must be a ZIP archive or directory")


def match_name(name, videos_by_id, videos_by_position):
    basename = Path(name.replace("\\", "/")).name
    suffix = CAPTION.search(basename)
    if not suffix:
        return None, "unsupported file extension", None
    # yt-dlp adds the language code before subtitle extension automatically.
    base = basename[:suffix.start()]
    lang = LANG_SUFFIX.search(base)
    if not lang:
        return None, "subtitle is not explicitly tagged Turkish (.tr.vtt/.tr.srt)", None
    base = base[:lang.start()]
    explicit = [
        vid for vid in videos_by_id
        if re.search(r"(?:^|[\s()\[\]-])" + re.escape(vid) + r"(?=$|[\s()\[\]-])", base)
    ]
    if len(explicit) > 1:
        return None, "multiple possible video IDs in filename", None
    if len(explicit) == 1:
        return explicit[0], "video_id", 1.0
    m = INDEX_TITLE.match(base)
    if not m:
        return None, "no video ID and no playlist index/title", None
    index, filename_title = int(m.group(1)), m.group(2)
    target = videos_by_position.get(index)
    if target is None:
        return None, f"playlist index {index} is not in catalog", None
    expected = normalize_title(target["title"])
    observed = normalize_title(filename_title)
    score = SequenceMatcher(None, observed, expected).ratio() if expected and observed else 0.0
    if score < 0.88:
        return None, f"playlist index {index} title mismatch (similarity {score:.2f})", score
    return target["id"], "index_and_verified_title", round(score, 4)


def load_catalog(path):
    catalog = json.loads(Path(path).read_text(encoding="utf-8"))
    videos = catalog.get("videos")
    if not isinstance(videos, list) or not videos:
        raise ValueError("Playlist catalog missing videos")
    by_id, by_position = {}, {}
    for video in videos:
        vid = str(video.get("id") or "")
        pos = video.get("position")
        if not VIDEO_ID.fullmatch(vid) or vid in by_id:
            raise ValueError(f"Invalid or duplicate video ID in catalog: {vid}")
        if not isinstance(pos, int) or pos < 1 or pos in by_position:
            raise ValueError(f"Invalid or duplicate playlist index for video {vid}")
        if not video.get("title"):
            raise ValueError(f"Missing video title for {vid}")
        by_id[vid] = video
        by_position[pos] = video
    return catalog, by_id, by_position


def import_subtitles(catalog_path, source_path, output_path):
    catalog, by_id, by_position = load_catalog(catalog_path)
    output = Path(output_path)
    seen = defaultdict(list)
    unmatched = []
    invalid = []
    files_seen = 0
    for name, raw in candidate_files(source_path):
        files_seen += 1
        vid, match_method, score = match_name(name, by_id, by_position)
        if not vid:
            unmatched.append({"file": name, "reason": match_method})
            continue
        try:
            decoded = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            invalid.append({"file": name, "id": vid, "reason": "invalid UTF-8 subtitle"})
            continue
        cues = normalize_vtt(decoded)
        if not cues:
            invalid.append({"file": name, "id": vid, "reason": "no valid timed subtitle cues"})
            continue
        seen[vid].append({
            "file": name, "matching": match_method, "title_similarity": score,
            "raw": raw, "cues": cues, "ext": Path(name).suffix.lower()
        })
    subtitle_dir = output / "transcripts"
    subtitle_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for position, video in sorted(by_position.items()):
        vid = video["id"]
        candidates = seen.get(vid, [])
        if len(candidates) != 1:
            status = "missing" if not candidates else "duplicate"
            records.append({
                "id": vid, "position": position, "status": status,
                "source_files": [entry["file"] for entry in candidates]
            })
            continue
        entry = candidates[0]
        text = "\n".join(cue["text"] for cue in entry["cues"]).strip()
        if not text:
            records.append({"id": vid, "position": position, "status": "empty"})
            continue
        hash16 = hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
        raw_ext = entry["ext"]
        (subtitle_dir / (vid + ".tr" + raw_ext)).write_bytes(entry["raw"])
        (subtitle_dir / (vid + ".tr.txt")).write_text(text + "\n", encoding="utf-8")
        (subtitle_dir / (vid + ".tr.cues.json")).write_text(
            json.dumps({"id": vid, "cues": entry["cues"]}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8"
        )
        records.append({
            "id": vid, "position": position, "status": "fetched",
            "source": "YTDLnis_user_export", "source_file": entry["file"],
            "matching_method": entry["matching"], "title_similarity": entry["title_similarity"],
            "language": "tr", "cue_count": len(entry["cues"]), "fingerprint": hash16,
            "raw_sha256": hashlib.sha256(entry["raw"]).hexdigest()
        })
    counts = Counter(x["status"] for x in records)
    manifest = {
        "schema_version": 1,
        "playlist_id": catalog.get("playlist_id"),
        "source": "YTDLnis_user_export",
        "total_videos": len(records), "files_seen": files_seen,
        "status_counts": {key: counts.get(key, 0) for key in ("fetched", "missing", "duplicate", "empty")},
        "unmatched_files": unmatched, "invalid_files": invalid,
        "videos": records,
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", required=True, help="LiseDers playlist-catalog.json")
    p.add_argument("--input", required=True, help="YTDLnis export folder or ZIP")
    p.add_argument("--output", required=True, help="Output directory, outside tracked content")
    args = p.parse_args()
    result = import_subtitles(args.catalog, args.input, args.output)
    print(json.dumps({
        "playlist_id": result["playlist_id"], "files_seen": result["files_seen"],
        "counts": result["status_counts"],
        "unmatched": len(result["unmatched_files"]),
        "invalid": len(result["invalid_files"])
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
