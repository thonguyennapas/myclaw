# 🦞 MyClaw Skills - OpenClaw Research Toolkit

## Tổng quan

Bộ skills nghiên cứu chuyên sâu cho OpenClaw, tập trung vào nghiên cứu **Blockchain & Chính sách Việt Nam** với khả năng kiểm chứng nguồn và chống bịa.

## Cấu trúc Skills

```
myclaw/
├── README.md                           ← Bạn đang đọc file này
│
├── deep-research-orchestrator/         ← 🎯 Skill điều phối trung tâm
│   └── SKILL.md                        
│
├── blockchain-policy-research/         ← 📊 Skill nghiên cứu chính
│   ├── SKILL.md                        ← Quy trình & framework nghiên cứu
│   ├── scripts/
│   │   └── research.py                 ← Script tự động tạo báo cáo
│   ├── templates/
│   │   └── report-templates.md         ← Mẫu báo cáo
│   └── resources/
│       └── reference-sources.md        ← Danh sách nguồn tham khảo
│
├── web-research-aggregator/            ← 🔍 Skill thu thập dữ liệu web
│   └── SKILL.md                        ← Quy trình tìm kiếm đa nguồn
│
└── source-validator/                   ← ✅ Skill kiểm chứng nguồn
    └── SKILL.md                        ← Phân loại 5 tier & validate
```

## Skills Chi tiết

### 1. 🎯 Deep Research Orchestrator
**Vai trò**: Skill điều phối trung tâm
- Quản lý quy trình nghiên cứu 5 phase
- Kết nối 3 skill chuyên biệt
- Checklist chất lượng cuối cùng
- Câu lệnh: `/research full`, `/research section:policy`, etc.

### 2. 📊 Blockchain Policy Research
**Vai trò**: Skill nghiên cứu chính - framework báo cáo
- **Phần A**: Xu hướng blockchain toàn cầu + VN (trend map)
- **Phần B**: Chính sách & văn bản pháp lý VN (policy matrix)
- **Phần C**: Đà Nẵng sandbox analysis
- **Phần D**: Vai trò NAPAS + kịch bản tham gia (3 mức rủi ro)
- **Phần E**: Executive Summary
- Quy tắc chống bịa nghiêm ngặt

### 3. 🔍 Web Research Aggregator
**Vai trò**: Thu thập dữ liệu web có hệ thống
- Tìm kiếm đa ngôn ngữ (Việt/Anh)
- Phân loại nguồn theo 5 tiers
- Kiểm chứng chéo (cross-verification)
- Từ khóa gợi ý cho mỗi chủ đề
- Output: JSON + Markdown table

### 4. ✅ Source Validator
**Vai trò**: Kiểm chứng & đánh giá nguồn
- Hệ thống 5 tier (Primary → Unreliable)
- 10-point checklist cho mỗi dữ kiện
- Red flags detection (10 cảnh báo)
- Bảng chứng cứ nguồn tự động
- Xử lý thông tin mâu thuẫn

## Cách Sử dụng

### Cài đặt vào OpenClaw
```bash
# Copy toàn bộ myclaw vào skills directory
cp -r myclaw/* ~/.openclaw/skills/

# Hoặc symlink
ln -s $(pwd)/myclaw/* ~/.openclaw/skills/
```

### Chạy script tạo template báo cáo
```bash
cd myclaw/blockchain-policy-research/scripts
python research.py --full --output ../../../reports
```

### Yêu cầu nghiên cứu qua chat
```
@OpenClaw Hãy sử dụng skill blockchain-policy-research để:
1. Tìm kiếm web về xu hướng blockchain 2025-2026
2. Tổng hợp chính sách blockchain VN (có trích nguồn)
3. Kiểm tra Đà Nẵng sandbox
4. Đề xuất 3 kịch bản cho NAPAS
5. Viết Executive Summary
```

## Output Mong muốn

Sau khi chạy nghiên cứu đầy đủ, sẽ tạo:

| File | Nội dung | Kích thước ước tính |
|------|---------|-------------------|
| `report.md` | Báo cáo đầy đủ consolidated | 15-25 trang |
| `executive-summary.md` | Tóm tắt điều hành | 1-2 trang |
| `trend-map.md` | Bản đồ xu hướng | 3-5 trang |
| `policy-matrix.md` | Bảng chính sách VN | 5-8 trang |
| `danang-sandbox.md` | Phân tích Đà Nẵng | 2-3 trang |
| `napas-roadmap.md` | Lộ trình NAPAS | 5-8 trang |
| `sources.md` | Tất cả nguồn tham khảo | 3-5 trang |

## Lấy cảm hứng từ

Skills trong bộ toolkit này được lấy cảm hứng từ các dự án trong Awesome Claude Skills ecosystem:

- **[deep-research](https://github.com/sanjay3290/ai-skills/tree/main/skills/deep-research)** - Gemini Deep Research Agent
- **[academic-deep-research](https://github.com/openclaw/skills/tree/main/skills/kesslerio/academic-deep-research)** - Academic research with citations
- **[research-cog](https://github.com/openclaw/skills/tree/main/skills/nitishgargiitd/research-cog)** - CellCog #1 DeepResearch Bench
- **[competitive-intelligence](https://github.com/openclaw/skills/tree/main/skills/shashwatgtm/competitive-intelligence-market-research)** - B2B market research
- **[proactive-research](https://github.com/openclaw/skills/tree/main/skills/robbyczgw-cla/proactive-research)** - Topic monitoring & alerts
- **[perplexity](https://github.com/openclaw/skills/tree/main/skills/dronnick/perplexity-bash)** - Perplexity AI search
- **[tavily](https://github.com/openclaw/skills/tree/main/skills/arun-8687/tavily-search)** - AI-optimized web search
- **[brave-search](https://github.com/openclaw/skills/tree/main/skills/steipete/brave-search)** - Brave Search API

## Nguyên tắc Thiết kế

1. **Chống bịa**: Mọi dữ kiện phải có nguồn kiểm chứng
2. **Cấu trúc rõ**: Framework 5 phần (A-E) nhất quán
3. **Đa ngôn ngữ**: Tìm kiếm tiếng Việt + tiếng Anh
4. **Phân tầng**: Nguồn phân loại 5 tier
5. **Actionable**: Đề xuất cụ thể với lộ trình 30-60-90 ngày
6. **NAPAS-oriented**: Tối ưu cho tổ chức trung gian thanh toán

---

📅 Cập nhật: Tháng 2/2026
🔬 Version: 1.0
