# 🦞 MyClaw Skills — OpenClaw Research Toolkit

## Tổng quan

Bộ skills nghiên cứu chuyên sâu cho OpenClaw, tập trung vào nghiên cứu **Blockchain & Chính sách Việt Nam** với khả năng tìm kiếm web thực sự, kiểm chứng nguồn và chống bịa.

## ⚡ Quick Start (3 bước)

```bash
# 1. Deploy skills
bash scripts/deploy.sh --setup-env

# 2. Start gateway
bash scripts/start.sh --screen

# 3. Health check
bash scripts/health-check.sh
```

## Cấu trúc dự án

```
myclaw/
├── .env.example                   ← 🔑 Template biến môi trường (Git-safe)
├── .gitignore                     ← 🔒 Bảo vệ file nhạy cảm
│
├── scripts/                       ← 🛠️ Scripts quản lý hệ thống
│   ├── start.sh                   ← Khởi chạy gateway (tự load .env)
│   ├── deploy.sh                  ← One-command deploy skills
│   └── health-check.sh            ← Kiểm tra toàn bộ hệ thống
│
├── web-search/                    ← 🌐 CORE: Tìm kiếm web thực sự
│   ├── SKILL.md                   ← Hướng dẫn + lệnh bash
│   └── scripts/search.py          ← Multi-engine search (Tavily/DDG)
│
├── daily-payment-digest/          ← 📰 Bản tin thanh toán hằng ngày
│   ├── SKILL.md
│   ├── DEPLOY.md                  ← Hướng dẫn deploy 2 option
│   └── scripts/
│       ├── digest.py              ← Script tổng hợp tin
│       ├── cron_trigger.sh        ← Trigger cho cron job
│       └── cron_setup.sh          ← Setup cron tự động
│
└── deep-research/                 ← 📊 Nghiên cứu Blockchain & Chính sách
    ├── SKILL.md                   ← Orchestrator + template + validation rules
    ├── scripts/
    │   └── research.py            ← Script nghiên cứu tự động
    ├── resources/
    │   └── reference-sources.md   ← Danh sách nguồn tham khảo
    └── templates/
        └── report-templates.md    ← Template báo cáo (SWOT, lộ trình, ...)
```

## 🔑 Quản lý Biến Môi Trường

**KHÔNG BAO GIỜ** gõ API key trực tiếp trên command line!

```bash
# ❌ CŨ (LỘ KEY trong terminal history)
LLM_API_KEY="AIza..." TELEGRAM_TOKEN="837..." openclaw gateway run

# ✅ MỚI (an toàn)
bash scripts/start.sh
```

### Cấu hình `.env`

1. **Copy template**: `cp .env.example ~/.openclaw/.env`
2. **Điền values**: `nano ~/.openclaw/.env`
3. **Start**: `bash scripts/start.sh`

### Biến môi trường hỗ trợ

| Nhóm | Biến | Bắt buộc | Mô tả |
|-|-|-|-|
| **LLM** | `LLM_PROVIDER` | ✅ | gemini, openai, anthropic |
| | `LLM_MODEL` | ✅ | gemini-2.5-flash, gpt-4o, ... |
| | `LLM_API_KEY` | ✅ | API key của provider |
| **Telegram** | `TELEGRAM_TOKEN` | ✅ | Bot token |
| | `TELEGRAM_CHAT_ID` | 🔸 | Cho cron job |
| **Search** | `TAVILY_API_KEY` | 🔸 | AI search (free 1000/tháng) |
| | `GOOGLE_API_KEY` | 🔸 | Google Search (free 100/ngày) |
| **Slack** | `SLACK_BOT_TOKEN` | 🔜 | Coming soon |
| **Teams** | `TEAMS_APP_ID` | 🔜 | Coming soon |
| **Zalo** | `ZALO_APP_ID` | 🔜 | Coming soon |

## Kiến trúc

```
                    ┌──────────────────────┐
                    │    ~/.openclaw/.env   │
                    │  (Unified Config)     │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  scripts/start.sh    │
                    │  (Load .env)         │
                    └──────────┬───────────┘
                               │
User ──┬── Telegram ──┐        │
       ├── Slack ─────┼── OpenClaw Gateway ── AI Agent
       ├── Teams ─────┤        │              ↓
       └── Zalo ──────┘        │        Đọc SKILL.md
                               │              ↓
                               │        Chạy scripts
                               │              ↓
                               └────── Trả kết quả
```

**Nguyên tắc thiết kế:**
1. **Một file .env** quản lý tất cả → không lộ key
2. **SKILL.md ngắn gọn** → vừa context window
3. **Có lệnh bash cụ thể** → AI biết chạy gì
4. **1 task = 1 folder** → gọn gàng, dễ quản lý

## Skills Chi tiết

### 1. 🌐 Web Search (Core Utility)
- Tìm kiếm internet thực sự qua `search.py`
- Auto-chọn engine: Tavily → DuckDuckGo
- Hỗ trợ tiếng Việt (`--region vn-vi`), tin tức, batch search
- **Dùng chung** cho cả daily-payment-digest và deep-research

### 2. 📰 Daily Payment Digest
- Bản tin thanh toán tổng hợp 6 chuyên mục
- 2 cách: Chủ động (Telegram) hoặc Bị động (Cron job 8h sáng)
- Tìm kiếm đa ngôn ngữ, lọc noise, xếp hạng relevance

### 3. 📊 Deep Research
- Nghiên cứu Blockchain & Chính sách VN chuyên sâu
- Framework 5 phần: Xu hướng → Chính sách → Đà Nẵng → NAPAS → Summary
- Kiểm chứng nguồn 5 Tier, cross-verify ≥ 2 nguồn
- Templates: SWOT, Use Case Matrix, Lộ trình triển khai

## Thêm Skill Mới

```bash
# 1. Tạo folder
mkdir -p myclaw/ten-skill-moi/scripts

# 2. Tạo SKILL.md (< 100 dòng) theo template
# 3. (Optional) Thêm scripts/tool.py
# 4. Thêm tên vào SKILLS array trong scripts/deploy.sh
# 5. Push & deploy:
git push origin main
bash scripts/deploy.sh
bash scripts/start.sh --screen
```

## Thêm Channel Mới (Teams / Slack / Zalo)

1. Thêm biến vào `.env.example` (đã chuẩn bị sẵn)
2. Cấu hình trong `.env` trên server
3. Restart gateway: `bash scripts/start.sh --screen`

> **Skills không cần thay đổi** khi thêm kênh mới — OpenClaw tự xử lý routing.

---

📅 Cập nhật: 10/02/2026
🔧 Version: 4.0 — Refactored: gộp 4 research skills → 1 folder `deep-research`
