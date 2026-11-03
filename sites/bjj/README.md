# MATMAP — Bản đồ kỹ năng BJJ

Trang web tương tác cho Brazilian Jiu-Jitsu: sơ đồ chuyển vị trí, chuỗi tấn công móc nối kỹ năng, và video YouTube nhúng.

## Chạy local

```bash
cd sites/bjj
npm install
npm run dev
```

Mở http://localhost:5173

## Cập nhật dữ liệu kỹ năng

Từ thư mục markdown `sport/bjj/ky-nang/`:

```bash
python scripts/extract_bjj_skills.py
```

(hoặc từ `sites/bjj`: `npm run extract`)

## Build production

```bash
npm run build
npm run preview
```

Output: `sites/bjj/dist/`

## GitHub Pages

Repo này deploy tự động qua Actions (`.github/workflows/deploy-matmap.yml`).

1. GitHub → **Settings → Pages**
2. **Source:** GitHub Actions
3. Push lên `master` (hoặc chạy workflow thủ công)

URL: **https://Nghiendev.github.io/sport/**

> Vite dùng `base: '/sport/'` vì đây là project Pages của repo `sport`.
