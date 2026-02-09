---
name: deep-research-orchestrator
description: "Skill điều phối nghiên cứu chuyên sâu: kết hợp web-research-aggregator, source-validator, và blockchain-policy-research để thực hiện nghiên cứu tự động từ đầu đến cuối. Sử dụng khi cần chạy nghiên cứu đầy đủ hoặc cập nhật báo cáo."
---

# Deep Research Orchestrator

## Mô tả
Skill điều phối (orchestrator) quản lý toàn bộ quy trình nghiên cứu blockchain, từ thu thập dữ liệu, kiểm chứng nguồn, đến xuất báo cáo hoàn chỉnh. Kết nối 3 skill chuyên biệt:

```
┌─────────────────────────────────────────────────┐
│           DEEP RESEARCH ORCHESTRATOR            │
│                                                 │
│  ┌──────────────┐  ┌──────────────┐            │
│  │ Web Research  │→│   Source      │            │
│  │ Aggregator    │  │   Validator   │            │
│  └──────┬───────┘  └──────┬───────┘            │
│         │                  │                    │
│         ▼                  ▼                    │
│  ┌─────────────────────────────────┐            │
│  │   Blockchain Policy Research    │            │
│  │   (Report Generator)           │            │
│  └─────────────┬───────────────────┘            │
│                │                                │
│                ▼                                │
│  ┌─────────────────────────────────┐            │
│  │         OUTPUT                  │            │
│  │  ├── report.md                  │            │
│  │  ├── executive-summary.md       │            │
│  │  ├── trend-map.md               │            │
│  │  ├── policy-matrix.md           │            │
│  │  ├── danang-sandbox.md          │            │
│  │  ├── napas-roadmap.md           │            │
│  │  └── sources.md                 │            │
│  └─────────────────────────────────┘            │
└─────────────────────────────────────────────────┘
```

## Khi nào sử dụng
- **Nghiên cứu mới**: Chạy toàn bộ quy trình từ đầu
- **Cập nhật**: Refresh một phần cụ thể của báo cáo
- **Xác minh**: Kiểm tra lại nguồn và dữ kiện
- **Mở rộng**: Nghiên cứu deep-dive vào một chủ đề con

## Quy trình Tổng thể

### Phase 1: KHỞI ĐỘNG (5 phút)
```
BƯỚC 1: Xác nhận phạm vi nghiên cứu
├── Nghiên cứu đầy đủ? (A+B+C+D+E)
├── Chỉ một phần? (chọn section)
├── Cập nhật? (section nào?)
└── Deep-dive? (chủ đề nào?)

BƯỚC 2: Kiểm tra output directory
├── Tạo thư mục reports/ nếu chưa có
├── Backup báo cáo cũ nếu có
└── Setup logging
```

### Phase 2: THU THẬP DỮ LIỆU (20-40 phút)
```
BƯỚC 3: Sử dụng web-research-aggregator
├── Chạy tìm kiếm theo nhóm từ khóa
│   ├── Nhóm "trends" (VN + EN)
│   ├── Nhóm "policy" (VN + EN)
│   ├── Nhóm "danang" (VN + EN)
│   └── Nhóm "napas_role" (VN + EN)
├── Thu thập ≥ 30 nguồn
├── Phân loại theo tier
└── Lưu raw results

Chiến lược tìm kiếm:
1. Bắt đầu từ nguồn Tier 1 (chính phủ)
2. Mở rộng sang Tier 2 (tổ chức quốc tế)
3. Bổ sung Tier 3 (báo chí) cho context
4. Cross-reference tất cả
```

### Phase 3: KIỂM CHỨNG (10-20 phút)
```
BƯỚC 4: Sử dụng source-validator
├── Validate tất cả nguồn Tier 1
├── Cross-check Tier 2-3
├── Đánh dấu & loại bỏ Tier 5
├── Tạo bảng chứng cứ nguồn
└── Đánh dấu "gaps" (thiếu thông tin)
```

### Phase 4: PHÂN TÍCH & VIẾT (30-60 phút)
```
BƯỚC 5: Sử dụng blockchain-policy-research
├── Section A: Tổng hợp xu hướng → trend-map.md
│   ├── Bản đồ 5-10 xu hướng lớn
│   ├── Kiến trúc & tiêu chuẩn
│   └── Pain points
│
├── Section B: Chính sách VN → policy-matrix.md
│   ├── Bảng văn bản/chỉ đạo (có nguồn)
│   └── Phân biệt blockchain tech vs crypto
│
├── Section C: Đà Nẵng → danang-sandbox.md
│   ├── Kết luận CÓ/CHƯA CÓ (có chứng cứ)
│   └── Thông tin gần nhất
│
├── Section D: Vai trò NAPAS → napas-roadmap.md
│   ├── 5 vai trò khả thi
│   └── 3-5 kịch bản (low/medium/high risk)
│
└── Section E: Executive Summary → executive-summary.md
    ├── Kết luận chính
    ├── Cơ hội
    └── Next steps
```

### Phase 5: REVIEW & HOÀN THIỆN (10 phút)
```
BƯỚC 6: Quality check
├── Đọc lại toàn bộ báo cáo
├── Xóa nhận định không có nguồn
├── Kiểm tra consistency giữa các phần
├── Verify links
├── Format check (markdown tables, headings)
└── Tạo report.md (consolidated)

BƯỚC 7: Tổng hợp nguồn → sources.md
├── Tất cả nguồn đã sử dụng
├── Tier & reliability rating
└── Ngày truy cập
```

## Câu lệnh Điều phối

### Chạy nghiên cứu đầy đủ:
```
/research full
```
Equivalent: Chạy Phase 1→5, tất cả sections.

### Chạy một phần:
```
/research section:trends      # Chỉ xu hướng
/research section:policy      # Chỉ chính sách VN
/research section:danang      # Chỉ Đà Nẵng sandbox
/research section:napas       # Chỉ vai trò NAPAS
/research section:summary     # Chỉ Executive Summary
```

### Cập nhật:
```
/research update:policy       # Cập nhật chính sách mới
/research update:trends       # Cập nhật xu hướng
/research refresh             # Chạy lại tất cả
```

### Kiểm tra:
```
/research validate            # Kiểm chứng lại nguồn
/research gaps                # Liệt kê thông tin còn thiếu
/research status              # Trạng thái nghiên cứu hiện tại
```

## Checklist Chất lượng Cuối cùng

Trước khi giao báo cáo, đảm bảo:

```
✅ Quality Checklist:
□ Tất cả nhận định quan trọng có nguồn ≥ Tier 2
□ Bảng văn bản VN có đủ: Tên, Số, Ngày, Cơ quan, Link
□ Phân biệt rõ blockchain tech vs crypto
□ Đà Nẵng có kết luận rõ CÓ/CHƯA CÓ
□ ≥ 3 kịch bản với đầy đủ: lợi ích, rủi ro, pháp lý, KPI
□ Executive Summary ≤ 2 trang
□ Không có nhận định bịa/không nguồn
□ Ngôn ngữ: Tiếng Việt, thuật ngữ kỹ thuật giữ English
□ Format Markdown chuẩn, tables render OK
□ Tất cả links hoạt động
```

## Lưu ý cho Agent

1. **Luôn bắt đầu** bằng việc đọc SKILL.md của blockchain-policy-research
2. **Tìm kiếm web** là bắt buộc - không dựa vào training data cũ
3. **Ghi rõ** nếu không tìm thấy nguồn cho bất kỳ nhận định nào
4. **Ưu tiên format** theo template trong blockchain-policy-research
5. **Ngày hiện tại** luôn kiểm tra để đảm bảo dữ liệu mới nhất
6. **Cross-reference** mọi dữ kiện quan trọng với ≥ 2 nguồn
