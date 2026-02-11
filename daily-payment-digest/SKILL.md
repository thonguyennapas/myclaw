---
name: daily-payment-digest
description: "Tạo bản tin thanh toán hằng ngày. Tổng hợp công nghệ mới, protocol update, sự kiện payment quốc tế & Việt Nam. CHẠY BẰNG LỆNH BASH python3."
---

# 📰 Bản tin Thanh toán Hằng ngày

> 🚨 **TUYỆT ĐỐI KHÔNG** gọi tool web_search, Brave Search, hay built-in search.
> 🚨 **LUÔN LUÔN** chạy bằng **lệnh bash** như bên dưới.

## Khi nào sử dụng
- User yêu cầu bản tin, tin tức payment, cập nhật công nghệ thanh toán
- User hỏi về Visa, Mastercard, blockchain payment, CBDC, agentic commerce
- User muốn biết sự kiện fintech/payment, event công nghệ
- User nhắn: "bản tin", "tin thanh toán", "digest", "tin hôm nay", "có gì mới"
- User nhắn: "tổng hợp tin tức thanh toán"

## Cách thực hiện

### Bước 1: Tạo bản tin (mất ~2-3 phút tìm kiếm)
```bash
python3 ~/.openclaw/skills/daily-payment-digest/scripts/digest.py
```

### Bước 2: Đọc file và GỬI NGUYÊN VĂN cho user
```bash
cat ~/digests/digest-$(date +%Y-%m-%d).md
```

Đọc nội dung file trên rồi GỬI NGUYÊN VĂN cho user qua Telegram.
KHÔNG tóm tắt, KHÔNG chỉnh sửa. Gửi TOÀN BỘ nội dung.

Nếu file quá dài, chia thành nhiều tin nhắn theo từng chuyên mục (┈┈┈ là điểm chia).

## 6 chuyên mục
1. 🌐 Công nghệ Thanh toán (RTP, FedNow, ISO 20022, Open Banking)
2. 🏦 Visa · Mastercard · Card Networks (tokenization, tap to pay)
3. ⛓️ Blockchain · Crypto Payments (x402, CBDC, stablecoin, DeFi)
4. 🤖 Agentic Commerce · AI Payments (Google UCP, AP2, M2M)
5. 📅 Events & Hội nghị (Money 20/20, Sibos, sự kiện VN)
6. 🇻🇳 Thanh toán Việt Nam (NAPAS, NHNN, VNPay, MoMo, QR)

## Lưu ý
- Script tự động tìm ~30 queries EN + VI, lọc noise, xếp hạng relevance
- Output đã format sẵn cho Telegram, CHỈ CẦN gửi nguyên văn
- File lưu tại `~/digests/digest-YYYY-MM-DD.md`
- Cron job chạy `digest.py` trực tiếp rồi gửi qua Telegram API (không đi qua gateway)
