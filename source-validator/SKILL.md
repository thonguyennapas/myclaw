---
name: source-validator
description: "Kiểm chứng độ tin cậy nguồn thông tin. Phân loại 5 tier, phát hiện thông tin bịa. Dùng khi cần validate dữ kiện trong báo cáo."
---

# Source Validator — Kiểm chứng nguồn

## Khi nào sử dụng
- Xác minh tính chính xác của nhận định
- Đánh giá độ tin cậy nguồn thông tin
- Cross-verify từ nhiều nguồn
- Phát hiện thông tin bịa/sai lệch

## Hệ thống 5 Tier

| Tier | Loại | Ví dụ | Ký hiệu |
|------|------|-------|---------|
| T1 🟢 | Chính thức | chinhphu.vn, sbv.gov.vn, bis.org | ✅ Verified |
| T2 🔵 | Tổ chức uy tín | World Bank, McKinsey, Gartner | ✅ Verified |
| T3 🟡 | Báo chí uy tín | VnExpress, Reuters, CoinDesk | ⚠️ Secondary |
| T4 🟠 | Nguồn phụ | Blog doanh nghiệp, whitepaper | ⚠️ Cần cross-ref |
| T5 🔴 | Không tin cậy | Social media, forum, marketing crypto | ❌ Loại bỏ |

## Quy trình validate

### Với mỗi dữ kiện, kiểm tra:
1. Nguồn có link hoạt động?
2. Thuộc Tier nào?
3. Ngày công bố/cập nhật?
4. Có cross-reference (≥2 nguồn)?
5. Phân biệt: fact vs opinion vs prediction?

### Khi không tìm thấy nguồn:
```
❌ SAI: "Việt Nam đã có sandbox blockchain"
✅ ĐÚNG: "Tính đến [ngày], không tìm thấy nguồn chính thức xác nhận."
```

### Để verify, dùng web-search:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "nhận định cần verify" --region vn-vi
python3 ~/.openclaw/skills/web-search/scripts/search.py --extract "https://link-can-kiem-tra.com"
```

## Red Flags — Dừng ngay khi gặp
🚩 Chỉ 1 nguồn cho claim lớn
🚩 Nguồn là marketing crypto
🚩 Số liệu không có methodology
🚩 "Theo nguồn tin", "được cho là" (anonymous)
🚩 Link 404 hoặc domain expired

## Output: Bảng chứng cứ nguồn

| # | Nhận định | Nguồn | Tier | Ngày | Trạng thái |
|---|----------|-------|------|------|------------|
| 1 | [dữ kiện] | [nguồn] | T1-T5 | [ngày] | ✅/⚠️/❌ |
