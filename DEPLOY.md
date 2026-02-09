# 🚀 Hướng dẫn Triển khai MyClaw Skills lên VPS

## Thông tin cần biết

### Cấu trúc thư mục OpenClaw trên VPS
OpenClaw cài đặt skills theo 2 cách:

| Vị trí | Path | Ưu tiên |
|--------|------|---------|
| **Global** (cho toàn bộ projects) | `~/.openclaw/skills/` | Thấp |
| **Workspace** (cho 1 project cụ thể) | `<project>/skills/` | Cao |

> **Khuyến nghị**: Sử dụng **Global** (`~/.openclaw/skills/`) để tất cả conversations đều dùng được.

---

## Step-by-Step Triển khai

### BƯỚC 1: Nén thư mục myclaw trên máy Windows

Mở PowerShell trên máy local:

```powershell
# Di chuyên đến thư mục openclaw
cd C:\Users\thonv\Desktop\napas\openclaw

# Nén toàn bộ myclaw thành file zip
Compress-Archive -Path .\myclaw\* -DestinationPath .\myclaw-skills.zip -Force

# Kiểm tra file zip đã tạo
dir myclaw-skills.zip
```

---

### BƯỚC 2: Upload lên VPS

```powershell
# SCP upload lên VPS (thay YOUR_VPS_IP và YOUR_USER cho đúng)
scp myclaw-skills.zip YOUR_USER@YOUR_VPS_IP:/tmp/myclaw-skills.zip
```

Hoặc nếu dùng SSH key:
```powershell
scp -i "C:\path\to\your\key.pem" myclaw-skills.zip YOUR_USER@YOUR_VPS_IP:/tmp/myclaw-skills.zip
```

---

### BƯỚC 3: SSH vào VPS

```powershell
ssh YOUR_USER@YOUR_VPS_IP
```

---

### BƯỚC 4: Tạo thư mục skills (nếu chưa có)

```bash
# Kiểm tra OpenClaw đã cài đúng chưa
ls ~/.openclaw/

# Tạo thư mục skills nếu chưa có
mkdir -p ~/.openclaw/skills/
```

---

### BƯỚC 5: Giải nén skills vào đúng vị trí

```bash
# Giải nén từ /tmp vào thư mục skills
cd ~/.openclaw/skills/
unzip /tmp/myclaw-skills.zip

# Xóa file zip tạm
rm /tmp/myclaw-skills.zip
```

---

### BƯỚC 6: Kiểm tra cấu trúc đã đúng

```bash
# Xem cấu trúc thư mục
find ~/.openclaw/skills/ -name "SKILL.md" | sort
```

**Kết quả mong muốn:**
```
/home/YOUR_USER/.openclaw/skills/blockchain-policy-research/SKILL.md
/home/YOUR_USER/.openclaw/skills/deep-research-orchestrator/SKILL.md
/home/YOUR_USER/.openclaw/skills/source-validator/SKILL.md
/home/YOUR_USER/.openclaw/skills/web-research-aggregator/SKILL.md
```

> ⚠️ **QUAN TRỌNG**: Mỗi `SKILL.md` phải nằm TRỰC TIẾP trong thư mục skill, 
> KHÔNG phải trong subfolder `myclaw/`. Tức là path phải là:
> `~/.openclaw/skills/blockchain-policy-research/SKILL.md` ✅
> KHÔNG phải: `~/.openclaw/skills/myclaw/blockchain-policy-research/SKILL.md` ❌

Nếu cấu trúc bị sai (có thêm folder `myclaw/`), sửa lại:
```bash
# Nếu bị lồng thêm thư mục myclaw/
cd ~/.openclaw/skills/
mv myclaw/* ./ 2>/dev/null
rmdir myclaw 2>/dev/null
# Xóa README.md ở root (chỉ giữ SKILL.md trong từng skill)
rm -f ~/.openclaw/skills/README.md
```

---

### BƯỚC 7: Đặt quyền truy cập

```bash
# Đảm bảo OpenClaw có thể đọc tất cả files
chmod -R 755 ~/.openclaw/skills/

# Nếu có scripts Python, cấp quyền thực thi
chmod +x ~/.openclaw/skills/blockchain-policy-research/scripts/research.py
```

---

### BƯỚC 8: Cài dependencies cho scripts (nếu cần)

```bash
# Script research.py chỉ dùng thư viện chuẩn Python, không cần pip install gì thêm
# Kiểm tra Python có sẵn
python3 --version

# Test chạy script tạo template
cd ~/.openclaw/skills/blockchain-policy-research
python3 scripts/research.py --full --output ./reports
```

---

### BƯỚC 9: Restart OpenClaw (nếu đang chạy)

```bash
# Kiểm tra OpenClaw có đang chạy không
# (Lệnh khác nhau tùy cách bạn cài OpenClaw)

# Nếu chạy bằng systemd:
sudo systemctl restart openclaw

# Nếu chạy bằng Docker:
docker restart openclaw

# Nếu chạy bằng process:
# Kill process cũ rồi khởi động lại
```

---

### BƯỚC 10: Kiểm tra skills đã được nhận

Mở Telegram bot và gửi một trong các tin nhắn test:

```
Xin chào, hãy liệt kê tất cả skills bạn có thể sử dụng
```

Hoặc:
```
Sử dụng skill blockchain-policy-research, cho tôi xem bản đồ xu hướng blockchain
```

Hoặc:
```
/research full
```

---

## Kiểm tra Nhanh (Troubleshooting)

### Skill không được nhận?

```bash
# 1. Kiểm tra SKILL.md có đúng format không
head -5 ~/.openclaw/skills/blockchain-policy-research/SKILL.md
# Phải thấy:
# ---
# name: blockchain-policy-research
# description: "..."
# ---

# 2. Kiểm tra quyền file
ls -la ~/.openclaw/skills/blockchain-policy-research/SKILL.md

# 3. Kiểm tra encoding (phải là UTF-8)
file ~/.openclaw/skills/blockchain-policy-research/SKILL.md

# 4. Kiểm tra OpenClaw logs
# (path log tùy cách cài đặt)
tail -50 ~/.openclaw/logs/latest.log
```

### Script Python lỗi?

```bash
# Test trực tiếp
cd ~/.openclaw/skills/blockchain-policy-research
python3 scripts/research.py --queries

# Nếu lỗi encoding (Windows → Linux):
# Convert line endings từ CRLF sang LF
sudo apt install dos2unix  # Ubuntu/Debian
dos2unix scripts/research.py
```

---

## Cập nhật Skills sau này

Khi bạn sửa skills trên máy Windows và muốn cập nhật lên VPS:

```powershell
# Trên máy Windows:
cd C:\Users\thonv\Desktop\napas\openclaw
Compress-Archive -Path .\myclaw\* -DestinationPath .\myclaw-skills.zip -Force
scp myclaw-skills.zip YOUR_USER@YOUR_VPS_IP:/tmp/myclaw-skills.zip

# Trên VPS:
cd ~/.openclaw/skills/
unzip -o /tmp/myclaw-skills.zip  # -o = overwrite
rm /tmp/myclaw-skills.zip
# Restart OpenClaw nếu cần
```

### Hoặc dùng Git (Khuyến nghị cho lâu dài):

```bash
# Trên VPS, lần đầu:
cd ~/.openclaw/skills/
git init
git remote add origin https://github.com/YOUR_USER/myclaw-skills.git

# Lần sau chỉ cần:
cd ~/.openclaw/skills/
git pull origin main
```

---

## Tóm tắt Nhanh (TL;DR)

```powershell
# === MÁY WINDOWS ===
cd C:\Users\thonv\Desktop\napas\openclaw
Compress-Archive -Path .\myclaw\* -DestinationPath .\myclaw-skills.zip -Force
scp myclaw-skills.zip USER@VPS_IP:/tmp/

# === TRÊN VPS (SSH) ===
mkdir -p ~/.openclaw/skills/
cd ~/.openclaw/skills/
unzip /tmp/myclaw-skills.zip
# Sửa cấu trúc nếu bị lồng thêm folder myclaw/
mv myclaw/* ./ 2>/dev/null; rmdir myclaw 2>/dev/null; rm -f README.md
chmod -R 755 ~/.openclaw/skills/
# Restart OpenClaw
# Test qua Telegram bot
```
