# Mapping: 14 Câu hỏi Phân tích ↔ Dashboard

## Tổng quan
Bảng này map 14 câu hỏi phân tích với các tab/biểu đồ trong dashboard.
**Trạng thái: 14/14 câu hỏi đã có biểu đồ trực tiếp (100%).**

---

## Nhóm 1: Phân tích giá (Price Analysis)

### ✅ Câu 1: Tính doanh thu trung bình của sản phẩm trong khoảng giá 100–300k VND
- **Tab:** Phân tích giá
- **Biểu đồ:** 3 KPI cards (Doanh thu TB/SP, Tổng doanh thu, Số sản phẩm)
- **Tiêu đề:** "Q1 – Phân khúc 100–300k VND"
- **Bổ sung:** Biểu đồ "Lượng bán trung bình / sản phẩm theo khúc giá"

### ✅ Câu 2: So sánh tỷ lệ discount giữa các danh mục sản phẩm
- **Tab:** Phân tích giá
- **Biểu đồ:** Thanh ngang sắp xếp — "Giảm giá TB (%) theo danh mục (đã sắp xếp)"
- **Đặc điểm:** `color_continuous_scale='Oranges'`, text hiển thị %, horizontal (label danh mục dài)

### ✅ Câu 3: Tìm phân khúc giá có ROI cao nhất (revenue / product_count)
- **Tab:** Phân tích giá
- **Biểu đồ:** Thanh đứng sắp xếp giảm — "Q3 – ROI theo khúc giá (doanh thu / số SP, đã sắp xếp)"
- **Đặc điểm:** `color_continuous_scale='Greens'`, text hiển thị số VNĐ

---

## Nhóm 2: Hiệu suất bán hàng (Sales Performance)

### ✅ Câu 4: Phân tích correlation giữa review_count và quantity_sold
- **Tab:** Tương tác khách hàng
- **Biểu đồ:** Scatter log–log "Q4 – Review và bán hàng (r = 0.621, màu = rating)"
- **Đặc điểm:** Trendline log–log bằng `numpy.polyfit`; annotation Pearson r = 0.621; KPI card "Pearson r"
- **Không dùng statsmodels** — dự án dùng numpy polyfit để không cần dependency thêm

### ✅ Câu 5: Tìm top 10 sản phẩm có tiềm năng cao (high reviews, low sales)
- **Tab:** Hiệu suất bán hàng
- **Biểu đồ:** Thanh ngang sequential — "Q5 – Top 10 sản phẩm tiềm năng (nhiều review / ít bán)"
- **Công thức:** `potential_score = review_count / (quantity_sold + 1)`
- **Lọc:** `review_count >= 20` và `quantity_sold > 0` (loại SKU chưa bán — nhiễu)
- **Đặc điểm:** `_SEQ_BLUE` colorscale, colorbar "Điểm tiềm năng", hover có review_count + sold + price

### ✅ Câu 6: Tính conversion rate ước tính từ review_count
- **Tab:** Tương tác khách hàng
- **Biểu đồ:** Thanh đứng — "Q6 – Tỷ lệ chuyển đổi ước tính theo bậc review"
- **Công thức:** `conv_rate = avg_sold / mid_review_count` (proxy: giữa mỗi khoảng review)
- **Đặc điểm:** `color_continuous_scale='Teal'`

---

## Nhóm 3: Thương hiệu & thị trường (Brand Analysis)

### ✅ Câu 7: So sánh hiệu suất bán hàng giữa OEM và Branded products
- **Tab:** Thương hiệu & thị trường
- **Biểu đồ:** `make_subplots` 1×3 — "Q7 – OEM so với thương hiệu"
  - Panel 1: Số SKU trong catalog
  - Panel 2: Giá TB (nghìn VND)
  - Panel 3: Doanh số TB / SKU (đơn)
- **Đặc điểm:** 2 màu riêng (OEM `#c2410c`, Branded `#0369a1`); không gộp thang lệch
- **Kèm:** 3 KPI cards (Sản phẩm OEM, Có thương hiệu, Chênh giá)

### ✅ Câu 8: Tìm thương hiệu có rating trung bình cao nhất (min 50 products)
- **Tab:** Thương hiệu & thị trường
- **Biểu đồ:** Thanh ngang sorted — "Q8 – Top 15 thương hiệu theo rating TB (≥ 50 SP)"
- **Lọc:** `product_count >= 50` và `avg_rating > 0`
- **Đặc điểm:** `color_continuous_scale='RdYlGn'`, text rating, `xaxis range=[0, 5.5]`

### ✅ Câu 9: Phân tích price positioning của top 10 brands
- **Tab:** Thương hiệu & thị trường
- **Biểu đồ:** Dot plot (min ● TB ◆ max) — "Q9 – Vị thế giá top 10 thương hiệu"
- **Đặc điểm:** `go.Scatter` markers+lines, 3 điểm mỗi brand (min/avg/max), nghìn VND

---

## Nhóm 4: Tính năng sản phẩm (Product Features)

### ✅ Câu 10: Ảnh hưởng của số lượng ảnh (number_of_images) đến rating
- **Tab:** Tính năng sản phẩm
- **Biểu đồ:** Thanh đứng gom nhóm — "Q10 – Rating TB theo số ảnh (gom nhóm)"
- **Gom nhóm:** `pd.cut` vào 5 bucket (1–5 ảnh, 6–10, 11–15, 16–20, 21+)
- **Đặc điểm:** Gradient cam đỏ (`#fff7ed` → `#9a3412`), customdata=n trong hover, colorbar
- **Tại sao không dùng scatter:** Scatter thô + outlier (50–70 ảnh) quá nhiễu; bar gom nhóm rõ pattern hơn

### ✅ Câu 11: Tác động của video (has_video) đến quantity_sold
- **Tab:** Tính năng sản phẩm
- **Biểu đồ:** `make_subplots` 2 hàng — "Q11 – Video: lượng bán TB / SKU"
  - Hàng 1: Avg sold (Có video vs Không video)
  - Hàng 2: Số SKU trong nhóm
- **Tại sao 2 panel:** avg_sold (vài–vài chục) vs count (nghìn) — gộp trên 1 trục Y sẽ vô nghĩa

### ✅ Câu 12: Phân tích sản phẩm có pay_later vs không có
- **Tab:** Tính năng sản phẩm
- **Biểu đồ:** `make_subplots` 2 hàng — "Q12 – Trả sau: lượng bán TB / SKU"
  - Hàng 1: Avg sold (Trả sau vs Không trả sau)
  - Hàng 2: Số SKU trong nhóm
- **Kèm:** 3 KPI cards (SKU có video, Ảnh TB/SKU, SKU hỗ trợ trả sau)

---

## Nhóm 5: Phân tích chuyên sâu (Temporal Analysis)

### ✅ Câu 13: Xu hướng phân bố catalog theo tuổi listing (date_created)
- **Tab:** Phân tích chuyên sâu
- **Biểu đồ:** Line chart (ordinal) — "Q13 – Phân bố catalog theo tuổi listing"
- **Xử lý dữ liệu:** `date_created` là **số ngày** (không phải Unix timestamp) — parse bằng `pd.to_numeric`
- **Khoảng tuổi:** 11 bands tiếng Việt (0–30 ngày, 31–60 ngày, …, >3 năm)
- **Đặc điểm:** Marker size=8, line width=3; book.md: "line chart for trends along ordered axis"

### ✅ Câu 14: Phân tích sản phẩm mới (launched trong 6 tháng gần nhất)
- **Tab:** Phân tích chuyên sâu
- **Biểu đồ:** Thanh ngang — "Q14 – Sản phẩm mới (tuổi listing ≤ 183 ngày ~ 6 tháng)"
- **Proxy:** Không có ngày lịch tuyệt đối → dùng tuổi listing ≤ 183 ngày
- **Kèm:** KPI card tổng sản phẩm mới + giải thích proxy

---

## TỔNG KẾT

### Thống kê Coverage

| Trạng thái | Số câu hỏi | % | Câu hỏi |
|------------|------------|---|---------|
| ✅ Trả lời đầy đủ trên dashboard | 14 | 100% | 1–14 |

### Phân tích theo nhóm

| Nhóm | Tab | Số Q | Coverage |
|------|-----|------|----------|
| Nhóm 1 – Phân tích giá | Phân tích giá | 3/3 | 100% |
| Nhóm 2 – Hiệu suất bán | Hiệu suất bán + Tương tác KH | 3/3 | 100% |
| Nhóm 3 – Thương hiệu | Thương hiệu & thị trường | 3/3 | 100% |
| Nhóm 4 – Tính năng SP | Tính năng sản phẩm | 3/3 | 100% |
| Nhóm 5 – Thời gian | Phân tích chuyên sâu | 2/2 | 100% |
| **Tổng** | | **14/14** | **100%** |

### Cải tiến so với phiên bản trước

| Hạng mục | Trước | Sau |
|----------|-------|-----|
| Câu hỏi trả lời trực tiếp | 6/14 (42.9%) | **14/14 (100%)** |
| Ngôn ngữ giao diện | Tiếng Anh | **Tiếng Việt** |
| Biểu đồ pie/donut | Có | **Không** (thay bằng thanh ngang) |
| Tab Product Features | Không có | **Có** (Q10–Q12) |
| Tab Deep Dive Q13/Q14 | Không có | **Có** (line chart + bar) |
| Q7 OEM vs Branded | Gộp thang lệch | **make_subplots 1×3** |
| Q10 scatter nhiễu | Scatter + trend | **Bar gom nhóm (bucket)** |
| AI Assistant | Placeholder | **Hoạt động end-to-end** |
| Phối màu | Cầu vồng/ngẫu nhiên | **Sequential một hue (book.md)** |
