"""Normalize section_link anchors in skills_catalog.json."""
import json
from pathlib import Path

ROOT = Path(__file__).parent
CATALOG_PATH = ROOT / "skills_catalog.json"

ALIASES = {
    "6-combinations-tổ-hợp": "6-combinations",
    "7-counter-phản-công": "7-counter-punching",
    "8-distance-chiến-thuật": "8-distance-strategy",
    "10-training-luyện-tập": "10-training",
    "11-rules-luật": "11-rules",
    "12-mental-tâm-lý": "12-mental",
    "13-levels-cấp-độ": "13-levels",
}

skills = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
updated = 0
for skill in skills:
    anchor = skill["section_link"].split("#")[-1]
    if anchor in ALIASES:
        new_anchor = ALIASES[anchor]
        skill["section_link"] = f"../TAT-CA-KY-NANG-BOXING.md#{new_anchor}"
        updated += 1

CATALOG_PATH.write_text(json.dumps(skills, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Updated {updated} section_link entries")
