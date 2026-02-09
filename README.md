# 🦞 MyClaw Skills - OpenClaw Research Toolkit

## Tổng quan

Bộ skills nghiên cứu chuyên sâu cho OpenClaw, tập trung vào nghiên cứu **Blockchain & Chính sách Việt Nam** với khả năng tìm kiếm web thực sự, kiểm chứng nguồn và chống bịa.

## ⚡ Cài đặt nhanh

```bash
cp -r myclaw/* ~/.openclaw/skills/
pip install ddgs
# Restart OpenClaw
```

## Cấu trúc Skills

```
myclaw/
├── web-search/                    ← 🌐 CORE: Tìm kiếm web thực sự
│   ├── SKILL.md                   ← Hướng dẫn ngắn gọn + lệnh bash
│   └── scripts/
│       └── search.py              ← Script tìm kiếm (Tavily/DDG/Google)
│
├── blockchain-policy-research/    ← 📊 Skill nghiên cứu chính
│   ├── SKILL.md                   ← Quy trình + lệnh tìm kiếm
│   ├── scripts/research.py        ← Script tạo báo cáo
│   ├── templates/                 ← Mẫu báo cáo (đọc on-demand)
│   └── resources/                 ← Nguồn tham khảo
│
├── deep-research-orchestrator/    ← 🎯 Điều phối nghiên cứu
│   └── SKILL.md                   ← Quy trình 4 phase
│
├── web-research-aggregator/       ← 🔍 Thu thập đa nguồn
│   └── SKILL.md                   ← Batch search + cross-verify
│
└── source-validator/              ← ✅ Kiểm chứng nguồn
    └── SKILL.md                   ← Hệ thống 5 tier
```

## Kiến trúc

```
User (Telegram) → OpenClaw Gateway → AI Agent
                                      ↓
                              Đọc SKILL.md (ngắn gọn)
                                      ↓
                              Chạy scripts (search.py)
                                      ↓
                              Trả kết quả về Telegram
```

**Nguyên tắc thiết kế:**
1. **SKILL.md ngắn gọn** (< 60 dòng) — vừa context window
2. **Có lệnh bash cụ thể** — AI biết chạy gì
3. **Scripts thực thi** — công cụ thực sự, không chỉ hướng dẫn
4. **Modular** — dễ thêm skill mới

## Skills Chi tiết

### 1. 🌐 Web Search (Core)
- Tìm kiếm internet thực sự qua `search.py`
- Auto-chọn engine: Tavily → DuckDuckGo
- Hỗ trợ tiếng Việt (`--region vn-vi`), tin tức, batch search
- **Cần**: `pip install ddgs` (miễn phí)

### 2. 📊 Blockchain Policy Research
- Framework 5 phần: Xu hướng → Chính sách → Đà Nẵng → NAPAS → Summary
- Tự động gọi web-search để tìm dữ liệu
- Chống bịa: mọi dữ kiện phải có nguồn

### 3. 🎯 Deep Research Orchestrator
- Điều phối 4 phase: Thu thập → Kiểm chứng → Viết → Review
- Kết nối 3 skill con thành pipeline

### 4. 🔍 Web Research Aggregator
- Batch search đa ngôn ngữ (VI + EN)
- Cross-verify và phân loại nguồn

### 5. ✅ Source Validator
- Phân loại nguồn 5 tier (Primary → Unreliable)
- Red flags detection
- Bảng chứng cứ nguồn

## Cách Test qua Telegram

```
# Test web search
Tìm kiếm web về xu hướng blockchain 2025

# Test nghiên cứu
Nghiên cứu chính sách blockchain Việt Nam, có trích nguồn

# Test đầy đủ
Thực hiện nghiên cứu blockchain theo quy trình deep-research-orchestrator
```

## Thêm Skill Mới

1. Tạo folder `myclaw/ten-skill-moi/`
2. Tạo `SKILL.md` ngắn gọn (< 60 dòng) với lệnh bash cụ thể
3. (Optional) Thêm `scripts/tool.py`
4. Push & deploy (xem DEPLOY.md)

---

📅 Cập nhật: 09/02/2026
🔧 Version: 2.0
