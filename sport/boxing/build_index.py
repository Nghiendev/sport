"""Generate TAT-CA-KY-NANG-BOXING.md index from skills_catalog.json."""
import json
import re
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).parent
CATALOG = json.loads((ROOT / "skills_catalog.json").read_text(encoding="utf-8"))

# Canonical section keys (must match markdown header anchors)
SECTIONS = OrderedDict([
    ("3-solo", ("3", "Solo & nền tảng", "Kỹ năng vận động và thế đấm — luyện mỗi ngày.")),
    ("4-đấm-punches", ("4", "Đấm (Punches)", "Bốn đòn cơ bản và biến thể.")),
    ("5-phòng-thủ-defense", ("5", "Phòng thủ (Defense)", "Block, slip, parry, roll, pull.")),
    ("6-combinations", ("6", "Combinations", "Chuỗi đấm có hệ thống.")),
    ("7-counter-punching", ("7", "Counter-punching", "Phản công sau nhử hoặc né.")),
    ("8-distance-strategy", ("8", "Khoảng cách & chiến thuật", "Range, ring craft, phong cách.")),
    ("9-clinch", ("9", "Clinch & inside fighting", "Tầm gần và tie-up.")),
    ("10-training", ("10", "Huấn luyện & dụng cụ", "Bag, mitt, sparring, conditioning.")),
    ("11-rules", ("11", "Thi đấu & luật", "Amateur rules, scoring, prep.")),
    ("12-mental", ("12", "Tinh thần & chiến lược", "Game plan, mindset, journal.")),
    ("13-levels", ("13", "Ma trận theo trình độ", "Beginner → advanced checklist.")),
])

# Legacy / alternate anchors in skills_catalog.json → canonical key
ANCHOR_ALIASES = {
    "6-combinations-tổ-hợp": "6-combinations",
    "7-counter-phản-công": "7-counter-punching",
    "8-distance-chiến-thuật": "8-distance-strategy",
    "10-training-luyện-tập": "10-training",
    "11-rules-luật": "11-rules",
    "12-mental-tâm-lý": "12-mental",
    "13-levels-cấp-độ": "13-levels",
}


def normalize_anchor(anchor: str) -> str:
    if anchor in ANCHOR_ALIASES:
        return ANCHOR_ALIASES[anchor]
    if anchor in SECTIONS:
        return anchor
    # fallback: match "N-" prefix to section number
    m = re.match(r"^(\d+)-", anchor)
    if m:
        num = m.group(1)
        for key in SECTIONS:
            if key.startswith(f"{num}-"):
                return key
    return anchor


def short_description(skill: dict) -> str:
    if skill.get("description_short"):
        return skill["description_short"].replace("|", "/")
    text = skill["situation"].replace("\n", " ").strip()
    # first sentence
    for end in [". ", " — ", " – "]:
        idx = text.find(end)
        if 40 < idx < 160:
            return text[: idx + 1].replace("|", "/")
    return (text[:120] + "…") if len(text) > 120 else text.replace("|", "/")


by_section: dict[str, list] = {k: [] for k in SECTIONS}
orphans: list = []

for skill in CATALOG:
    anchor = skill["section_link"].split("#")[-1]
    key = normalize_anchor(anchor)
    if key in by_section:
        by_section[key].append(skill)
    else:
        orphans.append((skill, anchor))

if orphans:
    print(f"Warning: {len(orphans)} skills with unmapped anchors:")
    for s, a in orphans[:5]:
        print(f"  - {s['slug']}: {a}")

lines = [
    "# Bách Khoa Toàn Bộ Kỹ Năng Boxing",
    "",
    "> Tài liệu tra cứu bổ sung cho [HUONG-DAN-BOXING.md](./HUONG-DAN-BOXING.md).",
    "> Tổng hợp từ kiến thức quyền anh Olympic/amateur, [Precision Striking](https://www.precisionstriking.com/), [Expert Boxing](https://expertboxing.com/), [USA Boxing](https://www.usaboxing.org/).",
    "",
    "---",
    "",
    "## Mục lục",
    "",
    "1. [Cách dùng tài liệu này](#1-cách-dùng-tài-liệu-này)",
    "2. [Bản đồ nhóm kỹ năng](#2-bản-đồ-nhóm-kỹ-năng)",
]

for key, (num, title, _) in SECTIONS.items():
    lines.append(f"{num}. [{title}](#{num}-{key.split('-', 1)[-1]})")

lines += [
    "14. [YouTube & nguồn học](#14-youtube--nguồn-học)",
    "",
    "---",
    "",
    "## 1. Cách dùng tài liệu này",
    "",
    "| File | Mục đích |",
    "|---|---|",
    "| `HUONG-DAN-BOXING.md` | Khung tư duy, lộ trình 12 tuần |",
    "| `TAT-CA-KY-NANG-BOXING.md` (file này) | Tra cứu — tên, mô tả, mức, link chi tiết |",
    "| `ky-nang/*.md` | Phân tích tình huống, phòng thủ, video |",
    "| `SO-DO-CHUYEN-DOI.md` | Chuỗi tấn công & chuyển range |",
    "",
    "**Quy tắc học:**",
    "- Không cần thuộc hết ~97 kỹ năng — chọn **2–3 mỗi nhóm**, luyện sâu",
    "- ⭐ Sơ cấp | ⭐⭐ Trung cấp | ⭐⭐⭐ Nâng cao",
    "",
    "---",
    "",
    "## 2. Bản đồ nhóm kỹ năng",
    "",
    "```",
    "  SOLO (stance, footwork, shadow)",
    "           ↓",
    "  PUNCHES ←→ DEFENSE",
    "           ↓",
    "  COMBINATIONS → COUNTER",
    "           ↓",
    "  DISTANCE / RING CRAFT → CLINCH",
    "           ↓",
    "  TRAINING + RULES + MENTAL",
    "```",
    "",
]

for key, (num, title, desc) in SECTIONS.items():
    skills = by_section.get(key, [])
    lines += [f"## {num}. {title}", "", f"*{desc}*", ""]
    if num == "13":
        lines += ["| Checklist | Mô tả | Mức | Chi tiết |", "|---|---|---|---|"]
    else:
        lines += ["| Kỹ năng | Mô tả ngắn | Mức | Chi tiết |", "|---|---|---|---|"]
    for s in skills:
        desc_short = short_description(s)
        lines.append(
            f"| {s['name_vi']} | {desc_short} | {s['level']} | [→ Chi tiết](./ky-nang/{s['slug']}.md) |"
        )
    lines += ["", "---", ""]

lines += [
    "## 14. YouTube & nguồn học",
    "",
    "| Kênh / Site | Link |",
    "|---|---|",
    "| Tony Jeffries | https://www.youtube.com/@TonyJeffries |",
    "| Precision Striking | https://www.youtube.com/@PrecisionStriking |",
    "| FightTips | https://www.youtube.com/@fighttips |",
    "| Expert Boxing | https://expertboxing.com/ |",
    "| Coach Anthony | https://www.youtube.com/@CoachAnthony |",
    "| Boxing Life | https://www.youtube.com/@BoxingLife |",
    "| USA Boxing | https://www.usaboxing.org/ |",
    "",
    f"*Tổng số kỹ năng: **{len(CATALOG)}** — sinh từ `skills_catalog.json`.*",
]

(ROOT / "TAT-CA-KY-NANG-BOXING.md").write_text("\n".join(lines), encoding="utf-8")

# Summary per section
for key in SECTIONS:
    print(f"{key}: {len(by_section[key])} skills", flush=True)
print("Wrote TAT-CA-KY-NANG-BOXING.md", flush=True)
