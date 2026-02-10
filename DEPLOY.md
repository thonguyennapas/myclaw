# 🚀 Hướng dẫn Triển khai MyClaw Skills lên VPS

## Yêu cầu
- VPS đã cài OpenClaw
- OpenClaw chạy qua `screen` session với lệnh `openclaw gateway run`
- Git đã cài trên VPS
- Python 3.8+ trên VPS

## Thông tin cấu trúc

OpenClaw tìm skills ở 2 vị trí:

| Vị trí | Path | Ưu tiên |
|--------|------|---------|
| **Global** | `~/.openclaw/skills/` | Mặc định |
| **Workspace** | `<project>/skills/` | Cao hơn |

> **Khuyến nghị**: Sử dụng **Global** (`~/.openclaw/skills/`)

---

## ⚡ Triển khai Nhanh (Copy-Paste)

```bash
# 1. Clone & copy skills
cd /tmp && rm -rf myclaw
git clone https://github.com/thonguyennapas/myclaw.git
cp -r /tmp/myclaw/blockchain-policy-research ~/.openclaw/skills/
cp -r /tmp/myclaw/deep-research-orchestrator ~/.openclaw/skills/
cp -r /tmp/myclaw/source-validator ~/.openclaw/skills/
cp -r /tmp/myclaw/web-research-aggregator ~/.openclaw/skills/
cp -r /tmp/myclaw/web-search ~/.openclaw/skills/
cp -r /tmp/myclaw/daily-payment-digest ~/.openclaw/skills/
rm -rf /tmp/myclaw

# 2. Fix line endings & permissions
find ~/.openclaw/skills/ -type f \( -name "*.md" -o -name "*.py" \) -exec dos2unix {} \;
chmod -R 755 ~/.openclaw/skills/
chmod +x ~/.openclaw/skills/web-search/scripts/search.py
chmod +x ~/.openclaw/skills/blockchain-policy-research/scripts/research.py

# 3. Cài dependencies
pip install ddgs

# 4. Test web search
cd ~/.openclaw/skills/web-search && python3 scripts/search.py "blockchain Vietnam" --max 3

# 5. Restart OpenClaw (trong screen session)
screen -r
# Ctrl+C → chạy lại lệnh bên dưới → Ctrl+A D
```

---

## Triển khai Chi tiết (Step-by-Step)

### BƯỚC 1: SSH vào VPS

```bash
ssh YOUR_USER@YOUR_VPS_IP
```

### BƯỚC 2: Clone repo & Copy skills

```bash
cd /tmp
rm -rf myclaw
git clone https://github.com/thonguyennapas/myclaw.git

# Copy từng skill vào đúng vị trí
cp -r /tmp/myclaw/blockchain-policy-research ~/.openclaw/skills/
cp -r /tmp/myclaw/deep-research-orchestrator ~/.openclaw/skills/
cp -r /tmp/myclaw/source-validator ~/.openclaw/skills/
cp -r /tmp/myclaw/web-research-aggregator ~/.openclaw/skills/
cp -r /tmp/myclaw/web-search ~/.openclaw/skills/
cp -r /tmp/myclaw/daily-payment-digest ~/.openclaw/skills/

rm -rf /tmp/myclaw
```

> 📰 **Daily Payment Digest**: Xem hướng dẫn chi tiết tại `daily-payment-digest/DEPLOY.md`
> - **Option 1 (Chủ động)**: Nhắn Telegram "Tổng hợp tin tức thanh toán" → chạy ngay
> - **Option 2 (Cron)**: `bash ~/.openclaw/skills/daily-payment-digest/scripts/cron_setup.sh`

### BƯỚC 3: Kiểm tra cấu trúc

```bash
find ~/.openclaw/skills/ -name "SKILL.md" | sort
```

**Kết quả đúng:**
```
/home/YOUR_USER/.openclaw/skills/blockchain-policy-research/SKILL.md
/home/YOUR_USER/.openclaw/skills/deep-research-orchestrator/SKILL.md
/home/YOUR_USER/.openclaw/skills/source-validator/SKILL.md
/home/YOUR_USER/.openclaw/skills/web-research-aggregator/SKILL.md
/home/YOUR_USER/.openclaw/skills/web-search/SKILL.md
```

> ⚠️ **QUAN TRỌNG**: Mỗi `SKILL.md` phải nằm TRỰC TIẾP trong thư mục skill:
> - `~/.openclaw/skills/blockchain-policy-research/SKILL.md` ✅
> - `~/.openclaw/skills/myclaw/blockchain-policy-research/SKILL.md` ❌

### BƯỚC 4: Fix line endings (Windows → Linux)

```bash
sudo apt install dos2unix -y
find ~/.openclaw/skills/ -type f \( -name "*.md" -o -name "*.py" \) -exec dos2unix {} \;
```

### BƯỚC 5: Cài dependencies

```bash
pip install ddgs
```

**(Khuyến nghị) Đăng ký Tavily để có chất lượng search tốt nhất:**
1. Vào https://app.tavily.com/sign-in → đăng ký bằng email (30 giây)
2. Copy API key
3. Thêm vào lệnh chạy OpenClaw (Bước 8)

### BƯỚC 6: Cấp quyền

```bash
chmod -R 755 ~/.openclaw/skills/
chmod +x ~/.openclaw/skills/blockchain-policy-research/scripts/research.py
chmod +x ~/.openclaw/skills/web-search/scripts/search.py
```

### BƯỚC 7: Test web search

```bash
cd ~/.openclaw/skills/web-search
python3 scripts/search.py "blockchain Vietnam" --max 3
# Phải thấy kết quả tìm kiếm từ internet
```

### BƯỚC 8: Restart OpenClaw trong screen

```bash
screen -ls
screen -r

# Nhấn Ctrl+C để dừng OpenClaw

# Chạy lại (thêm TAVILY_API_KEY nếu đã đăng ký)
TAVILY_API_KEY="tvly-xxxxx" LLM_PROVIDER="gemini" LLM_MODEL="gemini-2.5-flash" LLM_API_KEY="YOUR_KEY" TELEGRAM_TOKEN="YOUR_TOKEN" openclaw gateway run

# Nhấn Ctrl+A rồi D để detach
```

### BƯỚC 9: Test qua Telegram

```
Tìm kiếm web về xu hướng blockchain 2025
```

Hoặc test research:
```
Nghiên cứu chính sách blockchain Việt Nam, tìm kiếm web và trích nguồn
```

---

## Cập nhật Skills (Lần sau)

```bash
# Trên máy Windows (PowerShell):
cd C:\Users\thonv\Desktop\napas\openclaw\myclaw
git add .
git commit -m "update: mô tả thay đổi"
git push origin main

# Trên VPS (SSH):
cd /tmp && rm -rf myclaw
git clone https://github.com/thonguyennapas/myclaw.git
cp -r /tmp/myclaw/blockchain-policy-research ~/.openclaw/skills/
cp -r /tmp/myclaw/deep-research-orchestrator ~/.openclaw/skills/
cp -r /tmp/myclaw/source-validator ~/.openclaw/skills/
cp -r /tmp/myclaw/web-research-aggregator ~/.openclaw/skills/
cp -r /tmp/myclaw/web-search ~/.openclaw/skills/
cp -r /tmp/myclaw/daily-payment-digest ~/.openclaw/skills/
rm -rf /tmp/myclaw
find ~/.openclaw/skills/ -type f \( -name "*.md" -o -name "*.py" \) -exec dos2unix {} \;

# Restart OpenClaw
screen -r
# Ctrl+C → chạy lại lệnh openclaw → Ctrl+A D
```

---

## Thêm Skill Mới (Tương lai)

Khi tạo skill mới, tuân theo mẫu:

```
myclaw/
└── ten-skill-moi/
    ├── SKILL.md           ← NGẮN GỌN (< 60 dòng)
    └── scripts/           ← (optional) Scripts thực thi
        └── tool.py
```

### Yêu cầu cho SKILL.md mới:
1. **Frontmatter ngắn**: `name` + `description` (1-2 câu)
2. **"Khi nào sử dụng"**: 3-5 bullet points
3. **"Cách thực hiện"**: Có lệnh `bash` cụ thể
4. **Tổng dưới 60 dòng** — quá dài sẽ bị context overflow

### Ví dụ SKILL.md tối thiểu:
```yaml
---
name: ten-skill-moi
description: "Mô tả ngắn gọn skill làm gì. 1-2 câu."
---

# Tên Skill

## Khi nào sử dụng
- Điều kiện 1
- Điều kiện 2

## Cách thực hiện
\```bash
python3 ~/.openclaw/skills/ten-skill-moi/scripts/tool.py "input"
\```
```

---

## Troubleshooting

### Skill không hoạt động trên Telegram?

**Nguyên nhân phổ biến:**
1. SKILL.md quá dài (> 100 dòng) → context overflow
2. Không có lệnh bash/python cụ thể → AI không biết chạy gì
3. Description trong frontmatter quá mơ hồ → AI không match skill

**Cách fix:**
```bash
# 1. Kiểm tra kích thước SKILL.md
wc -l ~/.openclaw/skills/*/SKILL.md

# 2. Kiểm tra frontmatter
head -5 ~/.openclaw/skills/blockchain-policy-research/SKILL.md

# 3. Test script trực tiếp
python3 ~/.openclaw/skills/web-search/scripts/search.py "test" --max 2

# 4. Xem logs
tail -100 ~/.openclaw/logs/latest.log 2>/dev/null
```

### Script Python lỗi?

```bash
cd ~/.openclaw/skills/web-search
python3 scripts/search.py --status
dos2unix scripts/search.py
```

### Screen session bị mất?

```bash
screen -S openclaw
LLM_PROVIDER="gemini" LLM_MODEL="gemini-2.5-flash" LLM_API_KEY="YOUR_KEY" TELEGRAM_TOKEN="YOUR_TOKEN" openclaw gateway run
# Detach: Ctrl+A rồi D
# Attach lại: screen -r openclaw
```

---

## Bảo mật

⚠️ **KHÔNG commit API keys vào Git!**

```bash
cat > ~/.openclaw/.env << 'EOF'
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.5-flash
LLM_API_KEY=your_key
TELEGRAM_TOKEN=your_token
TAVILY_API_KEY=tvly-xxxxx
EOF

cd ~/.openclaw && source .env && openclaw gateway run
```

---

📅 Cập nhật: 09/02/2026
🔧 Version: 2.0 — Refactored skills for OpenClaw compatibility
