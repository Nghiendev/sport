# MMA Language

Từ điển song ngữ Việt–Anh cho võ thuật tổng hợp, lấy cảm hứng từ
[FIFA Football Language](https://www.fifatrainingcentre.com/en/resources-tools/football-language/index.php).

## Chạy local

```bash
cd sites/mma-language
npm install
npm run dev
```

http://localhost:5174

## Dữ liệu

- `src/data/terms.json` — 311 mục từ
- `src/data/sources.json` — nguồn tham khảo

Cập nhật từ CSV:

```bash
# từ thư mục repo root
python -c "..."  # hoặc dùng lại script parse CSV trong mma-dictionary/
```

## Deploy

Vite `base` = `/sport/mma-language/` → URL dự kiến:

https://nghiendev.github.io/sport/mma-language/
