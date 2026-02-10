#!/bin/bash
# ==============================================================================
# 🔍 MyClaw — Health Check
#
# Kiểm tra toàn bộ hệ thống trong 1 lệnh:
#   - .env loaded & valid
#   - Skills installed & formatted correctly
#   - Dependencies available
#   - Gateway running
#
# Usage: bash scripts/health-check.sh
# ==============================================================================

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

PASS=0
WARN=0
FAIL=0

check_pass() { echo -e "  ${GREEN}✅ $1${NC}"; PASS=$((PASS + 1)); }
check_warn() { echo -e "  ${YELLOW}⚠️  $1${NC}"; WARN=$((WARN + 1)); }
check_fail() { echo -e "  ${RED}❌ $1${NC}"; FAIL=$((FAIL + 1)); }

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}🔍 MyClaw Health Check — $(date '+%Y-%m-%d %H:%M')${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# ── 1. Environment File ──
echo ""
echo -e "${BLUE}📋 1. Environment Configuration${NC}"

ENV_FILE="$HOME/.openclaw/.env"
if [ -f "$ENV_FILE" ]; then
    check_pass ".env exists: $ENV_FILE"

    # Load and check variables
    source_env() {
        while IFS='=' read -r key value; do
            [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue
            key=$(echo "$key" | xargs)
            value=$(echo "$value" | xargs)
            value="${value%\"}"; value="${value#\"}"
            echo "$key"
        done < "$ENV_FILE"
    }

    VARS_SET=$(source_env)

    for var in LLM_PROVIDER LLM_MODEL LLM_API_KEY TELEGRAM_TOKEN; do
        if echo "$VARS_SET" | grep -q "^${var}$"; then
            val=$(grep "^${var}=" "$ENV_FILE" | head -1 | cut -d= -f2- | xargs)
            if [ -n "$val" ] && [[ "$val" != *"your_"* ]] && [[ "$val" != *"_here"* ]]; then
                check_pass "$var: configured"
            else
                check_fail "$var: empty or placeholder"
            fi
        else
            check_fail "$var: missing"
        fi
    done

    # Optional
    if grep -q "^TAVILY_API_KEY=" "$ENV_FILE"; then
        val=$(grep "^TAVILY_API_KEY=" "$ENV_FILE" | head -1 | cut -d= -f2- | xargs)
        if [ -n "$val" ] && [[ "$val" != *"your_"* ]]; then
            check_pass "TAVILY_API_KEY: configured"
        else
            check_warn "TAVILY_API_KEY: not set (using DuckDuckGo fallback)"
        fi
    else
        check_warn "TAVILY_API_KEY: not set (using DuckDuckGo fallback)"
    fi
else
    check_fail ".env not found — run: cp .env.example $ENV_FILE"
fi

# ── 2. Skills Installation ──
echo ""
echo -e "${BLUE}📋 2. Installed Skills${NC}"

SKILLS_DIR="$HOME/.openclaw/skills"
if [ -d "$SKILLS_DIR" ]; then
    check_pass "Skills directory: $SKILLS_DIR"

    EXPECTED_SKILLS=(
        "web-search"
        "daily-payment-digest"
        "deep-research"
    )

    for skill in "${EXPECTED_SKILLS[@]}"; do
        if [ -f "$SKILLS_DIR/$skill/SKILL.md" ]; then
            lines=$(wc -l < "$SKILLS_DIR/$skill/SKILL.md")
            if [ "$lines" -le 120 ]; then
                check_pass "$skill ($lines lines)"
            else
                check_warn "$skill ($lines lines — recommend < 60)"
            fi
        else
            check_fail "$skill — SKILL.md not found"
        fi
    done

    # Check for nested directory bug
    if [ -d "$SKILLS_DIR/myclaw" ]; then
        check_fail "Nested directory detected: $SKILLS_DIR/myclaw/ — should be flat!"
    fi
else
    check_fail "Skills directory not found: $SKILLS_DIR"
fi

# ── 3. SKILL.md Frontmatter ──
echo ""
echo -e "${BLUE}📋 3. SKILL.md Frontmatter${NC}"

for f in $(find "$SKILLS_DIR" -maxdepth 2 -name "SKILL.md" -type f 2>/dev/null | sort); do
    skill_name=$(basename "$(dirname "$f")")
    first_line=$(head -1 "$f" | tr -d '\r\n')
    if [ "$first_line" = "---" ]; then
        if head -10 "$f" | grep -q "^name:"; then
            check_pass "$skill_name — frontmatter OK"
        else
            check_fail "$skill_name — missing 'name:' in frontmatter"
        fi
    else
        check_fail "$skill_name — does not start with '---'"
    fi
done

# ── 4. Line Endings ──
echo ""
echo -e "${BLUE}📋 4. Line Endings${NC}"

CRLF_COUNT=0
for f in $(find "$SKILLS_DIR" -maxdepth 3 -name "SKILL.md" -type f 2>/dev/null); do
    if file "$f" | grep -q "CRLF"; then
        check_warn "CRLF: $f — run: dos2unix $f"
        CRLF_COUNT=$((CRLF_COUNT + 1))
    fi
done
if [ "$CRLF_COUNT" -eq 0 ]; then
    check_pass "All files use LF line endings"
fi

# ── 5. Dependencies ──
echo ""
echo -e "${BLUE}📋 5. Dependencies${NC}"

if command -v python3 &>/dev/null; then
    PY_VER=$(python3 --version 2>&1)
    check_pass "Python: $PY_VER"
else
    check_fail "Python3 not found"
fi

if python3 -c "import ddgs" 2>/dev/null || python3 -c "from duckduckgo_search import DDGS" 2>/dev/null; then
    check_pass "ddgs package installed"
else
    check_fail "ddgs not installed — run: pip install ddgs"
fi

if command -v openclaw &>/dev/null; then
    OC_VER=$(openclaw --version 2>&1 || echo "unknown")
    check_pass "OpenClaw: $OC_VER"
else
    check_fail "OpenClaw not found"
fi

if command -v dos2unix &>/dev/null; then
    check_pass "dos2unix: installed"
else
    check_warn "dos2unix: not installed (run: sudo apt install dos2unix)"
fi

# ── 6. Gateway Process ──
echo ""
echo -e "${BLUE}📋 6. Gateway Status${NC}"

if pgrep -f "openclaw gateway" >/dev/null 2>&1; then
    check_pass "Gateway is running"
else
    check_warn "Gateway is NOT running — start with: bash scripts/start.sh"
fi

if screen -ls 2>/dev/null | grep -q "openclaw"; then
    check_pass "Screen session 'openclaw' active"
else
    check_warn "No screen session — consider: bash scripts/start.sh --screen"
fi

# ── Summary ──
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
TOTAL=$((PASS + WARN + FAIL))
echo -e "📊 Results: ${GREEN}${PASS} pass${NC} | ${YELLOW}${WARN} warn${NC} | ${RED}${FAIL} fail${NC} (total: ${TOTAL})"

if [ $FAIL -eq 0 ] && [ $WARN -eq 0 ]; then
    echo -e "${GREEN}🎉 Everything looks great!${NC}"
elif [ $FAIL -eq 0 ]; then
    echo -e "${YELLOW}👍 Working, but has warnings${NC}"
else
    echo -e "${RED}⚠️  Has failures — fix above issues${NC}"
fi
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
