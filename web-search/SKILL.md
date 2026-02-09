---
name: web-search
description: "Tìm kiếm web đa engine cho deep research. Hỗ trợ: Tavily (AI-optimized, tốt nhất), DuckDuckGo (miễn phí), Google Custom Search. Tự động chọn engine tốt nhất. BẮT BUỘC sử dụng khi cần tìm thông tin mới từ internet."
---

# Web Search Skill — Đa Engine cho Deep Research

## Mô tả
Skill tìm kiếm web hỗ trợ 3 engine, tự động chọn tốt nhất:

| Engine | Chất lượng | API Key? | Miễn phí |
|--------|-----------|---------|---------|
| 🥇 **Tavily** | Tốt nhất cho AI | Cần (đăng ký 30s) | 1000 req/tháng free |
| 🥈 **DuckDuckGo** | Tốt | Không cần | Hoàn toàn free |
| 🥉 **Google** | Tốt nhất tiếng Việt | Cần | 100 req/ngày free |

## Khi nào BẮT BUỘC sử dụng
- **LUÔN LUÔN** khi cần thông tin mới/cập nhật
- Khi nghiên cứu xu hướng, chính sách, tin tức
- Khi cần xác minh nhận định
- Khi cần tìm nguồn chính thức cho báo cáo
- Khi người dùng hỏi về sự kiện gần đây

## Cài đặt

### Bắt buộc:
```bash
pip install duckduckgo-search
```

### Khuyến nghị (để có chất lượng tốt nhất):
```bash
# Đăng ký Tavily (miễn phí, 30 giây): https://app.tavily.com/sign-in
# Sau đó set biến môi trường:
export TAVILY_API_KEY="tvly-xxxxxxxxxxxxxxxx"
```

## Cách sử dụng

### Tìm kiếm tự động (auto-chọn engine tốt nhất):
```bash
python3 scripts/search.py "blockchain Vietnam policy 2025"
```

### Chỉ định engine:
```bash
python3 scripts/search.py "CBDC 2025" --engine tavily              # Tavily (tốt nhất)
python3 scripts/search.py "blockchain" --engine ddg                 # DuckDuckGo (free)
python3 scripts/search.py "chính sách blockchain" --engine google   # Google
python3 scripts/search.py "blockchain" --engine multi               # TẤT CẢ engines
```

### Tìm kiếm tiếng Việt:
```bash
python3 scripts/search.py "chính sách blockchain Việt Nam" --region vn-vi
```

### Deep search (Tavily only):
```bash
python3 scripts/search.py "CBDC global progress" --engine tavily --depth advanced
```

### Tìm tin tức:
```bash
python3 scripts/search.py "NHNN blockchain" --type news --region vn-vi
```

### Batch search (nhiều từ khóa):
```bash
python3 scripts/search.py --batch "blockchain VN;CBDC;Da Nang sandbox" --format md
```

### Đọc nội dung trang web:
```bash
python3 scripts/search.py --extract "https://chinhphu.vn/some-article"
```

### Kiểm tra engines sẵn sàng:
```bash
python3 scripts/search.py --status
```

### Lưu kết quả:
```bash
python3 scripts/search.py "query" --output results.md --format md
python3 scripts/search.py "query" --output results.json --format json
```

## Tham số đầy đủ

| Tham số | Mô tả | Giá trị |
|---------|-------|---------|
| `query` | Từ khóa tìm | Bất kỳ text |
| `--engine` | Engine | `auto`, `tavily`, `ddg`, `google`, `multi` |
| `--type` | Loại tìm | `text` (mặc định), `news` |
| `--region` | Vùng | `vn-vi` (Việt), `wt-wt` (toàn cầu) |
| `--max` | Số kết quả | Mặc định: 10 |
| `--time` | Giới hạn | `d`=ngày, `w`=tuần, `m`=tháng, `y`=năm |
| `--depth` | Độ sâu (Tavily) | `basic`, `advanced` |
| `--batch` | Nhiều keyword | Phân cách bằng `;` |
| `--extract` | Đọc URL | URL cần đọc |
| `--output` | Lưu file | Path file |
| `--format` | Định dạng | `text`, `md`, `json` |
| `--status` | Check engines | Không cần giá trị |

## Biến môi trường

```bash
# Tavily (khuyến nghị, free 1000 req/tháng)
export TAVILY_API_KEY="tvly-xxxxxxxx"

# Google (optional, free 100 req/ngày)  
export GOOGLE_API_KEY="AIzaSy-xxxxxxxx"
export GOOGLE_CX="xxxxxxxxxx"
```

## Quy trình Deep Research

```
BƯỚC 1: Tìm kiếm (web-search)
  python3 search.py "từ khóa" --engine auto --max 15

BƯỚC 2: Đọc chi tiết (web-search --extract)
  python3 search.py --extract "https://url-quan-trong.com"

BƯỚC 3: Kiểm chứng (source-validator)
  Phân loại nguồn theo tier, cross-check

BƯỚC 4: Tổng hợp (blockchain-policy-research)
  Viết báo cáo theo framework 5 phần
```

## Lưu ý
1. **Auto mode** tự chọn engine tốt nhất (Tavily → DuckDuckGo)
2. **Multi mode** tìm trên tất cả engines, deduplicate kết quả
3. **Tavily advanced** chậm hơn nhưng kết quả sâu hơn
4. Rate limiting: không gửi quá nhanh, có auto-retry
5. Kết quả tiếng Việt: dùng `--region vn-vi`
