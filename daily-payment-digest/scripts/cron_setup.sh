#!/bin/bash
# ==============================================================================
# 📰 Daily Payment Digest — Cron Setup cho OpenClaw
#
# Tất cả cấu hình đọc từ ~/.openclaw/.env:
#   - DIGEST_CRON_SCHEDULE  (mặc định: 0 8 * * *)
#   - TELEGRAM_TOKEN
#   - TELEGRAM_CHAT_ID
# ==============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📰 Daily Payment Digest — Cron Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TRIGGER_SCRIPT="$SCRIPT_DIR/cron_trigger.sh"
ENV_FILE="$HOME/.openclaw/.env"

# ── Load unified .env ──
if [ -f "$ENV_FILE" ]; then
    while IFS='=' read -r key value; do
        [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        value="${value%\"}"; value="${value#\"}"
        value="${value%\'}"; value="${value#\'}"
        export "$key=$value"
    done < "$ENV_FILE"
else
    echo -e "${RED}❌ File .env không tìm thấy: $ENV_FILE${NC}"
    echo -e "   Chạy: cp .env.example $ENV_FILE && nano $ENV_FILE"
    exit 1
fi

# ── 1. Kiểm tra files ──
echo -e "${BLUE}[1/5] Kiểm tra files...${NC}"

if [ ! -f "$TRIGGER_SCRIPT" ]; then
    echo -e "${RED}❌ Không tìm thấy cron_trigger.sh${NC}"
    exit 1
fi
chmod +x "$TRIGGER_SCRIPT"
chmod +x "$SCRIPT_DIR/digest.py" 2>/dev/null || true
echo -e "  ${GREEN}✅ cron_trigger.sh: OK${NC}"

# ── 2. Kiểm tra env ──
echo ""
echo -e "${BLUE}[2/5] Kiểm tra Telegram config từ .env...${NC}"

BOT_TOKEN="${TELEGRAM_TOKEN:-${TELEGRAM_BOT_TOKEN:-}}"
CHAT_ID="${TELEGRAM_CHAT_ID:-${DIGEST_CHAT_ID:-}}"

if [ -z "$BOT_TOKEN" ]; then
    echo -e "  ${YELLOW}⚠️ TELEGRAM_TOKEN chưa set trong .env${NC}"
    read -p "  Nhập Bot Token: " TOKEN_INPUT
    if [ -n "$TOKEN_INPUT" ]; then
        # Cập nhật trực tiếp vào .env
        if grep -q "^TELEGRAM_TOKEN=" "$ENV_FILE"; then
            sed -i "s|^TELEGRAM_TOKEN=.*|TELEGRAM_TOKEN=$TOKEN_INPUT|" "$ENV_FILE"
        else
            echo "TELEGRAM_TOKEN=$TOKEN_INPUT" >> "$ENV_FILE"
        fi
        echo -e "  ${GREEN}✅ Đã lưu vào $ENV_FILE${NC}"
    fi
else
    echo -e "  ${GREEN}✅ Bot Token: OK${NC}"
fi

if [ -z "$CHAT_ID" ]; then
    echo -e "  ${YELLOW}⚠️ TELEGRAM_CHAT_ID chưa set trong .env${NC}"
    echo "  💡 Lấy ID: nhắn tin cho bot → mở https://api.telegram.org/bot<TOKEN>/getUpdates"
    read -p "  Nhập Chat ID: " CHAT_INPUT
    if [ -n "$CHAT_INPUT" ]; then
        if grep -q "^TELEGRAM_CHAT_ID=" "$ENV_FILE"; then
            sed -i "s|^TELEGRAM_CHAT_ID=.*|TELEGRAM_CHAT_ID=$CHAT_INPUT|" "$ENV_FILE"
        else
            echo "TELEGRAM_CHAT_ID=$CHAT_INPUT" >> "$ENV_FILE"
        fi
        echo -e "  ${GREEN}✅ Đã lưu vào $ENV_FILE${NC}"
    fi
else
    echo -e "  ${GREEN}✅ Chat ID: OK${NC}"
fi

# ── 3. Timezone ──
echo ""
echo -e "${BLUE}[3/5] Kiểm tra timezone...${NC}"

CURRENT_TZ=$(timedatectl show -p Timezone --value 2>/dev/null || echo "Unknown")
echo -e "  📍 Timezone: ${CURRENT_TZ}"

if [ "$CURRENT_TZ" != "Asia/Ho_Chi_Minh" ]; then
    echo -e "  ${YELLOW}⚠️ Khuyến nghị: Asia/Ho_Chi_Minh${NC}"
    read -p "  Đổi timezone? (y/N): " CHANGE_TZ
    if [ "$CHANGE_TZ" = "y" ]; then
        sudo timedatectl set-timezone Asia/Ho_Chi_Minh
        echo -e "  ${GREEN}✅ Đã đổi timezone${NC}"
    fi
fi

# ── 4. Đọc schedule từ .env ──
echo ""
echo -e "${BLUE}[4/5] Đọc lịch chạy từ .env...${NC}"

CRON_SCHEDULE="${DIGEST_CRON_SCHEDULE:-0 8 * * *}"
echo -e "  ⏰ Lịch chạy: ${GREEN}${CRON_SCHEDULE}${NC}"

# Giải thích schedule
CRON_HOUR=$(echo "$CRON_SCHEDULE" | awk '{print $2}')
CRON_MIN=$(echo "$CRON_SCHEDULE" | awk '{print $1}')
CRON_DOW=$(echo "$CRON_SCHEDULE" | awk '{print $5}')

case "$CRON_DOW" in
    "*")     DOW_TEXT="mỗi ngày" ;;
    "1-5")   DOW_TEXT="Thứ 2 → Thứ 6" ;;
    "1,3,5") DOW_TEXT="Thứ 2, 4, 6" ;;
    *)       DOW_TEXT="$CRON_DOW" ;;
esac

echo -e "  📋 Nghĩa là: ${CRON_HOUR}:${CRON_MIN} — ${DOW_TEXT}"
echo ""
echo -e "  ${YELLOW}💡 Đổi lịch? Sửa DIGEST_CRON_SCHEDULE trong:${NC}"
echo -e "     $ENV_FILE"
echo -e "     Ví dụ: DIGEST_CRON_SCHEDULE=0 7 * * 1-5  (7h sáng, T2-T6)"

# ── 5. Cài cron ──
echo ""
echo -e "${BLUE}[5/5] Cài đặt cron job...${NC}"

CRON_LINE="$CRON_SCHEDULE $TRIGGER_SCRIPT >> $HOME/.openclaw/logs/cron-digest.log 2>&1"

# Xóa entry cũ nếu có
(crontab -l 2>/dev/null | grep -v "cron_trigger.sh" | grep -v "Daily Payment Digest") > /tmp/crontab_tmp || true

# Thêm entry mới
echo "" >> /tmp/crontab_tmp
echo "# 📰 Daily Payment Digest — schedule from .env" >> /tmp/crontab_tmp
echo "$CRON_LINE" >> /tmp/crontab_tmp

crontab /tmp/crontab_tmp
rm -f /tmp/crontab_tmp

mkdir -p "$HOME/.openclaw/logs"

echo -e "  ${GREEN}✅ Cron job đã cài: ${CRON_SCHEDULE}${NC}"

# ── Done ──
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ HOÀN TẤT!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Cách hoạt động:"
echo "  ⏰ ${CRON_HOUR}:${CRON_MIN} ${DOW_TEXT} → cron gửi message đến OpenClaw bot"
echo "  🤖 OpenClaw nhận → chạy skill daily-payment-digest"
echo "  📰 Kết quả → gửi về Telegram cho bạn"
echo ""
echo "📌 Lệnh hữu ích:"
echo "  crontab -l                              # Xem cron"
echo "  bash $TRIGGER_SCRIPT                    # Test trigger"
echo "  crontab -l | grep -v cron_trigger | crontab -  # Xóa cron"
echo ""
echo "⚙️  Tùy chỉnh:"
echo "  nano $ENV_FILE"
echo "    DIGEST_CRON_SCHEDULE=0 7 * * 1-5      # Đổi giờ / ngày"
echo "    DIGEST_MAX_RESULTS=3                  # Giảm số bài"
echo "    DIGEST_TIMELIMIT=d                    # Chỉ lấy tin hôm nay"
echo ""
