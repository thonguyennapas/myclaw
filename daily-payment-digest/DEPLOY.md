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

### Bước 1: Copy skill lên server

```bash
# Trên VPS — sau khi đã clone repo
cp -r /tmp/myclaw/daily-payment-digest ~/.openclaw/skills/

# Fix permissions & line endings
chmod +x ~/.openclaw/skills/daily-payment-digest/scripts/*.sh
chmod +x ~/.openclaw/skills/daily-payment-digest/scripts/*.py
find ~/.openclaw/skills/daily-payment-digest/ -type f -exec dos2unix {} \;

# Cài dependency
pip install ddgs
```

### Bước 2: Kiểm tra
```bash
# Kiểm tra file
ls -la ~/.openclaw/skills/daily-payment-digest/
ls -la ~/.openclaw/skills/daily-payment-digest/scripts/

# Test chạy thử
python3 ~/.openclaw/skills/daily-payment-digest/scripts/digest.py --help
```

### Bước 3: Restart OpenClaw
```bash
screen -r
# Ctrl+C → chạy lại lệnh openclaw → Ctrl+A D
```

---

## 📌 2 Cách sử dụng

### ✅ Option 1: Chủ động — Gõ lệnh trên Telegram (Khuyên dùng)

Bạn chủ động nhắn tin cho bot bất cứ lúc nào muốn đọc bản tin:

```
Tổng hợp tin tức thanh toán hôm nay
```

Hoặc các cách nói khác:
```
Bản tin thanh toán
Tin tức payment hôm nay
Có gì mới về thanh toán không?
Digest
```

**Cách hoạt động:**
```
Bạn nhắn Telegram → OpenClaw nhận → match skill → chạy digest.py
    → tìm kiếm ~30 queries → lọc noise → format đẹp → gửi về Telegram
```

**Ưu điểm:**
- Chủ động, muốn đọc lúc nào cũng được
- Không cần cấu hình thêm gì
- Hoạt động ngay sau khi deploy skill

---

### ⏰ Option 2: Bị động — Cron Job tự động 8h sáng mỗi ngày

Cron job tự động gửi 1 message đến OpenClaw bot lúc 8:00 AM,
trigger skill chạy và trả kết quả về Telegram cho bạn.

**Cách hoạt động:**
```
8:00 AM → cron chạy cron_trigger.sh
    → gửi message "Tổng hợp tin tức thanh toán hôm nay" đến bot
    → OpenClaw nhận → chạy skill → gửi bản tin về Telegram
```

#### Cài đặt:

**Cách 1: Chạy script setup tự động**
```bash
bash ~/.openclaw/skills/daily-payment-digest/scripts/cron_setup.sh
```

**Cách 2: Cài thủ công**
```bash
# 1. Set environment variables
echo 'export TELEGRAM_BOT_TOKEN="your_bot_token"' >> ~/.bashrc
echo 'export TELEGRAM_CHAT_ID="your_chat_id"' >> ~/.bashrc
source ~/.bashrc

# 2. Lấy Chat ID (nếu chưa có)
#    Nhắn gì đó cho bot → mở link:
#    https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
#    Tìm "chat":{"id": XXXXXX}

# 3. Test trigger
bash ~/.openclaw/skills/daily-payment-digest/scripts/cron_trigger.sh

# 4. Thêm cron job (8:00 AM mỗi ngày)
crontab -e
# Thêm dòng:
# 0 8 * * * /home/YOUR_USER/.openclaw/skills/daily-payment-digest/scripts/cron_trigger.sh >> /home/YOUR_USER/.openclaw/logs/cron-digest.log 2>&1

# 5. Kiểm tra timezone
timedatectl
# Nếu cần đổi:
# sudo timedatectl set-timezone Asia/Ho_Chi_Minh
```

#### Kiểm tra cron:
```bash
# Xem cron jobs
crontab -l

# Xem log
cat ~/.openclaw/logs/cron-digest.log

# Xóa cron (nếu cần)
crontab -l | grep -v "cron_trigger" | crontab -
```

---

## ⚙️ Cấu hình nâng cao (Optional)

### Tavily API (Khuyên dùng)
Search engine tốt hơn DuckDuckGo, free 1000 requests/tháng:
```bash
# Đăng ký: https://app.tavily.com/sign-in
echo 'export TAVILY_API_KEY="tvly-xxxxx"' >> ~/.bashrc
source ~/.bashrc
# Restart OpenClaw
```

### Thêm/sửa chuyên mục tìm kiếm
Chỉnh file `digest.py`, tìm `SEARCH_CATEGORIES` để thêm queries hoặc thay đổi chuyên mục.

---

## 🔍 Troubleshooting

### Skill không chạy trên Telegram?
```bash
# Kiểm tra SKILL.md
wc -l ~/.openclaw/skills/daily-payment-digest/SKILL.md
# Phải < 60 dòng

# Test script trực tiếp
python3 ~/.openclaw/skills/daily-payment-digest/scripts/digest.py

# Kiểm tra file output
ls -la ~/digests/
cat ~/digests/digest-$(date +%Y-%m-%d).md
```

### Cron job không chạy?
```bash
# Kiểm tra env
echo $TELEGRAM_BOT_TOKEN
echo $TELEGRAM_CHAT_ID

# Test trigger manual
bash ~/.openclaw/skills/daily-payment-digest/scripts/cron_trigger.sh

# Kiểm tra timezone
timedatectl
date
```

---

📅 Cập nhật: 10/02/2026
🔧 Version: 1.0
