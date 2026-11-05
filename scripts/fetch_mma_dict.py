"""Download all sheets from the public MMA dictionary Google Spreadsheet."""
from __future__ import annotations

import csv
import json
import re
import urllib.request
from pathlib import Path

SHEET_ID = "1wfJASrTYRlO896kUSKZzkgdY6G77sDOhfjNvTtVLUNI"
OUT_DIR = Path(__file__).resolve().parents[1] / "mma-dictionary"


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def discover_sheets() -> list[tuple[str, str]]:
    html = get(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/htmlview").decode(
        "utf-8", "replace"
    )
    # Patterns seen in Google Sheets HTML
    pairs: dict[str, str] = {}
    for gid, name in re.findall(r'gid=(\d+)[^>]*>\s*([^<]{1,80})\s*<', html):
        pairs[gid] = name.strip()
    for m in re.finditer(r'"(\d{5,})"\s*,\s*"([^"]{1,80})"', html):
        pairs.setdefault(m.group(1), m.group(2))
    for m in re.finditer(r'\[null,(\d+)\][^\[]{0,40}\["([^"]+)"', html):
        pairs.setdefault(m.group(1), m.group(2))
    # Always include default gid 0
    pairs.setdefault("0", "Sheet1")
    # Fallback: dump all gids found
    for gid in re.findall(r"gid[=\\:](\d+)", html):
        pairs.setdefault(gid, f"sheet_{gid}")
    return sorted(pairs.items(), key=lambda x: int(x[0]))


def download_csv(gid: str) -> str:
    url = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export"
        f"?format=csv&gid={gid}"
    )
    return get(url).decode("utf-8-sig")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sheets = discover_sheets()
    print(f"Discovered {len(sheets)} candidate sheets")
    saved = []
    for gid, name in sheets:
        safe = re.sub(r"[^\w\-]+", "_", name).strip("_") or f"sheet_{gid}"
        try:
            text = download_csv(gid)
        except Exception as e:  # noqa: BLE001
            print(f"skip gid={gid} name={name}: {e}")
            continue
        if not text.strip():
            print(f"empty gid={gid} name={name}")
            continue
        path = OUT_DIR / f"{safe}__gid{gid}.csv"
        path.write_text(text, encoding="utf-8")
        rows = list(csv.reader(text.splitlines()))
        saved.append({"gid": gid, "name": name, "file": path.name, "rows": len(rows)})
        print(f"saved {path.name} rows={len(rows)}")

    (OUT_DIR / "index.json").write_text(
        json.dumps(saved, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Done → {OUT_DIR}")


if __name__ == "__main__":
    main()
