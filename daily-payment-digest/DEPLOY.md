# 📰 Daily Payment Tech Digest — Hướng dẫn Triển khai

## Tổng quan

Bản tin thanh toán hằng ngày, tổng hợp 6 chuyên mục:
- 🌐 Công nghệ thanh toán mới
- 🏦 Visa, Mastercard, card networks
- ⛓️ Blockchain, crypto payments, CBDC
- 🤖 Agentic commerce, AI payments, Google UCP
- 📅 Events quốc tế & Việt Nam
- 🇻🇳 Thanh toán Việt Nam (NAPAS, NHNN, VNPay...)

---

## 🚀 Triển khai trên Ubuntu Server

### Bước 1: Deploy skill (nếu chưa deploy toàn bộ)

```bash
# Đã deploy toàn bộ myclaw? → bỏ qua bước này
# Chưa? → chạy:
cd /tmp/myclaw && bash scripts/deploy.sh --setup-env
```

### Bước 2: Kiểm tra

```bash
ls -la ~/.openclaw/skills/daily-payment-digest/
ls -la ~/.openclaw/skills/daily-payment-digest/scripts/

# Test chạy thử
python3 ~/.openclaw/skills/daily-payment-digest/scripts/digest.py --help
```

### Bước 3: Restart OpenClaw

```bash
bash scripts/start.sh --screen
```

---

## 📌 2 Cách sử dụng

### ✅ Option 1: Chủ động — Gõ lệnh trên Telegram (Khuyên dùng)

Nhắn tin cho bot bất cứ lúc nào:

```
Tổng hợp tin tức thanh toán hôm nay
```

Hoặc:
```
Bản tin thanh toán
Tin tức payment hôm nay
Có gì mới về thanh toán không?
Digest
```

**Cách hoạt động:**
```
Bạn nhắn Telegram → OpenClaw → match skill → chạy digest.py
    → tìm kiếm ~30 queries → lọc noise → format → gửi về Telegram
```

**Ưu điểm:**
- Chủ động, muốn đọc lúc nào cũng được
- Không cần cấu hình thêm gì
- Hoạt động ngay sau deploy

---

### ⏰ Option 2: Bị động — Cron Job tự động 8h sáng

**Yêu cầu:** `TELEGRAM_CHAT_ID` đã set trong `~/.openclaw/.env`

```
8:00 AM → cron → cron_trigger.sh → chạy digest.py trực tiếp
    → tạo file digest → đọc file → gửi thẳng qua Telegram API
```

> ⚠️ Cron trigger chạy **trực tiếp** `digest.py` rồi gửi qua Telegram API,
> **không** đi qua OpenClaw gateway (vì bot không thể trigger chính mình).

#### Cài đặt:

**Cách 1: Script tự động**
```bash
bash ~/.openclaw/skills/daily-payment-digest/scripts/cron_setup.sh
```

**Cách 2: Thủ công**
```bash
# 1. Đảm bảo TELEGRAM_CHAT_ID đã set trong ~/.openclaw/.env
nano ~/.openclaw/.env
# Thêm: TELEGRAM_CHAT_ID=your_chat_id

# 2. Lấy Chat ID (nếu chưa có)
#    Nhắn gì đó cho bot → mở:
#    https://api.telegram.org/bot<TOKEN>/getUpdates
#    Tìm "chat":{"id": XXXXXX}

# 3. Test trigger
bash ~/.openclaw/skills/daily-payment-digest/scripts/cron_trigger.sh

# 4. Thêm cron job
crontab -e
# Thêm dòng:
# 0 8 * * * /home/USER/.openclaw/skills/daily-payment-digest/scripts/cron_trigger.sh >> /home/USER/.openclaw/logs/cron-digest.log 2>&1

# 5. Kiểm tra timezone
timedatectl
# Đổi nếu cần: sudo timedatectl set-timezone Asia/Ho_Chi_Minh
```

#### Kiểm tra cron:
```bash
crontab -l                                                # Xem cron
cat ~/.openclaw/logs/cron-digest.log                      # Xem log
crontab -l | grep -v "cron_trigger" | crontab -          # Xóa cron
```

---

## ⚙️ Cấu hình nâng cao (Optional)

### Tavily API (Khuyên dùng)
Search engine AI tốt hơn DuckDuckGo, free 1000 requests/tháng:

```bash
# Thêm vào ~/.openclaw/.env
nano ~/.openclaw/.env
# Uncomment & điền: TAVILY_API_KEY=tvly-xxxxx

# Restart
bash scripts/start.sh --screen
```

### Thêm/sửa chuyên mục
Chỉnh `digest.py`, tìm `SEARCH_CATEGORIES` để thêm queries hoặc thay đổi chuyên mục.

---

## 🔍 Troubleshooting

### Skill không chạy trên Telegram?
```bash
# Health check toàn bộ
bash scripts/health-check.sh

# Test script trực tiếp
python3 ~/.openclaw/skills/daily-payment-digest/scripts/digest.py

# Kiểm tra output
ls -la ~/digests/
cat ~/digests/digest-$(date +%Y-%m-%d).md
```

### Cron job không chạy?
```bash
# Kiểm tra .env
grep TELEGRAM ~/.openclaw/.env

# Test trigger manual
bash ~/.openclaw/skills/daily-payment-digest/scripts/cron_trigger.sh

# Kiểm tra timezone
timedatectl && date
```

---

📅 Cập nhật: 10/02/2026
🔧 Version: 2.0 — Unified .env config
