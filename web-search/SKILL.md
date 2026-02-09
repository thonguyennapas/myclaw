---
name: web-search
description: "Script Python tra cứu thông tin từ internet. CHẠY BẰNG LỆNH BASH python3, TUYỆT ĐỐI KHÔNG gọi tool web_search hay Brave Search."
---

# Tra cứu thông tin bằng script search.py

> 🚨 **TUYỆT ĐỐI KHÔNG** gọi tool web_search, Brave Search, hay built-in search.
> 🚨 **LUÔN LUÔN** chạy bằng **lệnh bash** như bên dưới.
> ✅ Script này KHÔNG cần Brave API key. Nó dùng Tavily hoặc DuckDuckGo.

## Cách dùng — CHẠY LỆNH BASH

### Tra cứu cơ bản:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "từ khóa"
```

### Tra cứu tiếng Việt:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "chính sách blockchain Việt Nam" --region vn-vi
```

### Tra cứu tin tức:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "NHNN blockchain" --type news --region vn-vi
```

### Tra cứu nhiều từ khóa:
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

| Tham số | Giá trị |
|---------|---------|
| `--engine` | `auto` (mặc định), `tavily`, `ddg`, `google`, `multi` |
| `--type` | `text` (mặc định), `news` |
| `--region` | `vn-vi` (Việt Nam), `wt-wt` (toàn cầu) |
| `--max` | Số kết quả, mặc định 10 |
| `--time` | `d`=ngày, `w`=tuần, `m`=tháng, `y`=năm |
| `--format` | `text`, `md`, `json` |

## Lưu ý quan trọng
- Script tự chọn engine: Tavily (nếu có key) → DuckDuckGo (miễn phí)
- KHÔNG CẦN Brave API key, KHÔNG CẦN cấu hình thêm gì
- Dùng `--region vn-vi` khi tra cứu tiếng Việt
