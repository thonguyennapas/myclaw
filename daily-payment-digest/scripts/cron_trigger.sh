#!/bin/bash
# ==============================================================================
# 📰 Daily Payment Digest — Cron Trigger
#
# Chạy digest.py TRỰC TIẾP rồi gửi kết quả qua Telegram API.
#
# Flow:
#   cron → cron_trigger.sh → python3 digest.py → file digest
#     → đọc file → chia nhỏ → gửi qua Telegram sendMessage API
#
# Config: tất cả đọc từ ~/.openclaw/.env
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIGEST_SCRIPT="$SCRIPT_DIR/digest.py"
LOG_PREFIX="[$(date '+%Y-%m-%d %H:%M:%S')]"

# ── Load unified .env ──
ENV_FILE="$HOME/.openclaw/.env"

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
    echo "$LOG_PREFIX ❌ File .env không tìm thấy: $ENV_FILE"
    exit 1
fi

# Fallback: cũ-style env vars nếu có
BOT_TOKEN="${TELEGRAM_TOKEN:-${TELEGRAM_BOT_TOKEN:-}}"
CHAT_ID="${TELEGRAM_CHAT_ID:-${DIGEST_CHAT_ID:-}}"

# ── Validate ──
if [ -z "$BOT_TOKEN" ]; then
    echo "$LOG_PREFIX ❌ TELEGRAM_TOKEN chưa set trong $ENV_FILE"
    exit 1
fi

if [ -z "$CHAT_ID" ]; then
    echo "$LOG_PREFIX ❌ TELEGRAM_CHAT_ID chưa set trong $ENV_FILE"
    echo "   💡 Lấy chat ID:"
    echo "   1. Nhắn gì đó cho bot trên Telegram"
    echo "   2. Mở: https://api.telegram.org/bot${BOT_TOKEN}/getUpdates"
    echo "   3. Tìm 'chat':{'id': XXXXXXX}"
    exit 1
fi

# ── Step 1: Chạy digest.py ──
echo "$LOG_PREFIX 📰 Bắt đầu tạo bản tin..."

if [ ! -f "$DIGEST_SCRIPT" ]; then
    echo "$LOG_PREFIX ❌ Không tìm thấy digest.py: $DIGEST_SCRIPT"
    exit 1
fi

# Chạy digest.py, bắt exit code
python3 "$DIGEST_SCRIPT" 2>&1 | tail -20
DIGEST_EXIT=${PIPESTATUS[0]}

if [ $DIGEST_EXIT -ne 0 ]; then
    echo "$LOG_PREFIX ❌ digest.py thất bại (exit code: $DIGEST_EXIT)"
    # Gửi thông báo lỗi về Telegram
    curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -H "Content-Type: application/json" \
        -d "{\"chat_id\": \"${CHAT_ID}\", \"text\": \"⚠️ Daily Digest lỗi lúc $(date '+%H:%M %d/%m'). Kiểm tra log: ~/.openclaw/logs/cron-digest.log\"}" \
        > /dev/null
    exit 1
fi

# ── Step 2: Đọc file digest ──
TODAY=$(date +%Y-%m-%d)
DIGEST_OUTPUT_DIR="${DIGEST_OUTPUT_DIR:-$HOME/digests}"
# Expand ~ nếu có
DIGEST_OUTPUT_DIR="${DIGEST_OUTPUT_DIR/#\~/$HOME}"
DIGEST_FILE="$DIGEST_OUTPUT_DIR/digest-${TODAY}.md"

if [ ! -f "$DIGEST_FILE" ]; then
    echo "$LOG_PREFIX ❌ File digest không tìm thấy: $DIGEST_FILE"
    exit 1
fi

DIGEST_CONTENT=$(cat "$DIGEST_FILE")
DIGEST_LEN=${#DIGEST_CONTENT}
echo "$LOG_PREFIX 📄 File: $DIGEST_FILE ($DIGEST_LEN ký tự)"

# ── Step 3: Gửi qua Telegram ──
# Telegram giới hạn 4096 ký tự mỗi message
MAX_LEN=4000

send_telegram() {
    local text="$1"
    local response
    response=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
        -H "Content-Type: application/json" \
        --data-binary @- <<EOF
{
    "chat_id": "${CHAT_ID}",
    "text": $(python3 -c "import json,sys; print(json.dumps(sys.stdin.read()))" <<< "$text"),
    "disable_web_page_preview": true
}
EOF
    )
    
    local ok
    ok=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin).get('ok', False))" 2>/dev/null)
    
    if [ "$ok" = "True" ]; then
        return 0
    else
        echo "$LOG_PREFIX ⚠️ Gửi lỗi: $response"
        return 1
    fi
}

if [ $DIGEST_LEN -le $MAX_LEN ]; then
    # Nội dung ngắn → gửi 1 lần
    echo "$LOG_PREFIX 📤 Gửi 1 message..."
    send_telegram "$DIGEST_CONTENT"
else
    # Nội dung dài → chia theo dấu ┈┈┈ (section separator)
    echo "$LOG_PREFIX 📤 Chia nhỏ và gửi nhiều messages..."

    # Tạo temp file để split
    TEMP_DIR=$(mktemp -d)
    
    # Sử dụng Python để split thông minh
    python3 - "$DIGEST_FILE" "$TEMP_DIR" "$MAX_LEN" << 'PYEOF'
import sys, os

digest_file = sys.argv[1]
temp_dir = sys.argv[2]
max_len = int(sys.argv[3])

with open(digest_file, "r", encoding="utf-8") as f:
    content = f.read()

# Split theo dấu ┈┈┈ (section separator)
sections = content.split("┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈")

chunks = []
current = ""

for section in sections:
    section = section.strip()
    if not section:
        continue
    
    # Thêm lại separator
    piece = "┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈\n" + section + "\n"
    
    if len(current) + len(piece) > max_len:
        if current:
            chunks.append(current)
        current = piece
    else:
        current += piece

if current:
    chunks.append(current)

# Nếu không split được theo sections, split theo lines
if not chunks:
    lines = content.split("\n")
    current = ""
    for line in lines:
        if len(current) + len(line) + 1 > max_len:
            chunks.append(current)
            current = line + "\n"
        else:
            current += line + "\n"
    if current:
        chunks.append(current)

# Ghi ra files
for i, chunk in enumerate(chunks):
    with open(os.path.join(temp_dir, f"part_{i:02d}.txt"), "w", encoding="utf-8") as f:
        f.write(chunk)

print(len(chunks))
PYEOF

    PART_COUNT=$(ls "$TEMP_DIR"/part_*.txt 2>/dev/null | wc -l)
    echo "$LOG_PREFIX 📦 Chia thành $PART_COUNT phần"

    SENT=0
    for part_file in $(ls "$TEMP_DIR"/part_*.txt 2>/dev/null | sort); do
        PART_CONTENT=$(cat "$part_file")
        SENT=$((SENT + 1))
        echo "$LOG_PREFIX 📤 Gửi phần $SENT/$PART_COUNT..."
        send_telegram "$PART_CONTENT"
        
        # Delay giữa các message để tránh rate limit
        if [ $SENT -lt $PART_COUNT ]; then
            sleep 1
        fi
    done

    # Cleanup
    rm -rf "$TEMP_DIR"
fi

echo "$LOG_PREFIX ✅ Hoàn tất! Đã gửi bản tin về Telegram."
