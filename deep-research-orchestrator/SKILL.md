---
name: deep-research-orchestrator
description: "Điều phối nghiên cứu chuyên sâu bằng script search.py (KHÔNG dùng Brave Search). Chạy python3 ~/.openclaw/skills/web-search/scripts/search.py để tìm dữ liệu, rồi viết báo cáo."
---

# Deep Research Orchestrator — Điều phối nghiên cứu

> ⚠️ **QUAN TRỌNG**: KHÔNG sử dụng Brave Search. KHÔNG yêu cầu BRAVE_API_KEY.
> Sử dụng script `search.py` để tìm kiếm. Chỉ cần chạy lệnh bash bên dưới.

## Khi nào sử dụng
- Nghiên cứu mới từ đầu (full report)
- Cập nhật một phần báo cáo
- Deep-dive vào chủ đề con

## Quy trình tổng thể

```
search.py (tìm kiếm) → source-validator (kiểm chứng) → viết báo cáo 5 phần
```

### Phase 1: THU THẬP — chạy search.py qua bash
```bash
# Xu hướng blockchain
python3 ~/.openclaw/skills/web-search/scripts/search.py --batch "blockchain trends 2025;CBDC global;RWA tokenization;DeFi enterprise" --format md --output /tmp/research/raw_trends.md

# Chính sách Việt Nam
python3 ~/.openclaw/skills/web-search/scripts/search.py --batch "blockchain Việt Nam chính sách;NHNN blockchain;sandbox fintech VN" --region vn-vi --format md --output /tmp/research/raw_policy.md

# Đà Nẵng sandbox
python3 ~/.openclaw/skills/web-search/scripts/search.py "Đà Nẵng blockchain sandbox thí điểm 2025 2026" --region vn-vi --max 15 --format md --output /tmp/research/raw_danang.md

# NAPAS & Thanh toán
python3 ~/.openclaw/skills/web-search/scripts/search.py --batch "blockchain interbank payment;NAPAS Vietnam;đối soát blockchain" --format md --output /tmp/research/raw_napas.md
```

### Phase 2: KIỂM CHỨNG (source-validator)
- Phân loại nguồn theo 5 tier
- Cross-check dữ kiện quan trọng (≥2 nguồn)
- Loại bỏ nguồn Tier 5 (social media, marketing)
- Đánh dấu gaps (thiếu thông tin)

### Phase 3: VIẾT BÁO CÁO 5 PHẦN
**A — Xu hướng:** Bảng xu hướng (Tên | Mô tả | Mức trưởng thành | Nguồn)
**B — Chính sách VN:** Bảng văn bản (Tên | Số hiệu | Ngày | Cơ quan | Link)
**C — Đà Nẵng:** Kết luận CÓ/CHƯA CÓ sandbox (kèm chứng cứ nguồn)
**D — Vai trò NAPAS:** 3 kịch bản (low/medium/high risk + KPI + lộ trình)
**E — Executive Summary:** 1-2 trang tóm tắt + đề xuất hành động

### Phase 4: REVIEW
- Xóa nhận định không nguồn → ghi "⚠️ Không tìm thấy nguồn"
- Verify links hoạt động
- Đảm bảo format Markdown chuẩn

## Checklist cuối cùng
- [ ] Mọi nhận định có nguồn ≥ Tier 2
- [ ] Phân biệt blockchain tech vs crypto
- [ ] Đà Nẵng có kết luận CÓ/CHƯA CÓ
- [ ] ≥ 3 kịch bản NAPAS với KPI
- [ ] Executive Summary ≤ 2 trang
- [ ] Không có nhận định bịa
