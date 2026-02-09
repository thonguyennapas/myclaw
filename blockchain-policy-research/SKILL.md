---
name: blockchain-policy-research
description: "Viết báo cáo Blockchain/chính sách VN 5 phần. Tra cứu bằng lệnh bash python3 script. TUYỆT ĐỐI KHÔNG gọi tool web_search hay Brave Search."
---

# Blockchain Policy Research — Viết báo cáo

> 🚨 **TUYỆT ĐỐI KHÔNG** gọi tool web_search, Brave Search, hay built-in search.
> 🚨 Tra cứu bằng lệnh bash: `python3 ~/.openclaw/skills/web-search/scripts/search.py`
> 📄 Ghi TOÀN BỘ vào **1 file duy nhất**. KHÔNG tách nhiều file.

## QUY TẮC VÀNG
1. **KHÔNG bịa** — Mọi dữ kiện phải kèm nguồn (link)
2. Không có nguồn → ghi: "⚠️ Không tìm thấy nguồn chính thức để xác nhận"
3. Phân biệt rõ: blockchain công nghệ vs tài sản số/tiền mã hóa
4. Ưu tiên thông tin mới nhất, nhưng vẫn trích văn bản nền tảng trước đó

## CẤU TRÚC BÁO CÁO (ghi theo đúng thứ tự này)

### PHẦN 0: EXECUTIVE SUMMARY (1–2 trang)
- Kết luận chính cho mỗi nhóm (A, B, C, D)
- Top 3 cơ hội quan trọng nhất
- Đề xuất hành động cụ thể (30-60-90 ngày)
- Bảng tóm tắt:
  | Hạng mục | Kết luận | Hành động đề xuất |
  |----------|---------|-------------------|

### PHẦN A: BẢN ĐỒ XU HƯỚNG BLOCKCHAIN (thế giới + VN)

**Bảng 5-10 xu hướng lớn:**
| # | Xu hướng | Mô tả (2-3 câu) | Mảng ứng dụng | Mức trưởng thành | Tác động với VN | Nguồn |
|---|---------|-----------------|---------------|------------------|-----------------|-------|

**Nội dung bắt buộc:**
- Blockchain nổi bật ở mảng nào: tài chính, thanh toán, định danh, chuỗi cung ứng, chứng từ điện tử, tokenization, CBDC, cross-border
- Xu hướng 12-24 tháng: permissioned vs public, tiêu chuẩn ISO/ITU/W3C, bảo mật/tuân thủ, tích hợp AI/agentic
- Pain points phổ biến: minh bạch, chống gian lận, đối soát, traceability, tự động hóa liên tổ chức
- Dòng vốn đầu tư vào blockchain enterprise (nếu tìm thấy số liệu)

### PHẦN B: CHÍNH SÁCH & VĂN BẢN PHÁP LÝ VIỆT NAM

**Bảng văn bản (PHẢI có đầy đủ các cột):**
| # | Tên văn bản | Số/Ký hiệu | Ngày ban hành | Cơ quan ban hành | Nội dung liên quan blockchain | Tác động/Ý nghĩa | Link nguồn |
|---|------------|------------|---------------|-----------------|------------------------------|-------------------|-----------|

**Nội dung bắt buộc:**
- Văn bản cấp Thủ tướng (QĐ 749, QĐ 942, NQ 52...)
- Văn bản NHNN (chỉ thị crypto, sandbox fintech, chiến lược fintech, CBDC)
- Văn bản Bộ TT&TT (chuyển đổi số, blockchain strategy)
- Dự thảo nghị định tài sản số / tiền mã hóa (nếu có)
- **Phân định rõ** (viết 1 đoạn riêng):
  - Chính sách blockchain như **công nghệ** (DLT, smart contract, traceability)
  - Chính sách **tài sản số/tiền mã hóa** (crypto, exchange, ICO)
  - Giải thích sự khác biệt → tránh nhập nhằng

### PHẦN C: ĐÀ NẴNG SANDBOX / THÍ ĐIỂM

**Kết luận rõ ràng (1 dòng đầu tiên):**
> 🟢 **CÓ** sandbox chính thức / 🔴 **CHƯA CÓ** sandbox chính thức tính đến [ngày]

**Nếu CÓ — viết bảng:**
| Hạng mục | Chi tiết |
|----------|---------|
| Tên đề án/sandbox | ... |
| Cơ sở pháp lý | ... |
| Đơn vị chủ trì | ... |
| Đối tượng tham gia | ... |
| Phạm vi thử nghiệm | ... |
| Thời hạn | ... |
| Kết quả công bố | ... |
| Link nguồn | ... |

**Nếu CHƯA CÓ — viết:**
- Thông tin gần nhất: đề xuất/định hướng/đang xây dựng
- Các hoạt động liên quan (thành phố thông minh, CĐSQG tại ĐN)
- Bảng chứng cứ:
  | # | Nguồn | Nội dung | Ngày | Đánh giá |
  |---|-------|---------|------|----------|

### PHẦN D: VAI TRÒ THAM GIA CỦA NAPAS

**Vai trò khả thi của NAPAS (trung gian thanh toán):**
1. Đầu mối hạ tầng blockchain permissioned
2. Điều phối tiêu chuẩn/kết nối giữa các NH
3. Vận hành mạng permissioned liên ngân hàng
4. Dịch vụ xác thực/định danh (DID/KYC sharing)
5. Đối soát liên bên trên blockchain
6. Tokenization chứng từ số

**3-5 kịch bản theo mức rủi ro (PHẢI viết đầy đủ mỗi kịch bản):**

| Kịch bản | Mức rủi ro | Mô tả | Lợi ích | Rủi ro | Phụ thuộc pháp lý | Đối tác cần có | KPI đề xuất |
|----------|-----------|-------|---------|--------|-------------------|---------------|-------------|
| 1. PoC nội bộ | Thấp | ... | ... | ... | ... | ... | ... |
| 2. Pilot đối tác | Trung bình | ... | ... | ... | ... | ... | ... |
| 3. Mở rộng | Cao | ... | ... | ... | ... | ... | ... |

**Lộ trình 30-60-90 ngày cho kịch bản được khuyến nghị:**
| Giai đoạn | Thời gian | Hoạt động | Deliverable | Người chịu trách nhiệm |
|-----------|----------|-----------|-------------|----------------------|
| Khám phá | 30 ngày | ... | ... | ... |
| Xây dựng | 60 ngày | ... | ... | ... |
| Triển khai | 90 ngày | ... | ... | ... |

### PHỤ LỤC: DANH SÁCH NGUỒN ĐÃ SỬ DỤNG
| # | Nguồn | URL | Tier | Ngày truy cập | Ghi chú |
|---|-------|-----|------|--------------|---------|

## CÁCH TÌM KIẾM
```bash
python3 ~/.openclaw/skills/web-search/scripts/search.py "từ khóa" --region vn-vi --max 15
python3 ~/.openclaw/skills/web-search/scripts/search.py --extract "https://url-can-doc.com"
```

## GHI FILE
```bash
cat > ~/research/report-$(date +%Y%m%d).md << 'EOF'
[TOÀN BỘ nội dung — Phần 0 + A + B + C + D + Phụ lục]
EOF
```
