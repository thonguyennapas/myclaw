---
name: deep-research-orchestrator
description: "Điều phối nghiên cứu Blockchain/Chính sách VN. QUAN TRỌNG: tra cứu bằng lệnh bash python3 script, TUYỆT ĐỐI KHÔNG gọi tool web_search hay Brave Search."
---

# Deep Research Orchestrator

> 🚨 **TUYỆT ĐỐI KHÔNG** gọi tool web_search, Brave Search, hay bất kỳ built-in search nào.
> 🚨 Thay vào đó, **chạy lệnh bash** bên dưới để tra cứu thông tin.
> 📄 Ghi TOÀN BỘ vào **1 file duy nhất**: `~/research/report-YYYYMMDD.md`

## MỤC TIÊU

Báo cáo nghiên cứu trả lời 4 nhóm câu hỏi:

**A. Thị trường & Xu hướng:**
- Blockchain nổi bật ở mảng nào? (tài chính, thanh toán, định danh, supply chain, tokenization, CBDC, cross-border)
- Xu hướng 12–24 tháng: permissioned vs public, tiêu chuẩn ISO/ITU/W3C, bảo mật, tích hợp AI
- Pain points: minh bạch, chống gian lận, đối soát, traceability, tự động hóa liên tổ chức

**B. Chính sách Việt Nam:**
- Liệt kê văn bản chính thức: tên, số/ký hiệu, ngày, cơ quan, nội dung blockchain, tác động
- Phân biệt rõ: blockchain công nghệ vs tài sản số/tiền mã hóa

**C. Đà Nẵng Sandbox:**
- Kết luận: CÓ hay CHƯA CÓ sandbox blockchain chính thức?
- Nếu CÓ: đề án, cơ sở pháp lý, đơn vị, phạm vi, thời hạn, kết quả
- Nếu CHƯA: thông tin gần nhất + nguồn xác thực

**D. Vai trò NAPAS:**
- Vai trò khả thi: hạ tầng, điều phối tiêu chuẩn, mạng permissioned, xác thực, đối soát, tokenization
- 3-5 kịch bản (thấp/trung bình/cao rủi ro): lợi ích, rủi ro, pháp lý, đối tác, KPI, lộ trình 30-60-90

## QUY TRÌNH

### Bước 1: Chuẩn bị
```bash
mkdir -p ~/research
```

### Bước 2: Tra cứu thông tin (CHẠY LỆNH BASH — KHÔNG gọi tool web_search)

**Xu hướng thế giới — chạy từng lệnh bash sau:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "blockchain enterprise trends 2025 2026" --max 15
```
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "blockchain use cases finance payment identity supply chain tokenization" --max 10
```
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "CBDC global status 2025 central bank digital currency" --max 10
```
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "tokenization real world assets RWA 2025" --max 10
```

**Xu hướng Việt Nam — chạy lệnh bash:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "xu hướng blockchain Việt Nam 2024 2025" --region vn-vi --max 10
```
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "ứng dụng blockchain doanh nghiệp Việt Nam" --region vn-vi --max 10
```

**Chính sách VN — chạy lệnh bash:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "chính sách blockchain Việt Nam quyết định nghị quyết" --region vn-vi --max 15
```
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "NHNN blockchain DLT fintech sandbox" --region vn-vi --max 10
```
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "Quyết định 749 942 chuyển đổi số blockchain" --region vn-vi --max 10
```
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "nghị định tài sản ảo tiền mã hóa Việt Nam" --region vn-vi --max 10
```

**Đà Nẵng — chạy lệnh bash:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "Đà Nẵng blockchain sandbox thí điểm đề án" --region vn-vi --max 15
```
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "UBND Đà Nẵng Sở TT-TT blockchain thành phố thông minh" --region vn-vi --max 10
```

**NAPAS — chạy lệnh bash:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "blockchain interbank payment settlement reconciliation" --max 10
```
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "NAPAS blockchain thanh toán liên ngân hàng" --region vn-vi --max 10
```

### Bước 3: Đọc chi tiết nguồn quan trọng (chạy bash)
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py --extract "https://url-quan-trong.com"
```

### Bước 4: Kiểm chứng nguồn (source-validator)
- Phân loại 5 tier, cross-check ≥ 2 nguồn, loại Tier 5
- Không có nguồn → "⚠️ Không tìm thấy nguồn chính thức"

### Bước 5: Viết báo cáo theo skill blockchain-policy-research → ghi 1 file
```bash
cat > ~/research/report-$(date +%Y%m%d).md << 'EOF'
[TOÀN BỘ: Executive Summary + Phần A + B + C + D + Phụ lục nguồn]
EOF
```

### Bước 6: Trả Telegram
1. Tóm tắt ngắn (< 3000 ký tự)
2. "📄 Báo cáo đầy đủ: ~/research/report-YYYYMMDD.md"
3. Hỏi user xem phần nào chi tiết

## QUY TẮC NGUỒN
- Ưu tiên: chinhphu.vn, sbv.gov.vn, mic.gov.vn, bis.org, worldbank.org
- LOẠI BỎ: social media, blog cá nhân, marketing crypto
