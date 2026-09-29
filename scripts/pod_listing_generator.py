"""
Print-on-Demand (POD) Multi-Platform Listing & SEO Generator
-------------------------------------------------------------
Tự động tạo tiêu đề, mô tả chuẩn SEO, 13 thẻ tags cho Etsy/Redbubble/Amazon Merch,
kèm bảng tính toán tỷ suất lợi nhuận (Profit Margin) theo từng loại sản phẩm.
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

POD_PRODUCTS_CONFIG = {
    "hoodie_coffee_llms": {
        "title": "Powered by Coffee & LLMs Heavyweight Hoodie | Cyberpunk AI Developer Sweatshirt",
        "niche": "Programmers, AI Engineers, Tech Workers, Solopreneurs",
        "mockup": "projects/print_on_demand/designs/hoodie_coffee_llms.jpg",
        "retail_price": 48.00,
        "printify_cost": 23.50,
        "shipping_est": 6.50,
        "etsy_tags": [
            "ai engineer hoodie", "software developer gift", "coding sweatshirt", "cyberpunk hoodie",
            "coffee and coding", "programmer apparel", "tech geek clothes", "chatgpt gift",
            "machine learning gift", "computer science student", "nerd streetwear", "data scientist gift", "indie hacker"
        ],
        "bullet_points": [
            "PREMIUM STREETWEAR FIT: Crafted from 80% combed organic cotton & 20% durable poly-fleece for heavyweight comfort.",
            "CYBERPUNK NEON AESTHETIC: Features vibrant neon cyan & magenta neural circuit artwork with 'Powered by Coffee & LLMs'.",
            "PERFECT TECH GIFT: Ideal for software engineers, prompt writers, data scientists, and late-night builders.",
            "DURABLE DIRECT-TO-GARMENT PRINT: Won't crack or fade after repeated wash cycles. Double-needle stitched hems."
        ]
    },
    "tshirt_it_works": {
        "title": "It Works On My Machine Vintage Developer T-Shirt | Funny Programmer Graphic Tee",
        "niche": "Software Engineers, DevOps, IT Support",
        "mockup": "projects/print_on_demand/designs/tshirt_it_works_on_my_machine.jpg",
        "retail_price": 26.00,
        "printify_cost": 10.20,
        "shipping_est": 4.50,
        "etsy_tags": [
            "it works on my machine", "funny programmer shirt", "coding tshirt", "software developer tee",
            "devops gift", "computer science tee", "tech humor shirt", "debugging shirt",
            "git push shirt", "developer joke", "coder birthday gift", "linux shirt", "web dev tee"
        ],
        "bullet_points": [
            "ULTRA-SOFT 100% RING-SPUN COTTON: Lightweight, breathable fabric tailored for all-day comfort at your desk.",
            "RELATABLE DEV HUMOR: Classic developer excuse in vintage typography that every engineer instantly recognizes.",
            "UNISEX MODERN FIT: True-to-size retail fit that looks sharp on video calls or at tech conferences.",
            "PRINTED & SHIPPED ON-DEMAND: High-definition eco-friendly inks with zero plastic feel."
        ]
    },
    "mug_ai_brain": {
        "title": "Neural Circuit Brain Ceramic Coffee Mug (15oz) | AI & Machine Learning Developer Mug",
        "niche": "Data Scientists, AI Researchers, Tech Enthusiasts",
        "mockup": "projects/print_on_demand/designs/mug_ai_circuit_brain.jpg",
        "retail_price": 18.00,
        "printify_cost": 6.80,
        "shipping_est": 5.20,
        "etsy_tags": [
            "ai coffee mug", "neural network mug", "machine learning gift", "tech desk accessory",
            "programmer coffee cup", "data science mug", "coder desk setup", "ai researcher gift",
            "cyberpunk coffee mug", "computer science grad", "tech coworker gift", "15oz ceramic mug", "office mug"
        ],
        "bullet_points": [
            "LARGE 15 OZ CAPACITY: Generous size to keep your caffeine supply uninterrupted during deep coding sessions.",
            "GLOSSY CERAMIC FINISH: Microwave and dishwasher safe with vivid wrap-around circuit brain illustration.",
            "VIBRANT SUBLIMATION PRINT: Crisp, scratch-resistant print that retains its brilliance for years.",
            "SECURE PROTECTIVE PACKAGING: Ships in crush-proof molded foam packaging to ensure zero transit damage."
        ]
    }
}

def generate_pod_listing(product_key="hoodie_coffee_llms"):
    p = POD_PRODUCTS_CONFIG.get(product_key, POD_PRODUCTS_CONFIG["hoodie_coffee_llms"])
    out_dir = Path(__file__).resolve().parent.parent / "projects" / "print_on_demand" / "listings"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"listing_{product_key}.md"

    gross_profit = p["retail_price"] - p["printify_cost"] - p["shipping_est"]
    margin_pct = (gross_profit / p["retail_price"]) * 100

    bullets_text = "\n".join([f"• {b}" for b in p["bullet_points"]])
    tags_text = ", ".join(p["etsy_tags"])

    content = f"""# 👕 Print-on-Demand Ready-to-Publish Listing: {product_key.upper()}
> **Tạo lúc**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **Ngách mục tiêu**: `{p['niche']}`  
> **Tệp thiết kế / Mockup**: `{p['mockup']}`

---

## 💰 1. Bảng Tính Lợi Nhuận & Giá Bán (Economics)
- **Giá bán niêm yết (Retail Price):** `${p['retail_price']:.2f}`
- **Giá vốn in ấn (Printify Base Cost):** `${p['printify_cost']:.2f}`
- **Phí vận chuyển ước tính (Shipping):** `${p['shipping_est']:.2f}`
- **Lợi nhuận gộp trên mỗi đơn (Net Profit):** `${gross_profit:.2f}`
- **Tỷ suất lợi nhuận (Profit Margin):** `{margin_pct:.1f}%`

---

## 🏷️ 2. Tiêu Đề Chuẩn SEO (Etsy / Redbubble / Amazon Merch)
```text
{p['title']}
```

---

## 📋 3. Mô Tả Chi Tiết Sản Phẩm (Description & Features)
```text
{p['title']}

Upgrade your daily builder rotation with this high-density piece designed specifically for tech thinkers, engineers, and digital creators.

KEY HIGHLIGHTS:
{bullets_text}

SIZING & FIT:
- Standard US Unisex fit. If you prefer an oversized streetwear look, we recommend sizing up one size.
- Pre-shrunk fabric ensures consistent shape after laundering.

CARE INSTRUCTIONS:
- Machine wash cold, inside out, with like colors.
- Tumble dry low or hang dry for longest graphic lifespan.
- Do not iron directly on print design.

SHIPPING & PROCESSING:
- Crafted and fulfilled within 2–4 business days.
- Tracking number provided as soon as package is dispatched.
```

---

## 🔖 4. 13 Thẻ Tags SEO (Etsy / Redbubble - Copy & Paste Trực Tiếp)
```text
{tags_text}
```
"""

    out_file.write_text(content, encoding="utf-8")
    print(f"[✓] Created POD listing package: {out_file} (Net profit: ${gross_profit:.2f}/item)")
    return out_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="POD Multi-Platform Listing Generator")
    parser.add_argument("--item", default="hoodie_coffee_llms", choices=["hoodie_coffee_llms", "tshirt_it_works", "mug_ai_brain"], help="Product key")
    args = parser.parse_args()
    generate_pod_listing(args.item)
