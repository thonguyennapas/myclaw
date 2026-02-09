---
name: source-validator
description: "Kiểm chứng và đánh giá độ tin cậy nguồn thông tin cho nghiên cứu. Tự động phân loại nguồn theo tier, phát hiện thông tin bịa/không xác minh, và tạo bảng chứng cứ nguồn. Sử dụng khi cần validate bất kỳ dữ kiện nào trong báo cáo nghiên cứu."
---

# Source Validator Skill

## Mô tả
Skill này kiểm chứng và đánh giá độ tin cậy của nguồn thông tin, đảm bảo mọi dữ kiện trong báo cáo nghiên cứu đều có nguồn gốc rõ ràng và đáng tin cậy.

## Khi nào sử dụng
- Khi cần xác minh tính chính xác của một nhận định
- Khi cần đánh giá độ tin cậy của một nguồn thông tin
- Khi cần cross-verify thông tin từ nhiều nguồn
- Khi cần tạo bảng chứng cứ nguồn cho báo cáo
- Khi phát hiện thông tin nghi ngờ bịa/sai lệch

## Hệ thống Phân loại Nguồn

### Tier 1: Nguồn Gốc Chính thức (Primary) 🟢
```
Đặc điểm:
- Xuất phát trực tiếp từ cơ quan có thẩm quyền
- Là văn bản chính thức, nghị quyết, quyết định
- Có số hiệu, ngày ban hành, cơ quan ban hành rõ ràng
- Có thể truy cập trên cổng thông tin chính thức

Ví dụ:
✅ vanban.chinhphu.vn - Văn bản quy phạm pháp luật
✅ sbv.gov.vn - Thông cáo NHNN
✅ bis.org - Báo cáo BIS
✅ ecb.europa.eu - Báo cáo ECB
✅ Công báo Chính phủ
```

### Tier 2: Nguồn Tổ chức Uy tín (Authoritative) 🔵
```
Đặc điểm:
- Từ tổ chức được công nhận, có chuyên môn
- Có quy trình biên tập, fact-checking
- Thường có methodology rõ ràng

Ví dụ:
✅ World Bank reports
✅ McKinsey, BCG, Deloitte reports
✅ Gartner Hype Cycle
✅ Chainalysis, Messari reports
✅ Đại học/viện nghiên cứu có uy tín
```

### Tier 3: Báo chí Uy tín (Established Media) 🟡
```
Đặc điểm:
- Có ban biên tập chuyên nghiệp
- Lịch sử lâu năm, được công nhận
- Thường trích nguồn cho nhận định quan trọng

Ví dụ:
⚠️ VnExpress, Tuổi Trẻ, Thanh Niên
⚠️ Reuters, Bloomberg, Financial Times
⚠️ CoinDesk, The Block (lĩnh vực chuyên ngành)
⚠️ Ledger Insights (enterprise blockchain)
```

### Tier 4: Nguồn Phụ (Secondary) 🟠
```
Đặc điểm:
- Blog doanh nghiệp, whitepaper
- Ý kiến chuyên gia (cần verify đúng chuyên gia)
- Bài viết tổng hợp từ nhiều nguồn khác

⚠️ Chỉ sử dụng khi có cross-reference với Tier 1-3
```

### Tier 5: Không Tin cậy (Unreliable) 🔴
```
❌ Social media posts (Twitter/X, Facebook, LinkedIn)
❌ Blog cá nhân không kiểm chứng
❌ Forum, Reddit posts
❌ Wikipedia (dùng để tìm nguồn gốc, không trích trực tiếp)
❌ Marketing materials của crypto projects
❌ Thông tin không có link, ngày, tác giả
❌ "Một nguồn tin cho biết..." (anonymous)
```

## Quy trình Kiểm chứng

### Checklist cho Mỗi Dữ kiện

```
□ 1. Nguồn có tồn tại? (link hoạt động)
□ 2. Nguồn thuộc Tier nào? (1-5)
□ 3. Ngày công bố/cập nhật?
□ 4. Tác giả/cơ quan rõ ràng?
□ 5. Có cross-reference? (≥2 nguồn cho fact quan trọng)
□ 6. Nội dung trích dẫn chính xác?
□ 7. Context đầy đủ? (không cherry-pick)
□ 8. Phân biệt: fact vs opinion vs prediction?
□ 9. Có bias rõ ràng không? (ai benefit?)
□ 10. Còn cập nhật không? (latest version?)
```

### Xử lý Khi Không Tìm Thấy Nguồn

```markdown
❌ SAI: "Việt Nam đã có sandbox blockchain" (không nguồn)

✅ ĐÚNG: "Tính đến [ngày], không tìm thấy nguồn chính thức 
xác nhận Việt Nam đã có sandbox blockchain chính thức."

✅ ĐÚNG: "Theo [nguồn], Việt Nam đang nghiên cứu khung thử nghiệm 
fintech, nhưng chưa có sandbox chuyên biệt cho blockchain 
được công bố chính thức. [link]"
```

### Xử lý Thông tin Mâu thuẫn

```markdown
✅ ĐÚNG:
"Về vấn đề [X], có hai quan điểm:
- Theo [Nguồn A, link], [nội dung A]
- Tuy nhiên, [Nguồn B, link] cho rằng [nội dung B]
- Chúng tôi ưu tiên [Nguồn A/B] vì [lý do]"
```

## Output: Bảng Chứng cứ Nguồn

### Format chuẩn

```markdown
## Bảng Chứng cứ Nguồn

| # | Nhận định | Nguồn | Tier | Ngày | Truy cập | Trạng thái |
|---|----------|-------|------|------|----------|------------|
| 1 | VN đang nghiên cứu CBDC | SBV Report | T1 | 03/2024 | 09/02/2026 | ✅ Verified |
| 2 | 130 NHTW đang research CBDC | BIS Survey | T1 | 06/2024 | 09/02/2026 | ✅ Verified |
| 3 | Đà Nẵng có sandbox | [Không tìm thấy] | - | - | 09/02/2026 | ⚠️ Unconfirmed |
```

## Cảnh báo Đỏ (Red Flags)

Dừng ngay và đánh dấu khi gặp:
1. 🚩 Thông tin quá tốt để là thật (too good to be true)
2. 🚩 Chỉ 1 nguồn duy nhất cho claim lớn
3. 🚩 Nguồn là marketing material của crypto project
4. 🚩 Số liệu không có methodology
5. 🚩 "Tin đồn", "theo nguồn tin", "được cho là"
6. 🚩 Copy-paste giữa nhiều site (không có nguồn gốc)
7. 🚩 Ngày công bố quá cũ (>2 năm) cho thông tin thị trường
8. 🚩 Tên chuyên gia/tổ chức không verify được
9. 🚩 Link dẫn đến 404 hoặc domain expired
10. 🚩 Thông tin VN viết bằng tiếng Anh nhưng không có bản gốc tiếng Việt

## Ví dụ Sử dụng

### Validate một nhận định:
```
Input: "Việt Nam đứng thứ 3 thế giới về adoption cryptocurrency"
Process:
1. Tìm nguồn: Chainalysis Crypto Adoption Index
2. Verify: https://chainalysis.com/... → Tier 2
3. Cross-check: coindesk.com article → Tier 3
4. Result: ⚠️ Secondary - Đây là index của Chainalysis (tư nhân),
   không phải số liệu chính thức. VN thứ 3 trong index 2023,
   cần kiểm tra version mới nhất.
```

### Validate văn bản pháp lý VN:
```
Input: "Quyết định 749/QĐ-TTg về chuyển đổi số"
Process:
1. Tìm nguồn gốc: vanban.chinhphu.vn
2. Verify: Có, số 749/QĐ-TTg ngày 03/06/2020
3. Nội dung: Chương trình Chuyển đổi số quốc gia
4. Blockchain liên quan: Có nhắc DLT trong mục công nghệ ưu tiên
5. Result: ✅ Tier 1 - Verified
```
