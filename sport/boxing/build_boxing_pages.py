"""Generate boxing ky-nang detail pages from skills catalog."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parent
KY_NANG = ROOT / "ky-nang"
CATALOG = ROOT / "skills_catalog.json"


def render_page(skill: dict) -> str:
    section_link = skill.get("section_link", "../TAT-CA-KY-NANG-BOXING.md")
    level = skill.get("level", "⭐")
    tags = skill.get("tags", "")
    defense = skill.get("defense", "").strip()
    defense_block = defense if defense else "*(Không có counter riêng — tập trung distance, feint và không mở hàng sau khi đấm.)*"
    defense_row = skill.get("video_defense")
    defense_video = f"| **Phòng thủ / counter** | [📺 {defense_row['title']}]({defense_row['url']}) |" if defense_row else "| **Phòng thủ / counter** | *Không có* |"
    sources = skill.get("sources", [])
    sources_block = ""
    if sources:
        sources_block = "*Nguồn:*\n" + "\n".join(f"- {s}" for s in sources)
    extra = skill.get("extra_links", [])
    extra_text = " · ".join(f"[{e['title']}]({e['url']})" for e in extra) if extra else ""

    return f"""# {skill['name_vi']}

> **Tiếng Anh:** {skill['name_en']} · [← Quay lại bách khoa]({section_link}) · {level} · {tags}

---

## Phân tích tình huống

{skill['situation']}

---

## Cách phòng thủ / hóa giải

{defense_block}

---

## Video

| Loại | Video |
|------|-------|
| **Tấn công / thực hiện** | [📺 {skill['video_attack']['title']}]({skill['video_attack']['url']}) |
{defense_video}

---

{("**Bổ sung:** " + extra_text + "\\n\\n") if extra_text else ""}{sources_block}
"""


def main() -> None:
    skills: list[dict] = json.loads(CATALOG.read_text(encoding="utf-8"))
    KY_NANG.mkdir(exist_ok=True)
    for skill in skills:
        path = KY_NANG / f"{skill['slug']}.md"
        path.write_text(render_page(skill), encoding="utf-8")
    print(f"Generated {len(skills)} pages in {KY_NANG}")


if __name__ == "__main__":
    main()
