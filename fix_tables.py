"""Fix table formatting and re-apply YouTube links from cache."""
import json
import re
from pathlib import Path

from build_videos import HEADER_FIX, ROW_MAP, link

CACHE = Path(__file__).parent / "video_cache.json"
MD = Path(__file__).parent / "TAT-CA-KY-NANG-BJJ.md"


def strip_videos(text: str) -> str:
    text = re.sub(r"\s*\[📺[^\]]+\]\([^)]+\)", "", text)
    text = re.sub(r"\s*— \[📺[^\]]+\]\([^)]+\)", "", text)
    text = re.sub(r"\| 📺 Video \|", "", text)
    text = re.sub(r"\|---\|", "", text)  # remove duplicate sep fragments
    # normalize broken separators like |-----||---|
    text = re.sub(r"\|(-+\|)+\n", lambda m: "|" + "|".join(["---"] * (m.group(0).count("|") - 1)) + "|\n", text)
    return text


def fix_headers(text: str) -> str:
    for old, new in HEADER_FIX.items():
        text = text.replace(old + "\n", new + "\n")
    text = text.replace(
        "| Kỹ năng | Tiếng Anh | Mô tả | Mức |\n",
        "| Kỹ năng | Tiếng Anh | Mô tả | Mức | 📺 Video |\n",
    )
    text = text.replace(
        "|---------|-----------|-------|-----|\n",
        "|---------|-----------|-------|-----|----------|\n",
    )
    return text


def add_video_column_to_separators(text: str) -> str:
    lines = text.splitlines()
    out = []
    for i, line in enumerate(lines):
        if line.strip().startswith("|---") and "📺 Video" in (lines[i - 1] if i else ""):
            cols = line.count("|") - 1
            if cols >= 3 and not line.rstrip().endswith("---|") or line.count("---") < cols:
                out.append("|" + "|".join(["---"] * cols) + "|")
                continue
        out.append(line)
    return "\n".join(out) + "\n"


def apply_links(text: str, cache: dict) -> str:
    key_to_link = {}
    for k, v in cache.items():
        key_to_link[k] = link(v.get("id") or "", v["title"], v.get("search"))

    lines = text.splitlines(keepends=True)
    out = []
    for line in lines:
        if line.strip().startswith("|---"):
            out.append(line)
            continue
        for frag, key in ROW_MAP:
            if frag in line and key in key_to_link and "📺" not in line:
                vl = key_to_link[key]
                if line.strip().startswith("|"):
                    parts = [p.strip() for p in line.strip().strip("|").split("|")]
                    parts.append(vl)
                    line = "| " + " | ".join(parts) + " |\n"
                elif line.strip().startswith("- [ ]"):
                    line = line.rstrip() + f" — {vl}\n"
                break
        # rear mount steps
        if any(line.strip().startswith(f"| {n} |") for n in range(1, 5)) and "Hand fight" in line or "Clear hooks" in line or "Turn in" in line or "Scoot hips" in line:
            if "📺" not in line and "back_escape" in key_to_link:
                parts = [p.strip() for p in line.strip().strip("|").split("|")]
                if len(parts) == 2:
                    parts.append(key_to_link["back_escape"])
                    line = "| " + " | ".join(parts) + " |\n"
        out.append(line)
    return "".join(out)


def main():
    cache = json.loads(CACHE.read_text(encoding="utf-8"))
    text = MD.read_text(encoding="utf-8")
    text = strip_videos(text)
    text = fix_headers(text)
    text = apply_links(text, cache)
    if "Mỗi kỹ năng có link **📺 YouTube**" not in text:
        text = text.replace(
            "- Ký hiệu mức độ: ⭐ Sơ cấp | ⭐⭐ Trung cấp | ⭐⭐⭐ Nâng cao",
            "- Ký hiệu mức độ: ⭐ Sơ cấp | ⭐⭐ Trung cấp | ⭐⭐⭐ Nâng cao\n- Mỗi kỹ năng có link **📺 YouTube** (1 video tutorial)",
        )
    MD.write_text(text, encoding="utf-8")
    count = text.count("📺")
    print(f"Fixed. {count} video links in {MD}")


if __name__ == "__main__":
    main()
