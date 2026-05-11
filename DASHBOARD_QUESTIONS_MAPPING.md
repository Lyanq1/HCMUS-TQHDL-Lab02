# Mapping: 14 Câu hỏi Phân tích ↔ Dashboard

## Tổng quan
Bảng này map 14 câu hỏi phân tích đã chuẩn bị với các tab/biểu đồ trong dashboard để kiểm tra xem dashboard có trả lời được các câu hỏi này không.

---

## Nhóm 1: Price Analysis

### ✅ Câu 1: Tính doanh thu trung bình của sản phẩm trong khoảng giá 100-300k VND
**Trả lời qua Dashboard:** ✅ CÓ
- **Tab:** Price Analysis
- **Biểu đồ:** "Average Sales per Product by Segment"
- **Dữ liệu hiển thị:** Avg sales per product cho từng price segment
- **Cách tính thêm:** Revenue = Avg sales × Avg price của segment
- **Kết quả:** Segment 100-300k có avg_sold = 13.2, avg_price ≈ 200k → Revenue ≈ 2.64M VND/product

### ✅ Câu 2: So sánh tỷ lệ discount giữa các danh mục sản phẩm
**Trả lời qua Dashboard:** ⚠️ CHƯA TRỰC TIẾP
- **Tab:** Không có tab riêng cho discount analysis
- **Dữ liệu có:** Dataset có cột `discount_pct` (original_price - price)
- **Cần bổ sung:** Thêm biểu đồ so sánh discount % by category
- **Giải pháp:** Có thể tính qua Deep Dive tab với filtering

### ✅ Câu 3: Tìm phân khúc giá có ROI cao nhất (revenue/product_count)
**Trả lời qua Dashboard:** ✅ CÓ
- **Tab:** Price Analysis
- **Biểu đồ:** "Product vs Revenue Distribution by Price Segment"
- **Cách đọc:** So sánh % revenue vs % products
- **Kết quả:** Segment 100-300k có ROI tốt nhất (26.4% products → 28.8% revenue)

---

## Nhóm 2: Sales Performance

### ✅ Câu 4: Phân tích correlation giữa review_count và quantity_sold
**Trả lời qua Dashboard:** ✅ CÓ
- **Tab:** Customer Engagement
- **Biểu đồ:** "Reviews vs Sales (colored by rating)" - Scatter plot log-scale
- **Dữ liệu hiển thị:** Correlation rõ ràng, có mention "correlation: 0.621"
- **Insight:** Hiển thị trong title và KPI card

### ✅ Câu 5: Tìm top 10 sản phẩm có tiềm năng cao (high reviews, low sales)
**Trả lời qua Dashboard:** ⚠️ CHƯA TRỰC TIẾP
- **Tab:** Không có biểu đồ riêng cho "high potential products"
- **Dữ liệu có:** Có review_count và quantity_sold
- **Cần bổ sung:** Thêm scatter plot với quadrant analysis (high review, low sales)
- **Giải pháp tạm:** Có thể filter trong Deep Dive tab

### ✅ Câu 6: Tính conversion rate ước tính từ review_count
**Trả lời qua Dashboard:** ⚠️ GIÁN TIẾP
- **Tab:** Customer Engagement
- **Biểu đồ:** "Review Count Impact on Average Sales"
- **Dữ liệu:** Có avg_sold theo review ranges
- **Assumption:** Conversion rate ∝ quantity_sold / review_count
- **Cần bổ sung:** Thêm metric "sales per review" để tính conversion

---

## Nhóm 3: Brand Analysis

### ✅ Câu 7: So sánh hiệu suất bán hàng giữa OEM và Branded products
**Trả lời qua Dashboard:** ✅ CÓ
- **Tab:** Brand & Market
- **Biểu đồ:** "OEM vs Branded Comparison"
- **Metrics hiển thị:** Products count, Avg Price, Avg Sales
- **Insight rõ ràng:** OEM có volume cao, Branded có price cao 4.1x

### ✅ Câu 8: Tìm thương hiệu có rating trung bình cao nhất (min 50 products)
**Trả lời qua Dashboard:** ⚠️ CHƯA TRỰC TIẾP
- **Tab:** Brand & Market
- **Biểu đồ hiện có:** Top brands by revenue, brand scatter
- **Thiếu:** Không filter theo "min 50 products" và không sort by rating
- **Cần bổ sung:** Thêm biểu đồ "Top Brands by Rating (min 50 products)"

### ✅ Câu 9: Phân tích price positioning của top 10 brands
**Trả lời qua Dashboard:** ✅ CÓ
- **Tab:** Brand & Market
- **Biểu đồ:** "Top Brands: Product Count vs Revenue" - Scatter plot
- **Dữ liệu:** Có avg_price trong dataset top_brands
- **Cách đọc:** Position trên trục y (revenue) cho thấy price positioning

---

## Nhóm 4: Product Features

### ✅ Câu 10: Ảnh hưởng của số lượng ảnh (number_of_images) đến rating
**Trả lời qua Dashboard:** ❌ CHƯA CÓ
- **Tab:** Không có tab phân tích product features
- **Dữ liệu có:** Dataset có cột `number_of_images` và `rating_average`
- **Cần bổ sung:** Thêm scatter plot hoặc grouped bar chart
- **Giải pháp:** Cần thêm tab "Product Features Analysis" hoặc AI module

### ✅ Câu 11: Tác động của video (has_video) đến quantity_sold
**Trả lời qua Dashboard:** ❌ CHƯA CÓ
- **Tab:** Không có
- **Dữ liệu có:** Dataset có cột `has_video` (boolean)
- **Cần bổ sung:** Comparison chart: products with video vs without video
- **Metric:** Avg quantity_sold, avg revenue cho 2 nhóm

### ✅ Câu 12: Phân tích sản phẩm có pay_later vs không có
**Trả lời qua Dashboard:** ❌ CHƯA CÓ
- **Tab:** Không có
- **Dữ liệu có:** Dataset có cột `pay_later` (boolean)
- **Cần bổ sung:** Similar to câu 11, comparison analysis
- **Insight tiềm năng:** Pay_later có thể tăng conversion rate

---

## Nhóm 5: Temporal Analysis

### ✅ Câu 13: Xu hướng ra mắt sản phẩm theo thời gian (date_created)
**Trả lời qua Dashboard:** ❌ CHƯA CÓ
- **Tab:** Không có temporal analysis
- **Dữ liệu có:** Dataset có cột `date_created`
- **Cần bổ sung:** Line chart showing product launches over time
- **Insight:** Identify peak launch periods, seasonal trends

### ✅ Câu 14: Phân tích sản phẩm mới (launched trong 6 tháng gần nhất)
**Trả lời qua Dashboard:** ❌ CHƯA CÓ
- **Tab:** Không có
- **Dữ liệu có:** Có `date_created`, có thể filter
- **Cần bổ sung:** Filter by date + comparison với older products
- **Metrics:** Performance của new products vs established products

---

## TỔNG KẾT

### Thống kê Coverage

| Trạng thái | Số câu hỏi | % | Câu hỏi |
|------------|------------|---|---------|
| ✅ Trả lời đầy đủ | 6 | 42.9% | 1, 3, 4, 7, 9 |
| ⚠️ Trả lời gián tiếp | 3 | 21.4% | 2, 5, 6, 8 |
| ❌ Chưa có | 5 | 35.7% | 10, 11, 12, 13, 14 |

### Phân tích theo nhóm

**Nhóm 1 - Price Analysis:** 2/3 câu (66.7%)
- Câu 1, 3: ✅ Đầy đủ
- Câu 2: ⚠️ Cần bổ sung discount analysis

**Nhóm 2 - Sales Performance:** 1/3 câu (33.3%)
- Câu 4: ✅ Đầy đủ
- Câu 5, 6: ⚠️ Cần bổ sung

**Nhóm 3 - Brand Analysis:** 2/3 câu (66.7%)
- Câu 7, 9: ✅ Đầy đủ
- Câu 8: ⚠️ Cần filter by min products

**Nhóm 4 - Product Features:** 0/3 câu (0%)
- Tất cả ❌ Chưa có tab phân tích features

**Nhóm 5 - Temporal Analysis:** 0/2 câu (0%)
- Tất cả ❌ Chưa có temporal analysis

---

## KHUYẾN NGHỊ CẢI THIỆN

### Ưu tiên cao (Critical for Q&A session)

**1. Thêm tab "Product Features Analysis"**
- Biểu đồ: Images count vs Rating (scatter plot)
- Biểu đồ: Video impact comparison (bar chart: with video vs without)
- Biểu đồ: Pay_later impact (comparison chart)
- **Lý do:** Trả lời câu 10, 11, 12 (3 câu hỏi)

**2. Bổ sung Discount Analysis vào Price Analysis tab**
- Biểu đồ: Discount % by category (box plot hoặc violin plot)
- Metric: Avg discount % per category
- **Lý do:** Trả lời câu 2

**3. Thêm High Potential Products vào Sales Performance tab**
- Biểu đồ: Scatter plot với quadrant (high review, low sales)
- Filter: Top 20 high potential products
- **Lý do:** Trả lời câu 5

### Ưu tiên trung bình (Nice to have)

**4. Thêm Temporal Analysis tab**
- Line chart: Product launches over time
- Comparison: New products (6 months) vs Old products
- **Lý do:** Trả lời câu 13, 14

**5. Cải thiện Brand Analysis**
- Thêm filter: Min products count
- Sort by rating option
- **Lý do:** Trả lời đầy đủ câu 8

**6. Thêm Conversion Metrics vào Customer Engagement**
- Metric: Sales per review (conversion proxy)
- Chart: Conversion rate by segment
- **Lý do:** Trả lời câu 6

