---
name: web-research-aggregator
description: "Thu thập và tổng hợp dữ liệu từ nhiều nguồn web cho mục đích nghiên cứu. Hỗ trợ tìm kiếm đa ngôn ngữ (Việt/Anh), phân loại kết quả, và kiểm chứng chéo. Sử dụng khi cần thu thập dữ liệu nghiên cứu có hệ thống."
---

# Web Research Aggregator Skill

## Mô tả
Skill thu thập và tổng hợp thông tin từ nhiều nguồn web một cách có hệ thống, đặc biệt phù hợp cho nghiên cứu chính sách và xu hướng công nghệ tại Việt Nam.

## Khi nào sử dụng
- Khi cần thu thập thông tin từ nhiều nguồn cho một chủ đề nghiên cứu
- Khi cần tìm kiếm bằng cả tiếng Việt và tiếng Anh
- Khi cần kiểm chứng chéo (cross-verify) thông tin từ nhiều nguồn
- Khi cần tổng hợp kết quả tìm kiếm thành báo cáo có cấu trúc

## Quy trình Tìm kiếm

### Bước 1: Xác định Từ khóa
Với mỗi chủ đề nghiên cứu, xác định:
```
1. Từ khóa chính (primary keywords) - tiếng Việt
2. Từ khóa chính (primary keywords) - tiếng Anh
3. Từ khóa mở rộng (related terms)
4. Từ khóa loại trừ (exclusions)
5. Phạm vi thời gian (date range)
```

### Bước 2: Tìm kiếm Đa nguồn
```
Nguồn ưu tiên:
├── Tier 1: Website chính phủ (.gov.vn)
│   ├── chinhphu.vn
│   ├── sbv.gov.vn 
│   ├── mic.gov.vn
│   ├── most.gov.vn
│   └── vanban.chinhphu.vn
│
├── Tier 2: Tổ chức quốc tế
│   ├── bis.org
│   ├── worldbank.org
│   ├── imf.org
│   └── weforum.org
│
├── Tier 3: Cơ sở dữ liệu pháp luật
│   ├── thuvienphapluat.vn
│   └── luatvietnam.vn
│
├── Tier 4: Báo chí uy tín
│   ├── vnexpress.net
│   ├── tuoitre.vn
│   └── ledgerinsights.com
│
└── Tier 5: Nghiên cứu / Báo cáo
    ├── scholar.google.com
    ├── arxiv.org
    └── ssrn.com
```

### Bước 3: Thu thập & Phân loại
Với mỗi kết quả tìm kiếm:

```yaml
result:
  title: "[Tiêu đề]"
  url: "[URL]"
  source_tier: 1-5
  language: vi|en
  date: "DD/MM/YYYY"
  category: policy|trend|market|technical|sandbox
  reliability: verified|secondary|unverified
  summary: "[Tóm tắt 2-3 câu]"
  key_facts:
    - "[Dữ kiện 1]"
    - "[Dữ kiện 2]"
  related_docs: ["[link1]", "[link2]"]
```

### Bước 4: Kiểm chứng Chéo
```
Quy tắc cross-verification:
1. Mỗi dữ kiện quan trọng cần ≥ 2 nguồn xác nhận
2. Nếu chỉ có 1 nguồn → đánh dấu "cần kiểm chứng thêm"
3. Nếu các nguồn mâu thuẫn → ghi nhận cả hai quan điểm
4. Ưu tiên nguồn Tier 1 khi có mâu thuẫn
5. Ghi rõ ngày truy cập nguồn
```

### Bước 5: Tổng hợp Kết quả
```markdown
## Kết quả Nghiên cứu: [Chủ đề]

### Tổng quan
- Số nguồn tìm được: [N]
- Số nguồn hữu ích: [M]
- Mức độ tin cậy tổng thể: [Cao/TB/Thấp]

### Phát hiện chính
1. [Phát hiện 1] — Nguồn: [link1], [link2]
2. [Phát hiện 2] — Nguồn: [link3]

### Gaps (Thiếu thông tin)
- [Thông tin chưa tìm thấy 1]
- [Thông tin chưa tìm thấy 2]

### Cần kiểm chứng thêm
- [Nhận định chưa chắc chắn 1]
```

## Mẫu Từ khóa cho Blockchain Research tại VN

### Tiếng Việt
```
Nhóm 1 - Chính sách:
"blockchain Việt Nam chính sách" "site:chinhphu.vn"
"blockchain Việt Nam nghị quyết quyết định"
"NHNN blockchain DLT"
"sandbox fintech Việt Nam"
"tài sản số tiền mã hóa khung pháp lý"
"chuyển đổi số blockchain"

Nhóm 2 - Đà Nẵng:
"Đà Nẵng blockchain" "site:danang.gov.vn"
"Đà Nẵng sandbox thí điểm công nghệ"
"Đà Nẵng thành phố thông minh blockchain"

Nhóm 3 - Ứng dụng:
"blockchain ngân hàng Việt Nam"
"blockchain thanh toán liên ngân hàng"
"NAPAS blockchain"
"đối soát blockchain"
```

### Tiếng Anh
```
Nhóm 1 - Trends:
"blockchain enterprise adoption 2025"
"CBDC global progress 2025 2026"
"real world asset tokenization RWA"
"blockchain cross-border payment"

Nhóm 2 - Vietnam:
"Vietnam blockchain regulation policy"
"Vietnam CBDC digital currency"
"Vietnam fintech sandbox"
"Vietnam digital transformation blockchain"

Nhóm 3 - Payment:
"blockchain interbank settlement"
"payment infrastructure blockchain"
"tokenization payment instruments"
```

## Output Formats

### Markdown Table (mặc định)
```markdown
| # | Nguồn | Ngày | Tier | Tóm tắt | Link |
|---|-------|------|------|---------|------|
| 1 | Chính phủ VN | 01/2025 | T1 | ... | [link] |
```

### JSON (cho xử lý tự động)
```json
{
  "topic": "blockchain policy vietnam",
  "search_date": "2026-02-09",
  "total_results": 45,
  "filtered_results": 12,
  "results": [
    {
      "title": "...",
      "url": "...",
      "tier": 1,
      "reliability": "verified",
      "key_facts": ["..."]
    }
  ]
}
```

## Lưu ý
1. **Rate limiting**: Không gửi quá nhiều request liên tục
2. **Robots.txt**: Tuân thủ quy tắc crawling
3. **Cache**: Lưu cache kết quả để tiết kiệm bandwidth
4. **Date stamp**: Luôn ghi ngày tìm kiếm/truy cập
5. **Backup**: Lưu snapshot nội dung quan trọng (phòng link hỏng)
