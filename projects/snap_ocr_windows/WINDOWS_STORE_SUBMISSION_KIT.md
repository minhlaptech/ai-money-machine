# 📦 MICROSOFT WINDOWS STORE SUBMISSION KIT
## SnapOCR Pro — Windows Screen Text & Table Extractor

Bộ hồ sơ chuẩn hóa để đăng ký, nộp duyệt và xuất bản ứng dụng lên **Microsoft Store (Windows 10 & Windows 11)** qua cổng **Microsoft Partner Center**.

---

### 1. THÔNG TIN HỒ SƠ ỨNG DỤNG (STORE METADATA)

* **Tên ứng dụng (App Product Name):** SnapOCR Pro — Screen Text & Table Extractor
* **Tên hiển thị rút gọn:** SnapOCR Pro
* **Danh mục (Category):** Productivity (Năng suất) & Utilities (Tiện ích văn phòng)
* **Xếp hạng độ tuổi (Age Rating):** All Ages (3+ / Mọi lứa tuổi, không có nội dung nhạy cảm)
* **Ngôn ngữ hỗ trợ chính:** English, Vietnamese, Chinese, Japanese, Korean, French, German
* **Mô tả ngắn (Short Summary - 100 ký tự):**
  > Extract text, tables, formulas, and data from images & screenshots with instant AI translation.

---

### 2. MÔ TẢ CHI TIẾT TỐI ƯU TÌM KIẾM CHỢ (ASO DESCRIPTION)

```markdown
⚡ SnapOCR Pro — The Ultimate Screen Text & Table Extractor for Windows 11.

Never type unselectable text by hand again! SnapOCR Pro empowers you to effortlessly capture, extract, and convert text, complex tables, passwords, and source code from any image, scanned PDF, video lecture, or remote desktop screen with a single hotkey.

🔥 HIGHLIGHTED CAPABILITIES:
• 📋 Global Clipboard Snip (Ctrl + V): Press Win + Shift + S to snip any area of your screen, then hit Ctrl + V inside SnapOCR to instantly extract text in 0.5 seconds.
• 📊 Table to Excel & CSV Conversion: Detects tabular structures, preserving columns and rows. Export directly to Excel (.CSV) or copy as clean Markdown tables with 1 click.
• 🌐 Offline & Multi-Language OCR: Supports English, Vietnamese (Tiếng Việt), Chinese (中文), Japanese (日本語), Korean, French, and German.
• 🚀 Instant AI Translation: Translate extracted foreign text into Vietnamese or English on the spot.
• 🛡️ 100% Secure & Private: Text recognition processes directly on your device. Your sensitive screenshots, documents, and credentials never touch a remote server.
• 🎨 Native Windows 11 Fluent Design: Features beautiful Acrylic glassmorphism, dark mode, and seamless keyboard shortcuts.

💼 WHO IS THIS FOR?
- Office Workers & Accountants (Extracting tables from scanned invoices and locked PDFs into Excel)
- Software Developers (Copying error logs, stack traces, and code snippets from video tutorials or IDEs)
- Students & Researchers (Snapping citations and notes from online lectures and non-copyable slides)
- Translators & Language Learners (Instant screen OCR translation)

💎 PRICING MODEL:
- Free Tier: Up to 20 OCR extractions per day.
- Pro Lifetime License: Unlimited extractions, priority table formatting, and lifetime updates for a single one-time purchase ($14.99 USD).
```

---

### 3. TỪ KHÓA TÌM KIẾM HÀNG ĐẦU TRÊN MICROSOFT STORE (ASO KEYWORDS)

Khi nộp trên Partner Center, điền 7 cụm từ khóa sau:
1. `screen ocr`
2. `image to text`
3. `extract table to excel`
4. `screenshot text grabber`
5. `pdf ocr extractor`
6. `snipping tool ocr`
7. `translate image text`

---

### 4. QUY TRÌNH 3 BƯỚC ĐÓNG GÓI MSIX & NỘP LÊN MICROSOFT STORE

Microsoft cung cấp công cụ miễn phí chính thức **PWABuilder** để biến ứng dụng web/PWA này thành tệp `.msix` chuẩn Microsoft Store chỉ trong 2 phút:

#### Bước 1: Mở PWABuilder
1. Truy cập: **[https://www.pwabuilder.com](https://www.pwabuilder.com)**.
2. Nhập đường dẫn live của ứng dụng hoặc tải thư mục `projects/snap_ocr_windows` lên.
3. Bấm **"Package for Windows"**.

#### Bước 2: Nhập thông tin Developer từ Microsoft Partner Center
- Điền **Publisher ID** và **Package Name** mà bạn nhận được khi tạo ứng dụng trên Microsoft Partner Center.
- Bấm **"Generate MSIX Package"**. PWABuilder sẽ tạo ra tệp `.msix` và file chứng chỉ số an toàn.

#### Bước 3: Nộp lên Microsoft Partner Center ($19 USD trọn đời)
1. Đăng nhập [partner.microsoft.com](https://partner.microsoft.com).
2. Tạo sản phẩm mới: `SnapOCR Pro`.
3. Tải tệp `.msix` lên mục **Packages**.
4. Sao chép mô tả và tải 3 ảnh chụp màn hình từ `STORE_SUBMISSION_KIT`.
5. Bấm **"Submit to the Store"**. Microsoft sẽ duyệt và đưa app lên chợ trong vòng 24 - 48 giờ!

---

### 5. HƯỚNG DẪN DÙNG THỬ TRÊN MÁY TÍNH NGAY BÂY GIỜ

Bạn có thể chạy thử SnapOCR Pro dưới dạng Desktop App trên Windows ngay:

1. Mở tệp [projects/snap_ocr_windows/index.html](file:///d:/Project/work/projects/snap_ocr_windows/index.html) bằng trình duyệt Microsoft Edge hoặc Chrome.
2. Trên thanh địa chỉ URL sẽ xuất hiện biểu tượng **"Cài đặt ứng dụng" (Install app icon)** ở góc phải.
3. Bấm **"Cài đặt"** -> SnapOCR Pro sẽ lập tức mở ra dưới dạng một cửa sổ ứng dụng Windows độc lập (có icon trên Taskbar và Desktop) với đầy đủ hiệu ứng Fluent Design!
4. Nhấn tổ hợp phím `Win + Shift + S` chụp một vùng màn hình bất kỳ -> Chuyển sang SnapOCR và nhấn `Ctrl + V` -> Bấm **Run OCR Extraction** để trải nghiệm.
