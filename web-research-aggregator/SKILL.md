---
name: web-research-aggregator
description: "Thu thập dữ liệu từ nhiều nguồn web bằng python3 ~/.openclaw/skills/web-search/scripts/search.py (KHÔNG dùng Brave Search). Đa ngôn ngữ Việt/Anh."
---

# Web Research Aggregator — Thu thập dữ liệu nghiên cứu

> ⚠️ Tìm kiếm web bằng: `python3 ~/.openclaw/skills/web-search/scripts/search.py`. KHÔNG dùng Brave Search.

## Khi nào sử dụng
- Cần thu thập thông tin từ nhiều nguồn cho một chủ đề
- Cần tìm kiếm đa ngôn ngữ (Việt + Anh)
- Cần kiểm chứng chéo (cross-verify)
- Cần tổng hợp kết quả thành báo cáo có cấu trúc

## Quy trình

### Bước 1: Chạy batch search đa ngôn ngữ
```bash
# Tiếng Việt
python3 ~/.openclaw/skills/web-search/scripts/search.py --batch "chính sách blockchain Việt Nam;NHNN blockchain;Đà Nẵng sandbox" --region vn-vi --format md --output research_vi.md

# Tiếng Anh
python3 ~/.openclaw/skills/web-search/scripts/search.py --batch "blockchain Vietnam policy;CBDC Southeast Asia;blockchain enterprise 2025" --format md --output research_en.md
```

### Bước 2: Đọc chi tiết nguồn quan trọng
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py --extract "https://url-quan-trong.com"
```

### Bước 3: Phân loại theo Tier (nguồn ưu tiên)
```
Tier 1: .gov.vn → chinhphu.vn, sbv.gov.vn, mic.gov.vn, danang.gov.vn
Tier 2: Tổ chức QT → bis.org, worldbank.org, imf.org
Tier 3: Pháp luật → thuvienphapluat.vn, luatvietnam.vn
Tier 4: Báo chí → vnexpress.net, tuoitre.vn, ledgerinsights.com
Tier 5: Nghiên cứu → scholar.google.com, arxiv.org
```

### Bước 4: Cross-verify
- Mỗi dữ kiện quan trọng cần ≥ 2 nguồn
- Nếu chỉ 1 nguồn → đánh dấu "cần kiểm chứng thêm"
- Nếu mâu thuẫn → ghi nhận cả hai, ưu tiên Tier cao hơn

### Bước 5: Output
```markdown
## Kết quả: [Chủ đề]
- Số nguồn: [N] | Hữu ích: [M] | Tin cậy: [Cao/TB/Thấp]

### Phát hiện chính
1. [Phát hiện] — Nguồn: [link1], [link2]

### Gaps (thiếu thông tin)
- [Thông tin chưa tìm thấy]
```

## Từ khóa gợi ý cho Blockchain VN
- VN: "blockchain chính sách", "NHNN DLT", "sandbox fintech", "chuyển đổi số blockchain"
- EN: "Vietnam blockchain regulation", "CBDC Vietnam", "blockchain enterprise adoption"
