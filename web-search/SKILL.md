---
name: web-search
description: "Tìm kiếm web thực sự bằng script Python. BẮT BUỘC sử dụng khi cần thông tin mới từ internet. Hỗ trợ Tavily, DuckDuckGo, Google."
---

# Web Search — Tìm kiếm internet thực sự

## Khi nào BẮT BUỘC dùng
- Cần thông tin mới/cập nhật từ internet
- Nghiên cứu xu hướng, chính sách, tin tức
- Xác minh nhận định hoặc tìm nguồn chính thức
- Người dùng hỏi về sự kiện gần đây

## Cách sử dụng

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

### Tìm sâu (Tavily):
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "CBDC 2025" --engine tavily --depth advanced
```

### Nhiều từ khóa:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py --batch "blockchain VN;CBDC;sandbox Đà Nẵng" --format md
```

### Đọc nội dung URL:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py --extract "https://chinhphu.vn/bai-viet"
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
| `--status` | Check engines | Không cần giá trị |

## Lưu ý
- Auto mode tự chọn engine tốt nhất: Tavily → DuckDuckGo
- Luôn dùng `--region vn-vi` khi tìm tiếng Việt
- Dùng `--format md` khi cần output đẹp cho báo cáo
