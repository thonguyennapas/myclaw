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

## Triển khai Lần đầu (Step-by-Step)

### BƯỚC 1: SSH vào VPS

```bash
ssh YOUR_USER@YOUR_VPS_IP
```

### BƯỚC 2: Tạo thư mục skills & Clone repo

```bash
# Tạo thư mục nếu chưa có
mkdir -p ~/.openclaw/skills/

# Clone repo từ GitHub
cd /tmp
git clone https://github.com/thonguyennapas/myclaw.git

# Copy từng skill vào đúng vị trí (KHÔNG lồng thêm folder myclaw/)
cp -r /tmp/myclaw/blockchain-policy-research ~/.openclaw/skills/
cp -r /tmp/myclaw/deep-research-orchestrator ~/.openclaw/skills/
cp -r /tmp/myclaw/source-validator ~/.openclaw/skills/
cp -r /tmp/myclaw/web-research-aggregator ~/.openclaw/skills/
cp -r /tmp/myclaw/web-search ~/.openclaw/skills/

# Dọn dẹp
rm -rf /tmp/myclaw
```

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

### BƯỚC 5: Cài dependencies cho web search

```bash
pip install ddgs
```

**(Khuyến nghị) Đăng ký Tavily để có chất lượng search tốt nhất:**
1. Vào https://app.tavily.com/sign-in → đăng ký bằng email (30 giây)
2. Copy API key
3. Thêm vào lệnh chạy OpenClaw (Bước 8):
```bash
TAVILY_API_KEY="tvly-xxxxx" LLM_PROVIDER="gemini" ... openclaw gateway run
```

### BƯỚC 6: Cấp quyền

```bash
chmod -R 755 ~/.openclaw/skills/
chmod +x ~/.openclaw/skills/blockchain-policy-research/scripts/research.py
chmod +x ~/.openclaw/skills/web-search/scripts/search.py
```

### BƯỚC 7: Test web search hoạt động

```bash
cd ~/.openclaw/skills/web-search
python3 scripts/search.py "blockchain Vietnam" --max 3
# Phải thấy kết quả tìm kiếm từ internet
```

### BƯỚC 8: Restart OpenClaw trong screen

```bash
# Xem danh sách screen sessions
screen -ls

# Attach vào session đang chạy OpenClaw
screen -r

# Nhấn Ctrl+C để dừng OpenClaw

# Chạy lại
LLM_PROVIDER="gemini" LLM_MODEL="gemini-2.5-flash" LLM_API_KEY="YOUR_KEY" TELEGRAM_TOKEN="YOUR_TOKEN" openclaw gateway run

# Nhấn Ctrl+A rồi D để detach (thoát screen mà không tắt process)
```

### BƯỚC 9: Test qua Telegram

Gửi tin nhắn cho bot:
```
Hãy liệt kê tất cả skills bạn có
```

Hoặc test trực tiếp:
```
Sử dụng skill blockchain-policy-research, cho tôi xem bản đồ 10 xu hướng blockchain
```

---

## Cập nhật Skills (Lần sau)

Khi sửa skills trên máy Windows, push lên GitHub rồi chạy trên VPS:

```bash
# Trên máy Windows (PowerShell):
cd C:\Users\thonv\Desktop\napas\openclaw\myclaw
git add .
git commit -m "update: mô tả thay đổi"
git push origin main

# Trên VPS (SSH):
cd /tmp
rm -rf myclaw
git clone https://github.com/thonguyennapas/myclaw.git
cp -r /tmp/myclaw/blockchain-policy-research ~/.openclaw/skills/
cp -r /tmp/myclaw/deep-research-orchestrator ~/.openclaw/skills/
cp -r /tmp/myclaw/source-validator ~/.openclaw/skills/
cp -r /tmp/myclaw/web-research-aggregator ~/.openclaw/skills/
cp -r /tmp/myclaw/web-search ~/.openclaw/skills/
rm -rf /tmp/myclaw
find ~/.openclaw/skills/ -type f \( -name "*.md" -o -name "*.py" \) -exec dos2unix {} \;

# Restart OpenClaw trong screen
screen -r
# Ctrl+C → chạy lại lệnh openclaw → Ctrl+A D
```

---

## Thêm Skill Mới (Tương lai)

Khi tạo skill mới, chỉ cần:

1. Tạo thư mục mới trong `myclaw/` trên máy Windows:
   ```
   myclaw/
   └── ten-skill-moi/
       └── SKILL.md
   ```

2. Push lên GitHub
3. Trên VPS thêm 1 dòng copy:
   ```bash
   cp -r /tmp/myclaw/ten-skill-moi ~/.openclaw/skills/
   ```

---

## Troubleshooting

### Skill không được nhận?

```bash
# 1. Kiểm tra SKILL.md format
head -5 ~/.openclaw/skills/blockchain-policy-research/SKILL.md
# Phải thấy:
# ---
# name: blockchain-policy-research
# description: "..."
# ---

# 2. Kiểm tra quyền
ls -la ~/.openclaw/skills/blockchain-policy-research/SKILL.md

# 3. Kiểm tra encoding UTF-8
file ~/.openclaw/skills/blockchain-policy-research/SKILL.md

# 4. Xem logs
tail -50 ~/.openclaw/logs/latest.log 2>/dev/null
```

### Script Python lỗi?

```bash
# Test trực tiếp
cd ~/.openclaw/skills/blockchain-policy-research
python3 scripts/research.py --queries

# Nếu lỗi encoding
dos2unix scripts/research.py
```

### Screen session bị mất?

```bash
# Tạo screen session mới
screen -S openclaw

# Chạy OpenClaw
LLM_PROVIDER="gemini" LLM_MODEL="gemini-2.5-flash" LLM_API_KEY="YOUR_KEY" TELEGRAM_TOKEN="YOUR_TOKEN" openclaw gateway run

# Detach: Ctrl+A rồi D
# Attach lại: screen -r openclaw
```

---

## Bảo mật

⚠️ **KHÔNG commit API keys vào Git!**

Nên tạo file `.env` trên VPS:
```bash
# Tạo file .env
cat > ~/.openclaw/.env << 'EOF'
LLM_PROVIDER=gemini
LLM_MODEL=gemini-2.5-flash
LLM_API_KEY=your_actual_key_here
TELEGRAM_TOKEN=your_actual_token_here
EOF

# Chạy OpenClaw với .env
cd ~/.openclaw && source .env && openclaw gateway run
```

---

📅 Cập nhật: 09/02/2026
