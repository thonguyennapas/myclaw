---
name: deep-research
description: "Nghiên cứu chuyên sâu Blockchain/Chính sách VN. Tra cứu bằng lệnh bash python3 script. TUYỆT ĐỐI KHÔNG gọi tool web_search hay Brave Search."
---

# 📊 Deep Research — Nghiên cứu Blockchain & Chính sách VN

> 🚨 **TUYỆT ĐỐI KHÔNG** gọi tool web_search, Brave Search, hay built-in search.
> 🚨 Tra cứu bằng lệnh bash: `python3 ~/.openclaw/skills/web-search/scripts/search.py`
> 📄 Ghi TOÀN BỘ vào **1 file duy nhất**: `~/research/report-YYYYMMDD.md`

## MỤC TIÊU

Báo cáo nghiên cứu 4 nhóm:

| Phần | Nội dung |
|------|----------|
| **A** | Bản đồ xu hướng Blockchain (thế giới + VN) |
| **B** | Chính sách & văn bản pháp lý Việt Nam |
| **C** | Đà Nẵng Sandbox / Thí điểm |
| **D** | Vai trò tham gia của NAPAS |

---

## QUY TRÌNH

### Bước 1: Chuẩn bị
```bash
mkdir -p ~/research
```

### Bước 2: Tra cứu (CHẠY LỆNH BASH)

**Xu hướng thế giới:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "blockchain enterprise trends 2025 2026" --max 15
python3 ~/.openclaw/skills/web-search/scripts/search.py "CBDC global status 2025 central bank digital currency" --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "tokenization real world assets RWA 2025" --max 10
```

**Việt Nam:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "xu hướng blockchain Việt Nam 2024 2025" --region vn-vi --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "chính sách blockchain Việt Nam quyết định nghị quyết" --region vn-vi --max 15
python3 ~/.openclaw/skills/web-search/scripts/search.py "NHNN blockchain DLT fintech sandbox" --region vn-vi --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "nghị định tài sản ảo tiền mã hóa Việt Nam" --region vn-vi --max 10
```

**Đà Nẵng:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "Đà Nẵng blockchain sandbox thí điểm đề án" --region vn-vi --max 15
```

**NAPAS:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "blockchain interbank payment settlement reconciliation" --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "NAPAS blockchain thanh toán liên ngân hàng" --region vn-vi --max 10
```

### Bước 3: Đọc chi tiết nguồn quan trọng
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py --extract "https://url-quan-trong.com"
```

### Bước 4: Kiểm chứng nguồn (5 Tier)

| Tier | Loại | Ví dụ | Ký hiệu |
|------|------|-------|---------|
| T1 🟢 | Chính thức | chinhphu.vn, sbv.gov.vn, mic.gov.vn | ✅ Verified |
| T2 🔵 | Tổ chức QT | BIS, World Bank, IMF, WEF | ✅ Verified |
| T3 🟡 | Báo chí | VnExpress, Reuters, CoinDesk | ⚠️ Secondary |
| T4 🟠 | Nguồn phụ | Blog DN, whitepaper | ⚠️ Cần cross-ref |
| T5 🔴 | Không tin cậy | Social media, blog cá nhân | ❌ LOẠI BỎ |

- Cross-check ≥ 2 nguồn cho mỗi dữ kiện quan trọng
- Không có nguồn → "⚠️ Không tìm thấy nguồn chính thức"
- Phân biệt rõ: fact vs opinion vs prediction

### Bước 5: Viết báo cáo → ghi 1 file

**Cấu trúc bắt buộc:**

- **PHẦN 0: Executive Summary** — Kết luận + Top 3 cơ hội + Lộ trình 30-60-90
- **PHẦN A: Xu hướng Blockchain** — Bảng 5-10 xu hướng (mô tả, mảng, mức trưởng thành, nguồn)
- **PHẦN B: Chính sách VN** — Bảng văn bản (số/ký hiệu, ngày, cơ quan, nội dung, link)
- **PHẦN C: Đà Nẵng Sandbox** — Kết luận rõ: CÓ hay CHƯA CÓ + bảng chứng cứ
- **PHẦN D: Vai trò NAPAS** — 3-5 kịch bản (thấp/trung/cao rủi ro) + lộ trình 30-60-90
- **PHỤ LỤC** — Danh sách nguồn + Tier + ngày truy cập

```bash
cat > ~/research/report-$(date +%Y%m%d).md << 'EOF'
[TOÀN BỘ: Executive Summary + Phần A + B + C + D + Phụ lục nguồn]
EOF
```

### Bước 6: Trả Telegram
1. Tóm tắt ngắn (< 3000 ký tự)
2. "📄 Báo cáo đầy đủ: ~/research/report-YYYYMMDD.md"
3. Hỏi user xem phần nào chi tiết

## QUY TẮC VÀNG
1. **KHÔNG bịa** — Mọi dữ kiện phải kèm nguồn (link)
2. Phân biệt rõ: blockchain công nghệ vs tài sản số/tiền mã hóa
3. Ưu tiên nguồn: chinhphu.vn, sbv.gov.vn, mic.gov.vn, bis.org, worldbank.org
4. LOẠI BỎ: social media, blog cá nhân, marketing crypto
