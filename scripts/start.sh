#!/bin/bash
# ==============================================================================
# 🦞 MyClaw — Start OpenClaw Gateway
#
# Tự động load biến môi trường từ .env và khởi chạy gateway.
# KHÔNG CẦN gõ key trực tiếp trên command line nữa!
#
# Usage:
#   bash scripts/start.sh              # Load từ ~/.openclaw/.env (mặc định)
#   bash scripts/start.sh --env /path  # Load từ file .env custom
#   bash scripts/start.sh --screen     # Chạy trong screen session
# ==============================================================================

set -e

# ── Colors ──
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ── Parse Arguments ──
ENV_FILE=""
USE_SCREEN=false
SCREEN_NAME="openclaw"

while [[ $# -gt 0 ]]; do
    case $1 in
        --env)
            ENV_FILE="$2"
            shift 2
            ;;
        --screen)
            USE_SCREEN=true
            shift
            ;;
        --screen-name)
            SCREEN_NAME="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: bash scripts/start.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --env FILE        Đường dẫn file .env (mặc định: ~/.openclaw/.env)"
            echo "  --screen          Chạy trong screen session"
            echo "  --screen-name     Tên screen session (mặc định: openclaw)"
            echo "  -h, --help        Hiện help"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# ── Banner ──
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🦞 MyClaw — OpenClaw Gateway Launcher${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ── Find .env file ──
if [ -n "$ENV_FILE" ]; then
    # User provided explicit path
    if [ ! -f "$ENV_FILE" ]; then
        echo -e "${RED}❌ File .env không tồn tại: $ENV_FILE${NC}"
        exit 1
    fi
else
    # Auto-detect .env location (ưu tiên từ cao → thấp)
    ENV_SEARCH_PATHS=(
        "$HOME/.openclaw/.env"
        "$(dirname "$(dirname "$(realpath "$0")")")/.env"
        "./.env"
    )

    for path in "${ENV_SEARCH_PATHS[@]}"; do
        if [ -f "$path" ]; then
            ENV_FILE="$path"
            break
        fi
    done
fi

if [ -z "$ENV_FILE" ]; then
    echo -e "${RED}❌ Không tìm thấy file .env!${NC}"
    echo ""
    echo -e "${YELLOW}Tạo file .env từ template:${NC}"
    echo -e "  cp .env.example ~/.openclaw/.env"
    echo -e "  nano ~/.openclaw/.env"
    echo ""
    echo -e "${YELLOW}Hoặc chỉ định đường dẫn:${NC}"
    echo -e "  bash scripts/start.sh --env /path/to/.env"
    exit 1
fi

echo -e "${BLUE}📂 Loading .env: ${ENV_FILE}${NC}"

# ── Load .env ── (export mỗi biến, bỏ comments và dòng trống)
set -a
while IFS='=' read -r key value; do
    # Bỏ dòng trống, comments, dòng chỉ có space
    [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue

    # Trim whitespace
    key=$(echo "$key" | xargs)
    value=$(echo "$value" | xargs)

    # Bỏ quotes bao quanh value nếu có
    value="${value%\"}"
    value="${value#\"}"
    value="${value%\'}"
    value="${value#\'}"

    export "$key=$value"
done < "$ENV_FILE"
set +a

# ── Validate Required Variables ──
echo -e "${BLUE}🔍 Checking required environment variables...${NC}"

MISSING=0

check_var() {
    local var_name=$1
    local var_label=$2
    local var_value="${!var_name}"

    if [ -z "$var_value" ] || [[ "$var_value" == *"your_"* ]] || [[ "$var_value" == *"_here"* ]]; then
        echo -e "  ${RED}❌ ${var_label} (${var_name})${NC}"
        MISSING=$((MISSING + 1))
    else
        # Mask sensitive values
        local masked="${var_value:0:6}...${var_value: -4}"
        echo -e "  ${GREEN}✅ ${var_label}: ${masked}${NC}"
    fi
}

check_var "LLM_PROVIDER"   "LLM Provider"
check_var "LLM_MODEL"      "LLM Model"
check_var "LLM_API_KEY"    "LLM API Key"
check_var "TELEGRAM_TOKEN" "Telegram Token"

echo ""

# Optional vars
if [ -n "$TAVILY_API_KEY" ] && [[ "$TAVILY_API_KEY" != *"your_"* ]]; then
    local_masked="${TAVILY_API_KEY:0:8}..."
    echo -e "  ${GREEN}✅ Tavily API Key: ${local_masked}${NC}"
else
    echo -e "  ${YELLOW}⚠️  Tavily API Key: chưa set (search fallback sang DuckDuckGo)${NC}"
fi

echo ""

if [ $MISSING -gt 0 ]; then
    echo -e "${RED}❌ Thiếu ${MISSING} biến bắt buộc! Cập nhật file .env:${NC}"
    echo -e "  nano $ENV_FILE"
    exit 1
fi

# ── Start Gateway ──
echo -e "${GREEN}🚀 Starting OpenClaw Gateway...${NC}"
echo -e "${BLUE}   Provider: ${LLM_PROVIDER} | Model: ${LLM_MODEL}${NC}"
echo -e "${BLUE}   Channel:  Telegram${NC}"
echo ""

if [ "$USE_SCREEN" = true ]; then
    echo -e "${YELLOW}📺 Chạy trong screen session: ${SCREEN_NAME}${NC}"
    echo -e "${YELLOW}   Detach: Ctrl+A → D${NC}"
    echo -e "${YELLOW}   Attach: screen -r ${SCREEN_NAME}${NC}"
    echo ""

    # Kill existing screen session if exists
    screen -X -S "$SCREEN_NAME" quit 2>/dev/null || true

    screen -dmS "$SCREEN_NAME" bash -c "
        set -a
        source $ENV_FILE
        set +a
        openclaw gateway run
    "

    echo -e "${GREEN}✅ Gateway đang chạy trong background!${NC}"
    echo -e "   screen -r ${SCREEN_NAME}   # Xem logs"
else
    # Run in foreground
    openclaw gateway run
fi
