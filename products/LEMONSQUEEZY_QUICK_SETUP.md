# 🍋 HƯỚNG DẪN THIẾT LẬP LEMON SQUEEZY (3 PHÚT)
## Tab đang mở: https://app.lemonsqueezy.com/setup

Lemon Squeezy là cổng thanh toán Merchant of Record (MoR) hàng đầu thế giới dành riêng cho phần mềm (SaaS), công cụ AI và sản phẩm số. Họ tự động tính thuế VAT/Sales tax toàn cầu và chi trả thẳng về tài khoản ngân hàng / Payoneer / PayPal của bạn.

---

### 📝 BƯỚC 1: ĐIỀN THÔNG TIN CỬA HÀNG (Store Setup)
Trên màn hình `https://app.lemonsqueezy.com/setup`:
1. **Store Name:** Điền `MinhLap AI Tools` (hoặc `SynapseGEO`)
2. **Store URL:** `minhlap` (đường link sẽ là `minhlap.lemonsqueezy.com`)
3. **Country:** Chọn `Vietnam` (hoặc quốc gia bạn đang sinh sống)
4. **Currency:** Chọn `USD ($)`
5. Bấm **Create store**.

---

### 📦 BƯỚC 2: TẠO 2 SẢN PHẨM CHÍNH (Products)
Vào menu bên trái **Products** → **New Product**:

#### 1. Sản phẩm 1: SynapseGEO Pro Pass (Bán trên tool SynapseGEO)
- **Name:** `SynapseGEO Pro — AI Search Optimization Engine`
- **Pricing:** Single payment (Một lần) → `$19.00`
- **Description:** *"Audit unlimited domains for ChatGPT Search, Perplexity AI & Google AI Overviews. Instant license activation."*
- **Files / Redirect:** Redirect về `https://synapse-geo-audit.vercel.app?license={license_key}`

#### 2. Sản phẩm 2: The AI Money Blueprint eBook
- **Name:** `The AI Money Blueprint eBook`
- **Pricing:** `$14.99`
- **Files:** Kéo thả file `d:\Project\work\projects\digital_products\products\ebook_ai_money_blueprint\The_AI_Money_Blueprint.pdf`

---

### 🔑 BƯỚC 3: LẤY API KEY ĐIỀN VÀO FILE .ENV
1. Trên Lemon Squeezy, vào **Settings** (biểu tượng bánh răng góc dưới trái) → **API**.
2. Bấm **Generate new API key**, đặt tên `AI Money Machine`.
3. Copy mã khóa và dán vào file **[.env](file:///d:/Project/work/.env)** tại dòng:
   ```env
   LEMON_SQUEEZY_API_KEY=your_key_here
   ```
4. Ở phần **Stores**, copy ID cửa hàng của bạn (dãy số dạng `12345`) và dán vào:
   ```env
   LEMON_SQUEEZY_STORE_ID=your_store_id_here
   ```

---

### ⚡ BƯỚC 4: NHẬN TIỀN VỀ TÀI KHOẢN (Payouts)
- Vào **Settings** → **Payouts**.
- Kết nối tài khoản **Bank Transfer** (hỗ trợ chuyển khoản ngân hàng Việt Nam qua liên kết Stripe/Wise), hoặc **PayPal** / **Payoneer**.
- Lemon Squeezy sẽ tự động chuyển tiền định kỳ 2 lần/tháng vào tài khoản của bạn!
