# 🚀 Hướng Dẫn 5 Phút Kết Nối Cổng Thanh Toán Quốc Tế (USD) Về Việt Nam

Để AI có thể tự động bán sản phẩm và bạn nhận tiền USD trực tiếp về tài khoản ngân hàng Việt Nam mà **không cần thành lập công ty tại Mỹ hay châu Âu**, giải pháp tối ưu nhất năm 2025–2026 là **LemonSqueezy** (hoặc **Paddle** / **Stripe qua Payoneer**).

---

## 1. Tại Sao Chọn LemonSqueezy?
- **Merchant of Record (MoR)**: LemonSqueezy tự xử lý toàn bộ thuế VAT/Sales Tax toàn cầu, chống gian lận thẻ tín dụng, bồi hoàn (chargeback) cho bạn.
- **Hỗ trợ Developer Việt Nam**: Đăng ký bằng CMND/CCCD hoặc Hộ chiếu Việt Nam.
- **Rút tiền trực tiếp**: Tiền bán USD sẽ được chuyển thẳng về tài khoản ngân hàng Việt Nam (Vietcombank, Techcombank, MB...) hoặc tài khoản Wise / Payoneer mỗi thứ Hai hàng tuần.

---

## 2. Các Bước Kích Hoạt Trong 5 Phút

### Bước 1: Tạo Tài Khoản Store
1. Truy cập [lemonsqueezy.com](https://www.lemonsqueezy.com) và đăng ký tài khoản miễn phí.
2. Đặt tên Store: VD: `SynapseLab` hoặc `SynapseGEO`.
3. Điền thông tin cá nhân (Việt Nam) và thông tin tài khoản ngân hàng để nhận tiền (Payout Settings).

### Bước 2: Tạo Sản Phẩm Bán (SynapseGEO)
1. Vào tab **Products** -> **New Product**.
2. Đặt tên: `SynapseGEO Pro - Lifetime Access`.
3. Giá bán: `$19.00` (One-time payment).
4. Description: Copy phần mô tả từ website `products/geo_audit_engine/index.html`.
5. Tạo sản phẩm thứ hai (gói Agency): `$49.00 / month` (Subscription).

### Bước 3: Lấy Link Thanh Toán (Checkout Overlay)
1. Nhấn **Share** -> Copy URL Checkout (VD: `https://synapsegeo.lemonsqueezy.com/buy/...`).
2. Mở file [app.js](file:///d:/Project/work/products/geo_audit_engine/app.js) tại dòng hàm `executeMockPayment` hoặc nút `triggerCheckout`.
3. Thay thế link mock bằng URL Checkout thật của LemonSqueezy hoặc tích hợp LemonSqueezy JS SDK:
```html
<script src="https://assets.lemonsqueezy.com/lemon.js" defer></script>
```

---

## 3. Quy Trình Vận Hành Hoàn Toàn Tự Động (Hands-Off)
1. Khách hàng quốc tế truy cập web -> Test thử miễn phí 1 URL.
2. Thấy điểm số cần cải thiện -> Bấm mua gói Pro $19.
3. Khách nhập thẻ Visa/Mastercard/Apple Pay trên LemonSqueezy.
4. LemonSqueezy tự sinh License Key gửi vào email khách.
5. Mỗi tuần, tiền USD tự chuyển về tài khoản ngân hàng của bạn. Bạn không cần can thiệp bất kỳ khâu vận hành nào!
