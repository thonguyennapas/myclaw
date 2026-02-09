# Lộ trình & Đề xuất Vai trò NAPAS trong Blockchain

📅 Cập nhật: 09/02/2026

## Vai trò Khả thi

| # | Vai trò | Mô tả | Lợi thế NAPAS | Ưu tiên |
|---|---------|-------|---------------|---------|
| 1 | **Đầu mối hạ tầng mạng Permissioned** | Vận hành blockchain enterprise cho hệ thống thanh toán liên ngân hàng | Có sẵn hạ tầng kết nối 50+ ngân hàng, kinh nghiệm vận hành switch | 🔴 Cao |
| 2 | **Điều phối Tiêu chuẩn & Kết nối** | Xây dựng tiêu chuẩn kỹ thuật kết nối blockchain giữa các ngân hàng thành viên | Vai trò trung gian kết nối hiện tại, trust relationship với NH | 🔴 Cao |
| 3 | **Dịch vụ Đối soát Liên bên (Smart Reconciliation)** | Smart contract tự động đối soát giao dịch liên ngân hàng trên blockchain | Core business hiện tại, hiểu sâu quy trình đối soát | 🔴 Cao |
| 4 | **Dịch vụ Xác thực / Định danh (eKYC Blockchain)** | DID / Verifiable Credentials cho xác thực giao dịch liên ngân hàng | Có dữ liệu KYC từ hệ thống ngân hàng, kết nối CCCD/VNeID | 🟡 TB |
| 5 | **Tokenization Chứng từ Thanh toán** | Số hóa chứng từ thanh toán, ủy nhiệm thu/chi trên blockchain | Xử lý hàng triệu giao dịch/ngày, hiểu quy trình chứng từ | 🟡 TB |

## Kịch bản Tham gia

### Kịch bản 1: PoC Đối soát Liên ngân hàng trên Blockchain
**Mức rủi ro**: 🟢 THẤP

**Mô tả**: Xây dựng prototype smart contract để tự động đối soát giao dịch ATM/POS liên ngân hàng. Chạy song song (shadow) với hệ thống hiện tại, không ảnh hưởng production.

**Lợi ích**:
- Giảm 50-80% thời gian đối soát (từ T+1 → near real-time)
- Phát hiện sai lệch tức thời thay vì cuối ngày
- Tích lũy expertise blockchain nội bộ
- Ít rủi ro: không ảnh hưởng hệ thống production

**Rủi ro**:
- Chi phí R&D team & infrastructure
- PoC không đảm bảo sẽ scale production
- Cần thuyết phục lãnh đạo về ROI dài hạn

**Phụ thuộc pháp lý**:
- Không yêu cầu phê duyệt pháp lý đặc biệt (internal PoC)
- Cần tuân thủ chính sách bảo mật dữ liệu nội bộ
- Dữ liệu test phải được anonymized

**Đối tác cần có**:
- Đội ngũ R&D nội bộ NAPAS
- 1-2 đối tác blockchain technology (Hyperledger, R3...)
- Đội vận hành/đối soát hiện tại (domain knowledge)

**KPI đề xuất**:
- Hoàn thành PoC đúng timeline (90 ngày)
- Accuracy đối soát ≥ 99.99% vs hệ thống hiện tại
- Thời gian đối soát giảm ≥ 50%
- Báo cáo ROI analysis cho phase tiếp theo

**Lộ trình**:
- 📅 30 ngày: Khảo sát platform (Hyperledger Besu/Fabric, R3 Corda), setup team, define use case chi tiết
- 📅 60 ngày: Phát triển smart contract đối soát, deploy testnet, data migration tool
- 📅 90 ngày: Chạy shadow test 2 tuần với dữ liệu thực (anonymized), đánh giá kết quả, báo cáo board

### Kịch bản 2: Pilot Tokenization Chứng từ Thanh toán Liên NH
**Mức rủi ro**: 🟡 TRUNG BÌNH

**Mô tả**: Phối hợp 2-3 ngân hàng thí điểm số hóa chứng từ thanh toán (ủy nhiệm thu/chi, lệnh chuyển tiền) trên blockchain permissioned. Verify tính toàn vẹn và traceability.

**Lợi ích**:
- Giảm giấy tờ, tăng tốc xử lý chứng từ
- Audit trail minh bạch, tamper-proof
- Tiền đề cho trade finance digitalization
- Vị thế tiên phong trong hệ sinh thái

**Rủi ro**:
- Cần NH đối tác sẵn sàng pilot
- Thay đổi quy trình nghiệp vụ
- Câu hỏi pháp lý về tính hợp lệ chứng từ điện tử trên blockchain
- Vấn đề tương thích với hệ thống core banking

**Phụ thuộc pháp lý**:
- Luật Giao dịch điện tử (sửa đổi 2023)
- Nghị định hướng dẫn về chứng từ điện tử
- Quy định NHNN về giao dịch điện tử trong ngân hàng
- Sandbox fintech nếu có

**Đối tác cần có**:
- 2-3 ngân hàng thương mại (ưu tiên NHTM lớn đã có interest)
- Nhà cung cấp blockchain enterprise (Hyperledger, Polygon CDK...)
- Tư vấn pháp lý chuyên blockchain/fintech
- NHNN (tham vấn, định hướng)

**KPI đề xuất**:
- 100+ giao dịch pilot thành công
- Uptime ≥ 99.9%
- Thời gian xử lý chứng từ giảm ≥ 40%
- ≥ 2 NH đồng ý mở rộng pilot
- Báo cáo compliance đầy đủ

**Lộ trình**:
- 📅 30 ngày: MoU với NH đối tác, design solution architecture, khảo sát legal framework
- 📅 60 ngày: Phát triển platform, smart contract cho chứng từ thanh toán, API integration với core banking test
- 📅 90 ngày: Go-live pilot, monitor 4 tuần, đánh giá kết quả, đề xuất mở rộng

### Kịch bản 3: Hạ tầng Mạng Blockchain Liên Ngân hàng (BankChain)
**Mức rủi ro**: 🔴 CAO

**Mô tả**: Triển khai permissioned blockchain network kết nối toàn bộ hệ thống ngân hàng thành viên, phục vụ đa dạng use cases: đối soát, chứng từ, KYC sharing, cross-border...

**Lợi ích**:
- Định vị NAPAS là hạ tầng blockchain quốc gia cho ngân hàng
- Revenue streams mới (node operation, API, consulting)
- Nền tảng cho nhiều dịch vụ blockchain trong tương lai
- Competitive advantage dài hạn

**Rủi ro**:
- Đầu tư lớn (infrastructure, team, operations)
- Cần đồng thuận toàn hệ thống NH
- Phụ thuộc khung pháp lý quốc gia
- Rủi ro technology obsolescence
- Cạnh tranh với các platform quốc tế

**Phụ thuộc pháp lý**:
- Phê duyệt NHNN (bắt buộc)
- Khung pháp lý cho private blockchain infrastructure
- Quy chuẩn kỹ thuật quốc gia cho DLT trong tài chính
- Tuân thủ Luật An toàn thông tin mạng
- Tuân thủ quy định chống rửa tiền (AML)

**Đối tác cần có**:
- NHNN (chỉ đạo, phê duyệt, giám sát)
- Toàn bộ NH thành viên NAPAS (50+ NH)
- Đối tác công nghệ cấp enterprise (IBM, Microsoft, Consensys...)
- Tư vấn quốc tế (McKinsey, BCG...)
- Đối tác bảo mật (security audit firm)

**KPI đề xuất**:
- Kết nối ≥ 10 NH trong năm đầu
- ≥ 1,000 giao dịch/ngày trên blockchain
- Uptime ≥ 99.99%
- Latency < 2 giây cho finality
- Pass security audit bởi bên thứ 3
- Break-even trong 3-5 năm

**Lộ trình**:
- 📅 30 ngày: Đề xuất chiến lược lên NHNN, tham vấn NH lớn, RFI cho technology partner
- 📅 60 ngày: Feasibility study, technology selection, consortium governance framework
- 📅 90 ngày: Architecture design, MVP scope, pilot selection (3-5 NH), funding proposal
