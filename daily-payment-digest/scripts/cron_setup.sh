#!/bin/bash
# ==============================================================================
# 📰 Daily Payment Digest — Cron Setup cho OpenClaw
# Cài cron job gửi trigger đến OpenClaw bot mỗi 8h sáng
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

# ── 1. Kiểm tra files ──
echo -e "${BLUE}[1/4] Kiểm tra files...${NC}"

if [ ! -f "$TRIGGER_SCRIPT" ]; then
    echo -e "${RED}❌ Không tìm thấy cron_trigger.sh${NC}"
    exit 1
fi
chmod +x "$TRIGGER_SCRIPT"
chmod +x "$SCRIPT_DIR/digest.py" 2>/dev/null || true
echo -e "  ${GREEN}✅ cron_trigger.sh: OK${NC}"

# ── 2. Kiểm tra env ──
echo ""
echo -e "${BLUE}[2/4] Kiểm tra Telegram config...${NC}"

if [ -z "$TELEGRAM_BOT_TOKEN" ] && [ -z "$TELEGRAM_TOKEN" ]; then
    echo -e "  ${YELLOW}⚠️ TELEGRAM_BOT_TOKEN chưa set${NC}"
    read -p "  Nhập Bot Token: " TOKEN_INPUT
    if [ -n "$TOKEN_INPUT" ]; then
        echo "export TELEGRAM_BOT_TOKEN=\"$TOKEN_INPUT\"" >> ~/.bashrc
        echo -e "  ${GREEN}✅ Đã lưu vào ~/.bashrc${NC}"
    fi
else
    echo -e "  ${GREEN}✅ Bot Token: OK${NC}"
fi

if [ -z "$TELEGRAM_CHAT_ID" ] && [ -z "$DIGEST_CHAT_ID" ]; then
    echo -e "  ${YELLOW}⚠️ TELEGRAM_CHAT_ID chưa set${NC}"
    echo "  💡 Lấy ID: nhắn tin cho bot → mở https://api.telegram.org/bot<TOKEN>/getUpdates"
    read -p "  Nhập Chat ID: " CHAT_INPUT
    if [ -n "$CHAT_INPUT" ]; then
        echo "export TELEGRAM_CHAT_ID=\"$CHAT_INPUT\"" >> ~/.bashrc
        echo -e "  ${GREEN}✅ Đã lưu vào ~/.bashrc${NC}"
    fi
else
    echo -e "  ${GREEN}✅ Chat ID: OK${NC}"
fi

# ── 3. Timezone ──
echo ""
echo -e "${BLUE}[3/4] Kiểm tra timezone...${NC}"

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

# ── 4. Cài cron ──
echo ""
echo -e "${BLUE}[4/4] Cài đặt cron job...${NC}"

CRON_LINE="0 8 * * * $TRIGGER_SCRIPT >> $HOME/.openclaw/logs/cron-digest.log 2>&1"

# Xóa entry cũ nếu có
(crontab -l 2>/dev/null | grep -v "cron_trigger.sh" | grep -v "Daily Payment Digest") > /tmp/crontab_tmp || true

# Thêm entry mới
echo "" >> /tmp/crontab_tmp
echo "# 📰 Daily Payment Digest — 8:00 AM mỗi ngày" >> /tmp/crontab_tmp
echo "$CRON_LINE" >> /tmp/crontab_tmp

crontab /tmp/crontab_tmp
rm -f /tmp/crontab_tmp

mkdir -p "$HOME/.openclaw/logs"

echo -e "  ${GREEN}✅ Cron job: 8:00 AM mỗi ngày${NC}"

# ── Done ──
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "${GREEN}✅ HOÀN TẤT!${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Cách hoạt động:"
echo "  ⏰ 8:00 AM → cron gửi message đến OpenClaw bot"
echo "  🤖 OpenClaw nhận → chạy skill daily-payment-digest"
echo "  📰 Kết quả → gửi về Telegram cho bạn"
echo ""
echo "📌 Lệnh hữu ích:"
echo "  crontab -l                              # Xem cron"
echo "  bash $TRIGGER_SCRIPT                    # Test trigger"
echo "  crontab -l | grep -v cron_trigger | crontab -  # Xóa cron"
echo ""
