"""Extract BJJ skill pages into sites/bjj/src/data/skills.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KY_NANG = ROOT / "sport" / "bjj" / "ky-nang"
OUT = ROOT / "sites" / "bjj" / "src" / "data" / "skills.json"

YT = re.compile(
    r"\[([^\]]+)\]\((https://www\.youtube\.com/watch\?v=([A-Za-z0-9_-]{6,}))\)"
)
TITLE = re.compile(r"^#\s+(.+)$", re.M)
EN = re.compile(r"\*\*Tiếng Anh:\*\*\s*(.+?)(?:\s*[·|]|\s*$)", re.M)
LEVEL = re.compile(r"(⭐+)")
SIT = re.compile(r"## Phân tích tình huống\s*\n+([\s\S]*?)(?=\n---|\n## )")
VID = re.compile(r"## Video\s*\n+([\s\S]*?)(?=\n---|\n## |\Z)")


def main() -> None:
    skills = []
    for path in sorted(KY_NANG.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        title_m = TITLE.search(text)
        name = title_m.group(1).strip() if title_m else path.stem
        en_m = EN.search(text)
        name_en = en_m.group(1).strip() if en_m else ""
        level_m = LEVEL.search(text[:400])
        level = level_m.group(1) if level_m else ""
        sit_m = SIT.search(text)
        situation = (sit_m.group(1).strip() if sit_m else "")
        summary = situation.split("\n\n")[0][:320] if situation else ""

        videos = []
        vs = VID.search(text)
        if vs:
            for line in vs.group(1).split("\n"):
                if "youtube.com" not in line:
                    continue
                kind = "attack"
                lower = line.lower()
                if "phòng thủ" in line.lower() or "escape" in lower or "counter" in lower:
                    kind = "defense"
                m = YT.search(line)
                if m:
                    videos.append(
                        {
                            "kind": kind,
                            "title": m.group(1).replace("📺 ", "").strip(),
                            "videoId": m.group(3),
                            "url": m.group(2),
                        }
                    )
        for m in YT.finditer(text):
            vid = m.group(3)
            if any(v["videoId"] == vid for v in videos):
                continue
            videos.append(
                {
                    "kind": "extra",
                    "title": m.group(1).replace("📺 ", "").strip(),
                    "videoId": vid,
                    "url": m.group(2),
                }
            )

        skills.append(
            {
                "id": path.stem,
                "name": name,
                "nameEn": name_en,
                "level": level,
                "summary": summary,
                "videos": videos,
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(skills, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(skills)} skills → {OUT}")


if __name__ == "__main__":
    main()
