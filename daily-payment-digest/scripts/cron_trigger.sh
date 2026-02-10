#!/bin/bash
# ==============================================================================
# 📰 Daily Payment Digest — Cron Trigger cho OpenClaw
#
# Script này GỬI 1 TIN NHẮN đến OpenClaw Telegram Bot mỗi sáng 8h
# để trigger skill daily-payment-digest.
#
# Config: tất cả đọc từ ~/.openclaw/.env (unified config)
# ==============================================================================

# ── Load unified .env ──
ENV_FILE="$HOME/.openclaw/.env"

if [ -f "$ENV_FILE" ]; then
    set -a
    while IFS='=' read -r key value; do
        [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        value="${value%\"}"; value="${value#\"}"
        value="${value%\'}"; value="${value#\'}"
        export "$key=$value"
    done < "$ENV_FILE"
    set +a
fi

# Fallback: cũ-style env vars nếu có
BOT_TOKEN="${TELEGRAM_TOKEN:-${TELEGRAM_BOT_TOKEN:-}}"
CHAT_ID="${TELEGRAM_CHAT_ID:-${DIGEST_CHAT_ID:-}}"

# ── Validate ──
if [ -z "$BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_TOKEN chưa set"
    echo "   Cập nhật trong: $ENV_FILE"
    exit 1
fi

if [ -z "$CHAT_ID" ]; then
    echo "❌ TELEGRAM_CHAT_ID chưa set"
    echo "   Cập nhật trong: $ENV_FILE"
    echo ""
    echo "   💡 Lấy chat ID:"
    echo "   1. Nhắn gì đó cho bot trên Telegram"
    echo "   2. Mở: https://api.telegram.org/bot${BOT_TOKEN}/getUpdates"
    echo "   3. Tìm 'chat':{'id': XXXXXXX}"
    exit 1
fi

# ── Gửi message trigger đến OpenClaw bot ──
MESSAGE="${DIGEST_TRIGGER_MESSAGE:-Tạo bản tin thanh toán hôm nay}"

echo "📤 [$(date '+%Y-%m-%d %H:%M')] Gửi trigger đến OpenClaw bot..."
echo "   Message: $MESSAGE"
echo "   Chat ID: $CHAT_ID"

RESPONSE=$(curl -s -X POST \
    "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
    -H "Content-Type: application/json" \
    -d "{
        \"chat_id\": \"${CHAT_ID}\",
        \"text\": \"${MESSAGE}\"
    }")

# Kiểm tra kết quả
OK=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ok', False))" 2>/dev/null)

if [ "$OK" = "True" ]; then
    echo "✅ Đã gửi trigger thành công!"
    echo "   OpenClaw sẽ tự động chạy skill daily-payment-digest"
    echo "   và trả kết quả về Telegram cho bạn."
else
    echo "❌ Lỗi gửi: $RESPONSE"
    exit 1
fi
