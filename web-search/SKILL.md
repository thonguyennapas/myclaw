---
name: web-search
description: "Tìm kiếm web bằng script search.py (KHÔNG dùng Brave Search). Chạy: python3 ~/.openclaw/skills/web-search/scripts/search.py 'query'. Hỗ trợ Tavily, DuckDuckGo, Google. KHÔNG cần Brave API key."
---

# Web Search — Tìm kiếm internet bằng search.py

> ⚠️ **QUAN TRỌNG**: KHÔNG sử dụng Brave Search. KHÔNG yêu cầu BRAVE_API_KEY.
> Skill này dùng script `search.py` có sẵn. Chỉ cần chạy lệnh bash bên dưới.

## Khi nào dùng
- Cần thông tin mới từ internet
- Nghiên cứu xu hướng, chính sách, tin tức
- Xác minh nhận định hoặc tìm nguồn

## Cách sử dụng — LUÔN chạy bằng bash

### Tìm kiếm cơ bản:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "từ khóa tìm kiếm"
```

### Tìm tiếng Việt:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "chính sách blockchain Việt Nam" --region vn-vi
```

### Tìm tin tức:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "NHNN blockchain" --type news --region vn-vi
```

### Tìm sâu (nếu có TAVILY_API_KEY):
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "CBDC 2025" --engine tavily --depth advanced
```

### Nhiều từ khóa cùng lúc:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py --batch "blockchain VN;CBDC;sandbox Đà Nẵng" --format md
```

### Đọc nội dung URL:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py --extract "https://example.com/article"
```

### Lưu kết quả:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "query" --output results.md --format md
```

## Tham số

| Tham số | Mô tả | Giá trị |
|---------|-------|---------|
| `--engine` | Engine | `auto` (mặc định), `tavily`, `ddg`, `google`, `multi` |
| `--type` | Loại | `text` (mặc định), `news` |
| `--region` | Vùng | `vn-vi` (Việt Nam), `wt-wt` (toàn cầu) |
| `--max` | Số kết quả | Mặc định: 10 |
| `--time` | Giới hạn | `d`=ngày, `w`=tuần, `m`=tháng, `y`=năm |
| `--format` | Output | `text`, `md`, `json` |

## Lưu ý
- Engine tự động: Tavily (nếu có key) → DuckDuckGo (miễn phí)
- Luôn dùng `--region vn-vi` khi tìm tiếng Việt
- KHÔNG BAO GIỜ yêu cầu Brave API key — skill này không dùng Brave
