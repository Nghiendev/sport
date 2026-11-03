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

Output: `sites/bjj/dist/` — có thể deploy lên GitHub Pages, Netlify, Vercel, Cloudflare Pages.
