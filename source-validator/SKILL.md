---
name: source-validator
description: "Kiểm chứng nguồn 5 tier. Verify bằng lệnh bash python3 script. TUYỆT ĐỐI KHÔNG gọi tool web_search hay Brave Search."
---

# Source Validator — Kiểm chứng nguồn

> 🚨 **TUYỆT ĐỐI KHÔNG** gọi tool web_search, Brave Search, hay built-in search.
> 🚨 Verify bằng lệnh bash: `python3 ~/.openclaw/skills/web-search/scripts/search.py`

## Khi nào sử dụng
- Xác minh tính chính xác của mọi nhận định trong báo cáo
- Đánh giá độ tin cậy nguồn thông tin
- Cross-verify dữ kiện quan trọng (≥ 2 nguồn)
- Phát hiện thông tin bịa/sai lệch

## Hệ thống 5 Tier

| Tier | Loại | Ví dụ | Ký hiệu |
|------|------|-------|---------|
| T1 🟢 | Chính thức | chinhphu.vn, sbv.gov.vn, mic.gov.vn, thuvienphapluat.vn, Cổng TTĐT bộ/ngành | ✅ Verified |
| T2 🔵 | Tổ chức QT uy tín | BIS, World Bank, IMF, WEF, ISO, ITU, W3C | ✅ Verified |
| T3 🟡 | Báo chí/Nghiên cứu | VnExpress, Tuổi Trẻ, Reuters, CoinDesk, Gartner, McKinsey | ⚠️ Secondary |
| T4 🟠 | Nguồn phụ | Blog doanh nghiệp, whitepaper, báo cáo công ty tư vấn | ⚠️ Cần cross-ref |
| T5 🔴 | Không tin cậy | Social media, forum, blog cá nhân, marketing crypto | ❌ LOẠI BỎ |

## Quy trình validate

### Với mỗi dữ kiện quan trọng:
1. Nguồn có link hoạt động không?
2. Thuộc Tier nào? (T1-T2: dùng được, T3-T4: cần cross-ref, T5: loại)
3. Ngày công bố/cập nhật?
4. Có cross-reference (≥ 2 nguồn độc lập)?
5. Phân biệt: fact vs opinion vs prediction?

### Khi không tìm thấy nguồn:
```
❌ SAI: "Việt Nam đã có sandbox blockchain tại Đà Nẵng"
✅ ĐÚNG: "Tính đến [ngày], không tìm thấy nguồn chính thức xác nhận sandbox blockchain tại Đà Nẵng đã được cấp phép."
```

### Verify bằng web search:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "nhận định cần verify" --region vn-vi --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py --extract "https://link-can-kiem-tra.com"
```

## Red Flags — Phải ghi cảnh báo khi gặp
🚩 Chỉ 1 nguồn cho claim lớn (cần ≥ 2)
🚩 Nguồn là marketing crypto hoặc project shilling
🚩 Số liệu không có methodology/nguồn gốc
🚩 "Theo nguồn tin", "được cho là" (anonymous)
🚩 Link 404 hoặc domain expired
🚩 Nhập nhằng blockchain tech vs crypto

## Output: Bảng chứng cứ nguồn (đưa vào Phụ lục báo cáo)

| # | Nhận định | Nguồn | Tier | Ngày | Cross-ref | Trạng thái |
|---|----------|-------|------|------|-----------|------------|
| 1 | [dữ kiện] | [tên nguồn + link] | T1-T5 | [ngày] | [có/không] | ✅/⚠️/❌ |
