---
name: deep-research-orchestrator
description: "Điều phối nghiên cứu Blockchain & Chính sách VN. Dùng search.py (KHÔNG Brave). Ghi báo cáo vào 1 file ~/research/report-YYYYMMDD.md."
---

# Deep Research Orchestrator

> ⚠️ Tìm kiếm bằng: `python3 ~/.openclaw/skills/web-search/scripts/search.py`. KHÔNG dùng Brave Search.
> 📄 Ghi TOÀN BỘ vào **1 file duy nhất**: `~/research/report-YYYYMMDD.md`

## MỤC TIÊU NGHIÊN CỨU

Tạo báo cáo nghiên cứu dựa trên nguồn công khai có kiểm chứng, trả lời 4 nhóm câu hỏi:

**A. Thị trường & Xu hướng:**
- Blockchain nổi bật ở mảng nào? (tài chính, thanh toán, định danh, chuỗi cung ứng, chứng từ điện tử, tokenization, CBDC, cross-border...)
- Xu hướng 12–24 tháng: permissioned vs public, tiêu chuẩn ISO/ITU/W3C, bảo mật/tuân thủ, tích hợp AI
- Pain points: minh bạch, chống gian lận, đối soát, traceability, tự động hóa liên tổ chức

**B. Chính sách Việt Nam:**
- Liệt kê văn bản chính thức liên quan blockchain (chỉ đạo, chiến lược, chương trình CĐSQG, đề án, sandbox)
- Mỗi văn bản: tên, số/ký hiệu, ngày, cơ quan, nội dung blockchain, tác động
- Phân biệt rõ: blockchain công nghệ vs tài sản số/tiền mã hóa

**C. Đà Nẵng Sandbox:**
- Kết luận rõ: CÓ hay CHƯA CÓ sandbox blockchain chính thức?
- Nếu CÓ: đề án, cơ sở pháp lý, đơn vị chủ trì, phạm vi, thời hạn, kết quả
- Nếu CHƯA: thông tin gần nhất (đề xuất/đang xây dựng) + nguồn xác thực

**D. Vai trò NAPAS (trung gian thanh toán):**
- Vai trò khả thi: hạ tầng, điều phối tiêu chuẩn, mạng permissioned, xác thực/định danh, đối soát, tokenization
- 3-5 kịch bản theo mức độ rủi ro (thấp/trung bình/cao)
- Mỗi kịch bản: lợi ích, rủi ro, phụ thuộc pháp lý, đối tác cần, KPI, lộ trình 30-60-90 ngày

## QUY TRÌNH THỰC HIỆN

### Phase 1: Chuẩn bị
```bash
mkdir -p ~/research
```

### Phase 2: Thu thập dữ liệu (PHẢI chạy ĐẦY ĐỦ các lệnh sau)

**Xu hướng thế giới:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "blockchain enterprise trends 2025 2026" --max 15
python3 ~/.openclaw/skills/web-search/scripts/search.py "blockchain use cases finance payment identity supply chain" --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "CBDC global status 2025" --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "tokenization real world assets RWA 2025" --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "blockchain interoperability standards ISO ITU" --max 10
```

**Xu hướng Việt Nam:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "xu hướng blockchain Việt Nam 2024 2025" --region vn-vi --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "ứng dụng blockchain doanh nghiệp Việt Nam" --region vn-vi --max 10
```

**Chính sách VN:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "chính sách blockchain Việt Nam quyết định nghị quyết" --region vn-vi --max 15
python3 ~/.openclaw/skills/web-search/scripts/search.py "NHNN blockchain DLT fintech sandbox" --region vn-vi --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "Bộ TT&TT blockchain chuyển đổi số" --region vn-vi --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "Quyết định 749 942 chuyển đổi số blockchain" --region vn-vi --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "nghị định tài sản ảo tiền mã hóa Việt Nam" --region vn-vi --max 10
```

**Đà Nẵng:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "Đà Nẵng blockchain sandbox thí điểm đề án" --region vn-vi --max 15
python3 ~/.openclaw/skills/web-search/scripts/search.py "Đà Nẵng thành phố thông minh blockchain" --region vn-vi --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "UBND Đà Nẵng Sở TT-TT blockchain" --region vn-vi --max 10
```

**NAPAS / Thanh toán:**
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "blockchain interbank payment settlement reconciliation" --max 10
python3 ~/.openclaw/skills/web-search/scripts/search.py "NAPAS blockchain thanh toán liên ngân hàng" --region vn-vi --max 10
```

### Phase 3: Đọc chi tiết nguồn quan trọng
Với mỗi URL quan trọng từ kết quả tìm kiếm:
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py --extract "https://url-quan-trong.com"
```

### Phase 4: Kiểm chứng nguồn (source-validator)
- Phân loại mỗi nguồn theo 5 tier
- Cross-check: dữ kiện quan trọng cần ≥ 2 nguồn
- Loại bỏ nguồn Tier 5 (social media, marketing crypto)
- Không tìm thấy nguồn → ghi "⚠️ Không tìm thấy nguồn chính thức"

### Phase 5: Viết báo cáo → GHI VÀO 1 FILE DUY NHẤT

Viết theo format trong skill `blockchain-policy-research`, rồi ghi tất cả vào 1 file:
```bash
cat > ~/research/report-$(date +%Y%m%d).md << 'EOF'
[TOÀN BỘ nội dung báo cáo — Executive Summary + 4 phần chính + phụ lục nguồn]
EOF
```

### Phase 6: Trả kết quả Telegram
1. Gửi tóm tắt ngắn (< 3000 ký tự): phát hiện chính + kết luận
2. Thông báo: "📄 Báo cáo đầy đủ: `~/research/report-YYYYMMDD.md`"
3. Hỏi user muốn xem phần nào chi tiết

## QUY TẮC NGUỒN
- **Ưu tiên**: chinhphu.vn, sbv.gov.vn, mic.gov.vn, thuvienphapluat.vn, bis.org, worldbank.org, imf.org
- **Chấp nhận**: vnexpress.net, tuoitre.vn, ledgerinsights.com, coindesk.com (secondary)
- **LOẠI BỎ**: social media, blog cá nhân, marketing crypto
- Ưu tiên thông tin mới nhất, nhưng trích cả văn bản nền tảng trước đó nếu là căn cứ chính sách
