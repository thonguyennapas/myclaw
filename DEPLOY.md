# 🚀 Hướng dẫn Triển khai MyClaw Skills lên VPS

## Yêu cầu
- VPS Ubuntu (22.04 / 24.04) đã cài OpenClaw
- Git, Python 3.10+, screen
- SSH access

> 💡 **Python 3.12+** (Ubuntu 24.04): `deploy.sh` tự xử lý PEP 668 (`--break-system-packages`)

---

## ⚡ Triển khai Nhanh (Lần đầu)

```bash
# 1. Clone repo
cd /tmp && rm -rf myclaw
git clone https://github.com/thonguyennapas/myclaw.git

# 2. Deploy tất cả (skills + .env setup)
cd /tmp/myclaw && bash scripts/deploy.sh --setup-env

# 3. Start gateway
bash scripts/start.sh --screen

# 4. Verify
bash scripts/health-check.sh
```

Xong! Test qua Telegram:
```
Tìm kiếm web về xu hướng blockchain 2025
```

---

## Triển khai Chi tiết (Step-by-Step)

### BƯỚC 1: SSH vào VPS

```bash
ssh YOUR_USER@YOUR_VPS_IP
```

### BƯỚC 2: Clone repo

```bash
cd /tmp && rm -rf myclaw
git clone https://github.com/thonguyennapas/myclaw.git
```

### BƯỚC 3: Tạo file `.env`

```bash
# Copy template → điền giá trị thật
cp /tmp/myclaw/.env.example ~/.openclaw/.env
nano ~/.openclaw/.env
```

**Các giá trị cần điền:**

| Variable | Mô tả | Cách lấy |
|-|-|-|
| `LLM_API_KEY` | Gemini API Key | [Google AI Studio](https://aistudio.google.com/) |
| `TELEGRAM_TOKEN` | Bot token | [BotFather](https://t.me/BotFather) |
| `TAVILY_API_KEY` | Search API (optional) | [Tavily](https://app.tavily.com/sign-in) |
| `TELEGRAM_CHAT_ID` | Cho cron job (optional) | Nhắn bot → [getUpdates](https://api.telegram.org/bot<TOKEN>/getUpdates) |

⚠️ **KHÔNG BAO GIỜ commit `.env` lên Git!** File `.gitignore` đã bảo vệ.

### BƯỚC 4: Deploy skills

```bash
cd /tmp/myclaw
bash scripts/deploy.sh
```

Script tự động:
- 🗑️ Dọn skill cũ không còn trong danh sách (tránh xung đột sau refactor)
- 📦 Copy skills mới vào `~/.openclaw/skills/`
- 🔧 Fix line endings (CRLF → LF) + set permissions
- 📥 Cài dependencies (`ddgs`, `requests`) — auto-detect PEP 668
- 📄 Copy `.env.example` vào `~/.openclaw/` để luôn có template tham khảo

### BƯỚC 5: Kiểm tra sức khỏe

```bash
bash scripts/health-check.sh
```

Kết quả mong đợi:
```
📊 Results: 10 pass | 0 warn | 0 fail
🎉 Everything looks great!
```

### BƯỚC 6: Start gateway

```bash
# Chạy trong screen (khuyên dùng)
bash scripts/start.sh --screen

# Hoặc chạy foreground
bash scripts/start.sh
```

Kiểm tra:
```bash
screen -r openclaw    # Xem logs
# Ctrl+A → D          # Detach
```

### BƯỚC 7: Test qua Telegram

```
Tìm kiếm web về xu hướng blockchain 2025
```

```
Nghiên cứu chính sách blockchain Việt Nam, có trích nguồn
```

```
Tổng hợp tin tức thanh toán hôm nay
```

---

## 🔄 Cập nhật Skills (Lần sau)

### Trên máy Windows (push):
```bash
cd C:\Users\thonv\Desktop\napas\openclaw\myclaw
git add .
git commit -m "update: mô tả thay đổi"
git push origin main
```

### Trên VPS (pull & deploy):
```bash
cd /tmp && rm -rf myclaw
git clone https://github.com/thonguyennapas/myclaw.git
cd /tmp/myclaw && bash scripts/deploy.sh

# Restart gateway
bash scripts/start.sh --screen
```

> **`.env` không bị ghi đè** vì deploy.sh chỉ ghi nếu chưa tồn tại.

---

## ⏰ Cron Job — Bản tin tự động 8h sáng

```bash
# Setup cron
bash ~/.openclaw/skills/daily-payment-digest/scripts/cron_setup.sh

# Hoặc thủ công
crontab -e
# Thêm: 0 8 * * * ~/.openclaw/skills/daily-payment-digest/scripts/cron_trigger.sh >> ~/.openclaw/logs/cron-digest.log 2>&1
```

> Yêu cầu: `TELEGRAM_CHAT_ID` đã set trong `.env`

---

## ➕ Thêm Skill Mới

### 1. Tạo folder + SKILL.md

```
myclaw/
└── ten-skill-moi/
    ├── SKILL.md           ← NGẮN GỌN (< 100 dòng)
    └── scripts/           ← (optional) Scripts thực thi
        └── tool.py
```

### 2. Template SKILL.md:

```yaml
---
name: ten-skill-moi
description: "Mô tả ngắn gọn skill làm gì. 1-2 câu."
---

# Tên Skill

## Khi nào sử dụng
- Điều kiện 1
- Điều kiện 2

## Cách thực hiện
```bash
python3 ~/.openclaw/skills/ten-skill-moi/scripts/tool.py "input"
```
```

### 3. Đăng ký trong deploy.sh

Thêm tên skill vào array `SKILLS` trong `scripts/deploy.sh`:
```bash
SKILLS=(
    ...
    "ten-skill-moi"    # ← thêm dòng này
)
```

### 4. Deploy
```bash
git push origin main
# Trên VPS:
cd /tmp/myclaw && bash scripts/deploy.sh
bash scripts/start.sh --screen
```

---

## 🔧 Troubleshooting

### Quick fix:
```bash
# 1. Chạy health check
bash scripts/health-check.sh

# 2. Kiểm tra logs
screen -r openclaw

# 3. Test search trực tiếp
python3 ~/.openclaw/skills/web-search/scripts/search.py "test" --max 2

# 4. Xem SKILL.md
wc -l ~/.openclaw/skills/*/SKILL.md
```

### Skill không hoạt động?

| Nguyên nhân | Cách fix |
|-|-|
| SKILL.md quá dài (> 120 dòng) | Rút gọn < 100 dòng |
| Không có lệnh bash | Thêm block ```bash``` cụ thể |
| Description mơ hồ | Sửa frontmatter description |
| Line endings CRLF | `dos2unix ~/.openclaw/skills/*/SKILL.md` |
| Thiếu permissions | `chmod +x ~/.openclaw/skills/*/scripts/*.py` |

### pip install thất bại (PEP 668)?

```bash
# Ubuntu 24.04 / Python 3.12+ chặn pip install system-wide
# deploy.sh đã tự xử lý, nhưng nếu cần thủ công:
pip install --break-system-packages ddgs requests
```

### Gateway không start?

```bash
# Check .env
cat ~/.openclaw/.env

# Check OpenClaw
openclaw --version
openclaw gateway status

# Restart
bash scripts/start.sh --screen
```

---

## 🔐 Bảo mật

| ✅ Đúng | ❌ Sai |
|-|-|
| Dùng `.env` file | Gõ key trên command line |
| `.gitignore` chặn `.env` | Commit `.env` lên Git |
| Copy `.env.example` → `.env` | Hardcode key trong script |
| `start.sh` tự load `.env` | Export key vào `.bashrc` |

---

📅 Cập nhật: 10/02/2026
🔧 Version: 4.1 — Auto cleanup old skills, PEP 668 support, .env.example auto-copy
