---
name: blockchain-policy-research
description: "Nghiên cứu xu hướng Blockchain và chính sách Việt Nam. Tạo báo cáo có trích nguồn, chống bịa. Dùng web-search để tìm dữ liệu thực."
---

# Blockchain Policy Research

## Khi nào sử dụng
- Nghiên cứu xu hướng blockchain toàn cầu và Việt Nam
- Tổng hợp chính sách/văn bản pháp lý blockchain VN
- Đánh giá sandbox Đà Nẵng
- Đề xuất vai trò tham gia cho NAPAS
- Báo cáo nghiên cứu có trích nguồn

## Quy tắc VÀNG
1. **KHÔNG ĐƯỢC bịa** — Mọi dữ kiện phải có nguồn dẫn link
2. Không tìm thấy nguồn → ghi: "⚠️ Không tìm thấy nguồn chính thức"
3. Phân biệt: blockchain công nghệ vs tài sản số/crypto

## Quy trình thực hiện

### Bước 1: Tìm kiếm web (BẮT BUỘC)
```bash
# Tìm xu hướng
python3 ~/.openclaw/skills/web-search/scripts/search.py "blockchain trends 2025 2026" --max 15
python3 ~/.openclaw/skills/web-search/scripts/search.py "xu hướng blockchain 2025" --region vn-vi --max 10

# Tìm chính sách VN
python3 ~/.openclaw/skills/web-search/scripts/search.py "chính sách blockchain Việt Nam site:chinhphu.vn" --region vn-vi
python3 ~/.openclaw/skills/web-search/scripts/search.py "NHNN blockchain DLT quyết định" --region vn-vi

# Đà Nẵng sandbox
python3 ~/.openclaw/skills/web-search/scripts/search.py "Đà Nẵng sandbox blockchain thí điểm" --region vn-vi

# CBDC
python3 ~/.openclaw/skills/web-search/scripts/search.py "CBDC Vietnam digital currency 2025" --max 10
```

### Bước 2: Đọc chi tiết nguồn quan trọng
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py --extract "https://url-quan-trong.com"
```

### Bước 3: Viết báo cáo theo cấu trúc 5 phần

**Phần A — Xu hướng:** Bản đồ 5-10 xu hướng lớn (bảng: Xu hướng | Mô tả | Mức trưởng thành | Tác động | Nguồn)

**Phần B — Chính sách VN:** Bảng văn bản (Tên | Số/Ký hiệu | Ngày | Cơ quan | Nội dung | Link)

**Phần C — Đà Nẵng:** Kết luận CÓ/CHƯA CÓ sandbox (kèm chứng cứ nguồn)

**Phần D — Vai trò NAPAS:** 3-5 kịch bản (Mô tả | Rủi ro | KPI | Lộ trình 30-60-90 ngày)

**Phần E — Executive Summary:** 1-2 trang tóm tắt + đề xuất hành động

### Bước 4: Kiểm tra chất lượng
- Xóa nhận định không có nguồn
- Kiểm tra phân biệt blockchain tech vs crypto
- Đảm bảo format Markdown chuẩn

## Chi tiết templates
Xem file `templates/report-templates.md` để biết format chi tiết cho mỗi phần.

## Nguồn ưu tiên
- chinhphu.vn, sbv.gov.vn, mic.gov.vn, thuvienphapluat.vn
- bis.org, worldbank.org, imf.org, weforum.org
- Gartner, McKinsey, Deloitte reports
