#!/bin/bash
# ============================================================
# DEBUG SCRIPT: Tại sao OpenClaw không nhận custom skills?
# Chạy trên VPS: bash debug-skills.sh
# ============================================================

echo "==========================================="
echo "🔍 OpenClaw Skills Debug - $(date)"
echo "==========================================="

echo ""
echo "📋 1. KIỂM TRA THƯ MỤC SKILLS"
echo "---"

# Check cả skills/ và skill/ (có case ghi sai)
for dir in ~/.openclaw/skills ~/.openclaw/skill ~/.openclaw/Skills; do
    if [ -d "$dir" ]; then
        echo "✅ TỒN TẠI: $dir"
        echo "   Nội dung:"
        ls -la "$dir/" 2>/dev/null
    else
        echo "❌ KHÔNG TỒN TẠI: $dir"
    fi
done

echo ""
echo "📋 2. TÌM TẤT CẢ SKILL.md"
echo "---"
echo "Trong ~/.openclaw/skills/:"
find ~/.openclaw/skills/ -name "SKILL.md" -type f 2>/dev/null | while read f; do
    size=$(wc -c < "$f")
    lines=$(wc -l < "$f")
    echo "  ✅ $f ($lines dòng, $size bytes)"
    # Show frontmatter
    echo "     Frontmatter:"
    head -5 "$f" | sed 's/^/     /'
done

echo ""
echo "Trong ~/.openclaw/ (toàn bộ):"
find ~/.openclaw/ -name "SKILL.md" -type f 2>/dev/null | sort

echo ""
echo "📋 3. KIỂM TRA CẤU TRÚC LỒNG NHAU (bug phổ biến)"
echo "---"
# Kiểm tra xem có bị lồng thư mục ko: skills/myclaw/blockchain-policy-research/
for nested in ~/.openclaw/skills/myclaw ~/.openclaw/skills/openclaw; do
    if [ -d "$nested" ]; then
        echo "⚠️ PHÁT HIỆN THƯ MỤC LỒNG NHAU: $nested"
        echo "   → Đây là BUG! Skills phải nằm trực tiếp trong ~/.openclaw/skills/"
        ls -la "$nested/"
    fi
done

# Kiểm tra skill đúng cấp
echo ""
echo "Kiểm tra cấp thư mục đúng:"
for skill_dir in ~/.openclaw/skills/*/; do
    skill_name=$(basename "$skill_dir")
    if [ -f "$skill_dir/SKILL.md" ]; then
        echo "  ✅ $skill_name/ — có SKILL.md"
    else
        echo "  ⚠️ $skill_name/ — KHÔNG có SKILL.md!"
        ls "$skill_dir" 2>/dev/null | head -5 | sed 's/^/     /'
    fi
done

echo ""
echo "📋 4. KIỂM TRA PERMISSIONS"
echo "---"
ls -la ~/.openclaw/skills/ 2>/dev/null | head -20
echo ""
echo "Owner của skills dir:"
stat -c '%U:%G %a' ~/.openclaw/skills/ 2>/dev/null || stat -f '%Su:%Sg %A' ~/.openclaw/skills/ 2>/dev/null

echo ""
echo "📋 5. KIỂM TRA FILE ENCODING (line endings)"
echo "---"
for f in $(find ~/.openclaw/skills/ -name "SKILL.md" -type f 2>/dev/null); do
    if file "$f" | grep -q "CRLF"; then
        echo "  ⚠️ CRLF (Windows): $f → Cần chạy: dos2unix $f"
    else
        echo "  ✅ LF (Unix): $f"
    fi
done

echo ""
echo "📋 6. KIỂM TRA FRONTMATTER YAML"
echo "---"
for f in $(find ~/.openclaw/skills/ -name "SKILL.md" -type f 2>/dev/null); do
    skill_name=$(basename $(dirname "$f"))
    first_line=$(head -1 "$f" | tr -d '\r\n')
    if [ "$first_line" = "---" ]; then
        # Check if has name field
        if head -10 "$f" | grep -q "^name:"; then
            name_val=$(head -10 "$f" | grep "^name:" | head -1)
            echo "  ✅ $skill_name — Frontmatter OK — $name_val"
        else
            echo "  ❌ $skill_name — Có --- nhưng THIẾU name: field!"
        fi
    else
        echo "  ❌ $skill_name — KHÔNG bắt đầu bằng --- (first line: '$first_line')"
    fi
done

echo ""
echo "📋 7. OPENCLAW CONFIG"
echo "---"
if [ -f ~/.openclaw/openclaw.json ]; then
    echo "✅ Có openclaw.json"
    echo "Nội dung (200 ký tự đầu):"
    head -c 200 ~/.openclaw/openclaw.json
    echo ""
    echo ""
    # Check for skills config
    if grep -q "skills" ~/.openclaw/openclaw.json; then
        echo "Skills config trong openclaw.json:"
        grep -A5 "skills" ~/.openclaw/openclaw.json
    else
        echo "⚠️ Không có 'skills' config trong openclaw.json"
    fi
else
    echo "❌ KHÔNG có openclaw.json!"
fi

echo ""
echo "📋 8. OPENCLAW VERSION & STATUS"
echo "---"
openclaw --version 2>/dev/null || echo "❌ openclaw command not found"
echo ""
echo "Gateway status:"
openclaw gateway status 2>/dev/null || echo "⚠️ Không kiểm tra được gateway status"

echo ""
echo "📋 9. KIỂM TRA SKILLS QUA OPENCLAW CLI"
echo "---"
echo "openclaw skills list:"
openclaw skills list 2>/dev/null || echo "⚠️ Command không khả dụng"

echo ""
echo "📋 10. LOGS GẦN NHẤT"
echo "---"
if [ -d ~/.openclaw/logs ]; then
    echo "Log files:"
    ls -lt ~/.openclaw/logs/ | head -5
    echo ""
    echo "50 dòng log cuối cùng:"
    tail -50 ~/.openclaw/logs/latest.log 2>/dev/null || \
    tail -50 $(ls -t ~/.openclaw/logs/*.log 2>/dev/null | head -1) 2>/dev/null || \
    echo "❌ Không tìm thấy file log"
else
    echo "❌ Không có thư mục logs"
fi

echo ""
echo "📋 11. KIỂM TRA PROCESS OPENCLAW"
echo "---"
ps aux | grep -i openclaw | grep -v grep

echo ""
echo "📋 12. SCREEN SESSIONS"
echo "---"
screen -ls 2>/dev/null || echo "⚠️ screen not found"

echo ""  
echo "==========================================="
echo "🏁 DEBUG HOÀN TẤT"
echo "==========================================="
echo ""
echo "📌 CÁC BƯỚC TIẾP THEO:"
echo "   1. Copy toàn bộ output trên gửi lại cho tôi"
echo "   2. Hoặc chạy lệnh sau để lưu: bash debug-skills.sh > debug-output.txt 2>&1"
echo "   3. Nếu thấy ❌ hoặc ⚠️ → đó là nguyên nhân!"
