---
name: deep-research-orchestrator
description: "Điều phối nghiên cứu chuyên sâu: kết hợp web-search, source-validator, và blockchain-policy-research để chạy nghiên cứu tự động. Dùng khi cần nghiên cứu đầy đủ hoặc cập nhật báo cáo."
---

# Deep Research Orchestrator — Điều phối nghiên cứu

## Khi nào sử dụng
- Nghiên cứu mới từ đầu (full report)
- Cập nhật một phần báo cáo
- Deep-dive vào chủ đề con

## Quy trình tổng thể

```
web-search (tìm kiếm) → source-validator (kiểm chứng) → blockchain-policy-research (viết báo cáo)
```

### Phase 1: THU THẬP (dùng web-search)
```bash
# Xu hướng
python3 ~/.openclaw/skills/web-search/scripts/search.py --batch "blockchain trends 2025;CBDC global;RWA tokenization;DeFi enterprise" --format md --output ~/research/raw_trends.md

# Chính sách VN
python3 ~/.openclaw/skills/web-search/scripts/search.py --batch "blockchain Việt Nam chính sách;NHNN blockchain;sandbox fintech VN" --region vn-vi --format md --output ~/research/raw_policy.md

# Đà Nẵng
python3 ~/.openclaw/skills/web-search/scripts/search.py "Đà Nẵng blockchain sandbox thí điểm 2025 2026" --region vn-vi --max 15 --format md --output ~/research/raw_danang.md

# NAPAS / Thanh toán
python3 ~/.openclaw/skills/web-search/scripts/search.py --batch "blockchain interbank payment;NAPAS blockchain;đối soát blockchain" --format md --output ~/research/raw_napas.md
```

### Phase 2: KIỂM CHỨNG (dùng source-validator)
- Phân loại nguồn theo 5 tier
- Cross-check dữ kiện quan trọng (≥2 nguồn)
- Loại bỏ nguồn Tier 5
- Đánh dấu gaps (thiếu thông tin)

### Phase 3: VIẾT BÁO CÁO (dùng blockchain-policy-research)
Viết theo cấu trúc 5 phần: A (Xu hướng) → B (Chính sách) → C (Đà Nẵng) → D (NAPAS) → E (Summary)

### Phase 4: REVIEW
- Xóa nhận định không nguồn
- Verify links
- Format check

## Câu lệnh nhanh

| Yêu cầu | Thực hiện |
|----------|-----------|
| Nghiên cứu đầy đủ | Chạy Phase 1→4, tất cả sections |
| Chỉ xu hướng | Phase 1 (trends) → Phase 3 (Phần A) |
| Chỉ chính sách | Phase 1 (policy) → Phase 3 (Phần B) |
| Chỉ Đà Nẵng | Phase 1 (danang) → Phase 3 (Phần C) |
| Cập nhật | Chạy lại Phase 1 cho section cần update |

## Checklist cuối cùng
- [ ] Mọi nhận định có nguồn ≥ Tier 2
- [ ] Phân biệt blockchain tech vs crypto
- [ ] Đà Nẵng có kết luận CÓ/CHƯA CÓ
- [ ] ≥ 3 kịch bản NAPAS với KPI
- [ ] Executive Summary ≤ 2 trang
- [ ] Không có nhận định bịa
