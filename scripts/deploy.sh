#!/bin/bash
# ==============================================================================
# 🦞 MyClaw — Deploy Skills to OpenClaw
#
# Script tự động:
#   1. Clone repo (hoặc pull nếu đã có)
#   2. Copy skills vào ~/.openclaw/skills/
#   3. Fix line endings & permissions
#   4. Cài dependencies
#   5. Setup .env nếu chưa có
#
# Usage:
#   bash deploy.sh                  # Deploy từ GitHub
#   bash deploy.sh --local ./myclaw # Deploy từ thư mục local
#   bash deploy.sh --setup-env      # Deploy + setup .env
# ==============================================================================

set -e

# ── Colors ──
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# ── Config ──
REPO_URL="https://github.com/thonguyennapas/myclaw.git"
SKILLS_DIR="$HOME/.openclaw/skills"
TEMP_DIR="/tmp/myclaw-deploy"
SETUP_ENV=false
LOCAL_PATH=""

# Skills to deploy (thêm skill mới vào đây)
SKILLS=(
    "web-search"
    "daily-payment-digest"
    "deep-research"
)

# ── Parse Args ──
while [[ $# -gt 0 ]]; do
    case $1 in
        --local)
            LOCAL_PATH="$2"
            shift 2
            ;;
        --setup-env)
            SETUP_ENV=true
            shift
            ;;
        --help|-h)
            echo "Usage: bash deploy.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --local PATH    Deploy từ thư mục local thay vì GitHub"
            echo "  --setup-env     Tạo file .env từ template (interactive)"
            echo "  -h, --help      Hiện help"
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
echo -e "${CYAN}🦞 MyClaw — Skills Deployment${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ── Step 1: Get Source ──
echo -e "${BLUE}[1/5] Lấy source code...${NC}"

if [ -n "$LOCAL_PATH" ]; then
    # Deploy from local directory
    if [ ! -d "$LOCAL_PATH" ]; then
        echo -e "${RED}❌ Thư mục không tồn tại: $LOCAL_PATH${NC}"
        exit 1
    fi
    SOURCE_DIR="$LOCAL_PATH"
    echo -e "  ${GREEN}✅ Sử dụng thư mục local: $SOURCE_DIR${NC}"
else
    # Clone from GitHub
    rm -rf "$TEMP_DIR"
    echo -e "  📦 Cloning $REPO_URL..."
    git clone --depth 1 "$REPO_URL" "$TEMP_DIR" 2>/dev/null
    SOURCE_DIR="$TEMP_DIR"
    echo -e "  ${GREEN}✅ Clone thành công${NC}"
fi

# ── Step 2: Copy Skills ──
echo ""
echo -e "${BLUE}[2/5] Copy skills vào $SKILLS_DIR...${NC}"

mkdir -p "$SKILLS_DIR"

for skill in "${SKILLS[@]}"; do
    if [ -d "$SOURCE_DIR/$skill" ]; then
        cp -r "$SOURCE_DIR/$skill" "$SKILLS_DIR/"
        echo -e "  ${GREEN}✅ $skill${NC}"
    else
        echo -e "  ${YELLOW}⚠️  $skill — không tìm thấy, bỏ qua${NC}"
    fi
done

# ── Step 3: Fix Line Endings & Permissions ──
echo ""
echo -e "${BLUE}[3/5] Fix line endings & permissions...${NC}"

# Install dos2unix if needed
if command -v dos2unix &>/dev/null; then
    find "$SKILLS_DIR" -type f \( -name "*.md" -o -name "*.py" -o -name "*.sh" \) -exec dos2unix {} \; 2>/dev/null
    echo -e "  ${GREEN}✅ Line endings fixed (dos2unix)${NC}"
else
    echo -e "  ${YELLOW}⚠️  dos2unix chưa cài — chạy: sudo apt install dos2unix${NC}"
fi

chmod -R 755 "$SKILLS_DIR"
find "$SKILLS_DIR" -name "*.py" -exec chmod +x {} \;
find "$SKILLS_DIR" -name "*.sh" -exec chmod +x {} \;
echo -e "  ${GREEN}✅ Permissions set${NC}"

# ── Step 4: Install Dependencies ──
echo ""
echo -e "${BLUE}[4/5] Cài dependencies...${NC}"

# duckduckgo-search (tên package mới, cung cấp module duckduckgo_search + ddgs CLI)
if pip install duckduckgo-search 2>/dev/null; then
    echo -e "  ${GREEN}✅ duckduckgo-search installed${NC}"
elif pip install ddgs 2>/dev/null; then
    echo -e "  ${GREEN}✅ ddgs installed (legacy)${NC}"
else
    echo -e "  ${RED}❌ Không cài được search package — thử: pip3 install duckduckgo-search${NC}"
fi

# requests — dùng cho extract URL content
pip install requests 2>/dev/null && echo -e "  ${GREEN}✅ requests installed${NC}" || true

# ── Step 5: Setup .env ──
echo ""
echo -e "${BLUE}[5/5] Kiểm tra cấu hình .env...${NC}"

ENV_TARGET="$HOME/.openclaw/.env"

if [ -f "$ENV_TARGET" ]; then
    echo -e "  ${GREEN}✅ .env đã tồn tại: $ENV_TARGET${NC}"
elif [ "$SETUP_ENV" = true ]; then
    echo -e "  ${YELLOW}📝 Tạo .env mới...${NC}"

    # Copy template
    if [ -f "$SOURCE_DIR/.env.example" ]; then
        cp "$SOURCE_DIR/.env.example" "$ENV_TARGET"
    else
        cat > "$ENV_TARGET" << 'ENVEOF'
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.5-flash
LLM_API_KEY=
TELEGRAM_TOKEN=
TAVILY_API_KEY=
ENVEOF
    fi

    echo ""
    echo -e "  ${YELLOW}Cần điền các giá trị sau:${NC}"
    
    read -p "  LLM_API_KEY (Gemini API Key): " input_llm
    [ -n "$input_llm" ] && sed -i "s|LLM_API_KEY=.*|LLM_API_KEY=$input_llm|" "$ENV_TARGET"

    read -p "  TELEGRAM_TOKEN (Bot Token): " input_tg
    [ -n "$input_tg" ] && sed -i "s|TELEGRAM_TOKEN=.*|TELEGRAM_TOKEN=$input_tg|" "$ENV_TARGET"

    read -p "  TAVILY_API_KEY (optional, Enter để bỏ qua): " input_tv
    [ -n "$input_tv" ] && sed -i "s|TAVILY_API_KEY=.*|TAVILY_API_KEY=$input_tv|" "$ENV_TARGET"

    echo -e "  ${GREEN}✅ .env đã tạo: $ENV_TARGET${NC}"
else
    echo -e "  ${YELLOW}⚠️  Chưa có .env! Tạo bằng cách:${NC}"
    echo -e "     cp $SOURCE_DIR/.env.example $ENV_TARGET"
    echo -e "     nano $ENV_TARGET"
    echo -e "  ${YELLOW}   Hoặc chạy lại: bash deploy.sh --setup-env${NC}"
fi

# ── Cleanup ──
if [ -z "$LOCAL_PATH" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi

# ── Verify ──
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ DEPLOY HOÀN TẤT!${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "📋 Skills đã cài:"
find "$SKILLS_DIR" -maxdepth 2 -name "SKILL.md" | sort | while read f; do
    skill_name=$(basename "$(dirname "$f")")
    echo -e "  ✅ $skill_name"
done
echo ""
echo -e "📌 ${YELLOW}Bước tiếp theo:${NC}"
echo -e "  1. Kiểm tra .env:  cat $ENV_TARGET"
echo -e "  2. Start gateway:  bash scripts/start.sh"
echo -e "  3. Hoặc screen:    bash scripts/start.sh --screen"
echo ""
