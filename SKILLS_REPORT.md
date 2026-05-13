# BÁO CÁO PHÂN TÍCH DỮ LIỆU - TIKI E-COMMERCE
## Đồ án Trực quan hóa Dữ liệu

---

## 1. TỔNG QUAN DỮ LIỆU

### 1.1 Nguồn dữ liệu
- **Platform**: TIKI Vietnam (100% dữ liệu Việt Nam)
- **Tổng số sản phẩm**: 41,576 sản phẩm
- **Số biến**: 19 biến (vượt yêu cầu tối thiểu 7 biến)
- **Danh mục**: 6 danh mục thời trang (Balo/Vali, Phụ kiện, Giày nam/nữ, Túi xách nam/nữ)
- **Số thương hiệu**: 824 thương hiệu
- **Tổng doanh thu ước tính**: 86.4 tỷ VND

### 1.2 Độ tin cậy dữ liệu
✅ **Đạt tiêu chí 1**: Kết hợp nguồn dữ liệu đáng tin cậy
- Dữ liệu crawl từ TIKI - sàn thương mại điện tử lớn nhất Việt Nam
- Đã kiểm tra và xử lý missing values, outliers
- Validation: price ≤ original_price, rating trong khoảng [0-5]
- Không có duplicate records

---

## 2. PHÂN TÍCH SÂU THEO YÊU CẦU

### 2.1 Đặc điểm chính: THỊ TRƯỜNG GIÁ RẺ CHIẾM ƯU THẾ

**Bức tranh tổng thể:**
- Phân khúc dưới 100k VND: **55.7% sản phẩm** nhưng chỉ **28.1% doanh thu**
- Phân khúc 100–300k VND: **26.4% sản phẩm**, **28.8% doanh thu**
- **Kết luận**: 82.1% sản phẩm tập trung ở phân khúc giá rẻ (<300k)

### 2.2 Phân tích sâu phân khúc dưới 100k VND

#### A. Cấu trúc sản phẩm trong phân khúc
**Danh mục chiếm ưu thế:**
1. **Fashion Accessories** (Phụ kiện thời trang)
   - Kính mát, túi đeo chéo, miếng lót giày
   - Giá trung bình: 60,000 - 70,000 VND
   - Ví dụ best-seller: Túi đeo chéo LAZA (60k VND, bán 24,847 chiếc)

2. **Giày dép phân khúc thấp**
   - Dép, giày thể thao giá rẻ
   - Phụ kiện chăm sóc giày

#### B. Đặc điểm thương hiệu
- **73.8% là sản phẩm OEM** (không thương hiệu)
- OEM chiếm ưu thế tuyệt đối ở phân khúc <100k
- Giá trung bình OEM: 151k VND vs Branded: 613k VND (chênh lệch 4.1x)

#### C. Hiệu suất bán hàng
- **Trung bình 23.2 sản phẩm/SKU** - cao nhất trong tất cả phân khúc
- Top seller: Kính mát OEM 2508 (600k, bán 2,761 chiếc)
- Sản phẩm giá rẻ có volume cao nhưng margin thấp

#### D. Chất lượng và đánh giá
- Rating trung bình: 1.38/5 (thấp do nhiều sản phẩm chưa có đánh giá)
- Chỉ 31.3% sản phẩm có reviews
- Sản phẩm có 50+ reviews bán nhiều hơn **147.4x** so với <10 reviews

### 2.3 Đây có phải thị trường ngách?

**KHÔNG - Đây là thị trường đại chúng (Mass Market)**

**Bằng chứng:**
1. **Volume cao**: 23,160 sản phẩm trong phân khúc dưới 100k
2. **Doanh số lớn**: Tổng 739,094 sản phẩm đã bán
3. **Đa dạng danh mục**: Không tập trung vào 1 niche cụ thể
4. **Giá thấp, margin thấp**: Chiến lược volume-based

**So sánh với thị trường ngách:**
- Thị trường ngách: Ít sản phẩm, giá cao, margin cao, khách hàng đặc thù
- Thị trường này: Nhiều sản phẩm, giá thấp, margin thấp, khách hàng đại chúng

### 2.4 Dự đoán doanh thu khi đầu tư

**Mô hình dự đoán dựa trên Review Count (Correlation: 0.621)**

#### Assumption Model:
```
Revenue Potential = Price × Predicted_Sales
Predicted_Sales = f(review_count, category, price_segment)
```

**Kịch bản đầu tư vào phân khúc dưới 100k:**

| Review Count | Avg Sales/Product | Revenue/Product | ROI Estimate |
|--------------|-------------------|-----------------|--------------|
| 0-10 reviews | 1.6 sản phẩm | 112k VND | Thấp |
| 10-50 reviews | 15.3 sản phẩm | 1.07M VND | Trung bình |
| 50+ reviews | 235.8 sản phẩm | 16.5M VND | Cao |

**Kết luận:**
- Đầu tư vào sản phẩm giá rẻ CẦN tập trung vào việc tạo reviews
- Không có reviews = doanh thu rất thấp
- Với 50+ reviews, ROI tăng 147x

---

## 3. CÁC INSIGHTS CHÍNH (7 INSIGHTS)

### Insight 1: Nghịch lý Volume vs Revenue
**Phát hiện:** Phân khúc dưới 100k có 55.7% sản phẩm nhưng chỉ 28.1% doanh thu
**Ý nghĩa:** Chiến lược volume không hiệu quả về mặt doanh thu
**Cơ hội:** Tăng tỷ trọng sản phẩm 100–300k (balance tốt: 26.4% sản phẩm, 28.8% doanh thu)

### Insight 2: Tập trung doanh thu cực cao
**Phát hiện:** Top 100 sản phẩm (0.24% catalog) tạo ra 31.8% tổng doanh thu
**Ý nghĩa:** Thị trường có hiệu ứng "winner takes all"
**Chiến lược:** Focus marketing vào top performers thay vì dàn trải

### Insight 3: Giá trị thương hiệu
**Phát hiện:** Branded products có giá cao gấp 4.1x OEM
**Ý nghĩa:** Khách hàng sẵn sàng trả premium cho thương hiệu
**Cơ hội:** Phát triển private label hoặc hợp tác với branded

### Insight 4: Review là yếu tố quyết định
**Phát hiện:** Correlation 0.621 giữa review_count và quantity_sold
**Ý nghĩa:** Review có tác động trực tiếp đến doanh số
**Hành động:** Chiến dịch khuyến khích review (incentive, follow-up)

### Insight 5: Danh mục Balo/Vali dẫn đầu
**Phát hiện:** Backpacks/Suitcases chiếm 33.6% doanh thu (29B VND)
**Ý nghĩa:** Nhu cầu du lịch, đi học/làm cao
**Cơ hội:** Mở rộng SKU trong danh mục này

### Insight 6: Giày Converse thống trị phân khúc cao cấp
**Phát hiện:** 2 trong top 5 sản phẩm doanh thu cao nhất là Converse (1.6-1.7M VND)
**Ý nghĩa:** Brand loyalty mạnh trong giày thể thao
**Chiến lược:** Partnership với các brand giày quốc tế khác

### Insight 7: OEM chiếm ưu thế về số lượng nhưng yếu về giá trị
**Phát hiện:** OEM = 73.8% sản phẩm nhưng chỉ 31.4% doanh thu
**Ý nghĩa:** Thị trường đang chuyển dịch sang branded
**Xu hướng:** Cơ hội cho các thương hiệu Việt Nam

---

## 4. ĐÁNH GIÁ THEO 7 TIÊU CHÍ TRỰC QUAN HÓA

### Tiêu chí 1: Kết hợp nguồn dữ liệu đáng tin cậy ✅
- Dữ liệu từ TIKI Vietnam (platform chính thức)
- Đã xử lý missing values, outliers, duplicates
- Validation logic: price ≤ original_price, rating [0-5]
- **Notebooks**: `01_data_loading.ipynb`, `02_data_quality.ipynb`

### Tiêu chí 2: Phù hợp với mục đích ✅
**Dashboard có 8 tabs, mỗi tab phục vụ mục đích cụ thể:**
- **Tổng quan**: Biểu đồ cột (so sánh doanh thu), thanh ngang (tỷ trọng khúc giá), bubble chart (đa chiều)
- **Phân tích giá**: Grouped bar (% SP vs % doanh thu), scatter log-scale, Q1 KPI (100–300k), Q2 discount theo danh mục, Q3 ROI theo khúc giá
- **Hiệu suất bán hàng**: Thanh ngang (tránh label dài), sequential color, Q5 top 10 sản phẩm tiềm năng (review cao / sales thấp)
- **Thương hiệu & thị trường**: Q7 `make_subplots` 1×3 (SKU, giá TB, doanh số TB) OEM vs Branded; Q8 rating TB (≥50 SP); Q9 dot plot vị thế giá
- **Tương tác khách hàng**: Q4 scatter (r = 0.621) + trendline log–log (numpy); Q6 proxy conversion rate
- **Tính năng sản phẩm**: Q10 bar gom nhóm ảnh → rating TB; Q11/Q12 `make_subplots` 2 hàng (lượng bán TB + số SKU)
- **Phân tích chuyên sâu**: Q13 line chart tuổi listing; Q14 sản phẩm mới ≤183 ngày; bộ lọc danh mục tương tác
- **Trợ lý AI**: Sinh code Gemini → duyệt → chạy sandbox → xem kết quả

### Tiêu chí 3: Rõ ràng và dễ hiểu ✅
**Thiết kế:**
- Toàn bộ nhãn, tiêu đề, KPI, hover đã chuyển sang **tiếng Việt**
- KPI cards với sub-metrics (context rõ ràng)
- Tiêu đề biểu đồ có insight ngay trong title
- Phối màu nhất quán: sequential một hue (xanh lam, cam đỏ) — theo *The Big Book of Dashboards*
- Tên sản phẩm dài được cắt ngắn (`str[:35] + "..."`)
- Tooltips hover hiển thị chi tiết, customdata cho n từng nhóm
- Đã loại biểu đồ pie/donut (vi phạm best-practice) → thanh ngang

### Tiêu chí 4: Sự tích hợp và liên kết ✅
**Liên kết giữa các tabs:**
- Tổng quan → Phân tích giá: Từ tổng quan phân khúc đến chi tiết giá
- Phân tích giá → Hiệu suất bán hàng: Từ giá đến hiệu suất bán
- Hiệu suất bán hàng → Thương hiệu & thị trường: Từ sản phẩm đến thương hiệu
- Thương hiệu → Tương tác khách hàng: Từ thương hiệu đến hành vi khách hàng
- Tính năng sản phẩm: Đánh giá tác động video, ảnh, trả sau
- Phân tích chuyên sâu: Tổng hợp tất cả với lọc tương tác + phân tích thời gian
- Trợ lý AI: Phân tích tùy chỉnh bằng ngôn ngữ tự nhiên

### Tiêu chí 5: Tương tác và điều hướng ✅
**Interactive features:**
- 8 tabs navigation (dễ chuyển đổi, tên tiếng Việt)
- Category filtering trong tab Phân tích chuyên sâu
- Hover tooltips trên tất cả biểu đồ (với customdata)
- Thanh công cụ Plotly: phóng to, pan, chọn vùng, lasso, xuất ảnh PNG
- Responsive layout (Bootstrap grid)
- AI Assistant: nhập câu hỏi → sinh code → duyệt → chạy → xem kết quả

### Tiêu chí 6: Thiết kế hấp dẫn ✅
**Visual design (theo *The Big Book of Dashboards*):**
- Nền trung tính (`#f8fafc` paper, `#e2e8f0` plot) — không gây phân tâm
- Sequential một hue (xanh lam `_SEQ_BLUE`, cam đỏ cho Q10) — tránh "cầu vồng"
- Sàn màu đủ tối so với nền để cột nhỏ không "chìm" (>= `#64748b`)
- Card-based layout với spacing nhất quán
- Consistent font family (`system-ui, sans-serif`)
- Đa dạng loại biểu đồ: bar, horizontal bar, scatter, line, dot plot, bubble, make_subplots

### Tiêu chí 7: Phân tích dữ liệu - Xu hướng và Kết luận ✅
**Thể hiện xu hướng:**
- Q4 scatter log–log: Xu hướng review → sales (trendline numpy polyfit, r = 0.621)
- Q13 line chart: Phân bố tuổi listing (trục ordinal, marker)
- Q5 sequential bar: Sản phẩm tiềm năng (nhiều review, ít bán)

**Kết luận rõ ràng:**
- Mỗi biểu đồ có insight trong title
- KPI cards có context (sub-metrics)
- Hệ số tương quan Pearson hiển thị rõ (0.621)
- Multiplier effects (147.4x, 4.1x) được highlight
- Q10 gom nhóm ảnh (bucket) để thấy pattern — tránh scatter nhiễu
- Q11/Q12 hai panel riêng (avg sold / SKU count) — không bị lệch thang

---

## 5. TÍCH HỢP AI (Tiêu chí 8)

### 5.1 Kiến trúc hệ thống AI

**Nguyên tắc thiết kế:**
✅ AI đề xuất và viết code
✅ Con người quyết định và phê duyệt
✅ Thực thi trên môi trường local (sandbox)
✅ Không thực thi ngầm - hiển thị code bắt buộc

**Kiến trúc 3-tier:**
```
Frontend (Dash tab "Trợ lý AI")
  → AI API (FastAPI /api/ai/generate — Gemini)
  → Execution API (FastAPI /api/execute/run — RestrictedPython sandbox)
  → Logs API (SQLite /api/logs/history)
```

### 5.2 Các API đã triển khai

#### A. AI API (FastAPI) ✅ ĐÃ TRIỂN KHAI
**Endpoint:** `POST /api/ai/generate`
**Input:**
- `user_request`: Yêu cầu phân tích bằng ngôn ngữ tự nhiên
- `context`: Thông tin về dataset (columns, dtypes, sample data)
- `conversation_history`: Lịch sử hội thoại

**Output:**
- `code`: Python code để thực hiện phân tích
- `explanation`: Giải thích bằng tiếng Việt về code
- `request_id`: ID để tracking
- `model_used`: Tên mô hình Gemini đã dùng

**AI Provider:** Google Gemini (hỗ trợ fallback models, xử lý rate limit 429)

#### B. Execution API (FastAPI) ✅ ĐÃ TRIỂN KHAI
**Endpoint:** `POST /api/execute/run`
**Input:**
- `code`: Code đã được con người chỉnh sửa và phê duyệt
- `request_id`: ID từ AI API

**Output:**
- `status`: success/error/validation_error
- `stdout`: Kết quả đầu ra
- `stderr`: Lỗi / traceback
- `outputs`: Danh sách biểu đồ Plotly HTML (iframe)
- `duration_ms`: Thời gian thực thi

**Security:**
- Whitelist libraries (pandas, numpy, matplotlib, seaborn, plotly)
- Timeout protection (max 30s)
- Sandbox environment (RestrictedPython)
- Code validation trước khi chạy (`api/utils/code_validator.py`)

#### C. Logs API (FastAPI) ✅ ĐÃ TRIỂN KHAI
**Endpoint:** `POST /api/logs/save` — Lưu request, code, results, timestamp
**Endpoint:** `GET /api/logs/history` — Truy xuất lịch sử phân tích

**Storage:** SQLite database (`api/database/schema.sql`)

### 5.3 Frontend AI Assistant Tab ✅ ĐÃ TRIỂN KHAI

**Workflow người dùng (đã hoạt động):**

1. **Nhập yêu cầu** — Textarea + nút "Gửi cho AI"
2. **Xem giải thích + code** — Markdown panel (tiếng Việt) + code editor có thể sửa
3. **Phê duyệt** — Nút "Phê duyệt & chạy" (code chỉ chạy khi bấm)
4. **Xem kết quả** — Stdout, stderr, biểu đồ Plotly HTML (iframe)
5. **Lịch sử** — Nút "Tải lịch sử" hiện danh sách request_id + trạng thái

### 5.4 Câu hỏi phân tích đã chuẩn bị (cho vấn đáp)

**Nhóm 1: Price Analysis**
1. Tính doanh thu trung bình của sản phẩm trong khoảng giá 100–300k VND
2. So sánh tỷ lệ discount giữa các danh mục sản phẩm
3. Tìm phân khúc giá có ROI cao nhất (revenue/product_count)

**Nhóm 2: Sales Performance**
4. Phân tích correlation giữa review_count và quantity_sold
5. Tìm top 10 sản phẩm có tiềm năng cao (high reviews, low sales)
6. Tính conversion rate ước tính từ review_count

**Nhóm 3: Brand Analysis**
7. So sánh hiệu suất bán hàng giữa OEM và Branded products
8. Tìm thương hiệu có rating trung bình cao nhất (min 50 products)
9. Phân tích price positioning của top 10 brands

**Nhóm 4: Product Features**
10. Ảnh hưởng của số lượng ảnh (number_of_images) đến rating
11. Tác động của video (has_video) đến quantity_sold
12. Phân tích sản phẩm có pay_later vs không có

**Nhóm 5: Temporal Analysis**
13. Xu hướng phân bố catalog theo tuổi listing (date_created)
14. Phân tích sản phẩm mới (tuổi listing ≤ 183 ngày ~ 6 tháng)

---

## 6. 14 CÂU HỎI ↔ BIỂU ĐỒ DASHBOARD (tất cả ✅)

| # | Câu hỏi | Tab | Loại biểu đồ | Ghi chú |
|---|---------|-----|---------------|---------|
| Q1 | Doanh thu TB 100–300k | Phân tích giá | KPI cards (3 thẻ) | Doanh thu TB / SP, Tổng doanh thu, Số SP |
| Q2 | Discount theo danh mục | Phân tích giá | Thanh ngang (sorted) | `color_continuous_scale='Oranges'` |
| Q3 | ROI theo khúc giá | Phân tích giá | Thanh đứng (sorted) | ROI = doanh thu / số SP |
| Q4 | Review → Sales | Tương tác KH | Scatter log–log + trendline | `numpy.polyfit`, annotation r=0.621 |
| Q5 | SP tiềm năng | Hiệu suất bán | Thanh ngang sequential | Score = review / (sold+1), loại sold=0 |
| Q6 | Conversion rate | Tương tác KH | Thanh đứng | Proxy: avg_sold / mid_review |
| Q7 | OEM vs Branded | Thương hiệu | `make_subplots` 1×3 | SKU, giá TB, doanh số TB |
| Q8 | Top brand by rating | Thương hiệu | Thanh ngang sorted | ≥50 SP, `color_continuous_scale='RdYlGn'` |
| Q9 | Price positioning | Thương hiệu | Dot plot (min/TB/max) | Top 10 thương hiệu, nghìn VND |
| Q10 | Ảnh → Rating | Tính năng SP | Thanh đứng (bucket) | Gom 1–5, 6–10…21+; cam đỏ gradient |
| Q11 | Video → Sales | Tính năng SP | `make_subplots` 2 hàng | Avg sold + SKU count |
| Q12 | Pay later → Sales | Tính năng SP | `make_subplots` 2 hàng | Avg sold + SKU count |
| Q13 | Phân bố tuổi listing | Chuyên sâu | Line chart (ordinal) | Khoảng ngày tiếng Việt, marker |
| Q14 | SP mới (≤183 ngày) | Chuyên sâu | Thanh ngang + KPI | Proxy 6 tháng, theo danh mục |

**Coverage: 14/14 câu hỏi = 100%** (trước đây chỉ 6/14 = 42.9%)

---

## 7. CÔNG NGHỆ SỬ DỤNG

### 7.1 Data Analysis Stack
- **Python 3.11**
- **pandas ≥ 2.0**: Data manipulation
- **numpy ≥ 1.24**: Tính toán (polyfit trendline)
- **scipy ≥ 1.10**: Statistical analysis
- **Jupyter Notebook**: EDA environment

### 7.2 Dashboard Stack
- **Dash ≥ 2.9**: Web framework
- **Plotly ≥ 5.14**: Interactive charts (px, go, make_subplots)
- **dash-bootstrap-components ≥ 1.4**: UI components (Bootstrap grid)
- **Flask** (built-in Dash server)

### 7.3 AI Integration Stack ✅ ĐÃ TRIỂN KHAI
- **FastAPI ≥ 0.95**: API framework (3 router: ai, execute, logs)
- **Google Generativeai (Gemini)**: AI code generation
- **RestrictedPython ≥ 6.0**: Code sandboxing
- **SQLAlchemy ≥ 2.0 + SQLite**: Logging database
- **python-dotenv**: Configuration management
- **Uvicorn**: ASGI server

---

## 8. KẾT QUẢ ĐẠT ĐƯỢC

### 8.1 Phase 1: EDA ✅ HOÀN THÀNH
- ✅ 5 notebooks phân tích chi tiết
- ✅ 41,576 sản phẩm đã được phân tích
- ✅ 7 insights chính với bằng chứng dữ liệu
- ✅ Phân tích sâu vào phân khúc giá rẻ (đặc điểm chính)
- ✅ Mô hình dự đoán doanh thu dựa trên review_count

### 8.2 Phase 2: Dashboard ✅ HOÀN THÀNH & NÂNG CẤP
- ✅ **8 tabs** tương tác với **30+ biểu đồ**
- ✅ Trả lời đầy đủ **14/14 câu hỏi** phân tích (trước đây 6/14)
- ✅ Toàn bộ nhãn giao diện bằng **tiếng Việt**
- ✅ Phối màu theo *The Big Book of Dashboards* (sequential một hue, nền trung tính)
- ✅ Loại bỏ pie/donut (vi phạm best-practice) → thanh ngang
- ✅ `make_subplots` cho Q7 (1×3), Q11/Q12 (2 hàng) — tránh gộp thang lệch
- ✅ Q10 gom nhóm ảnh (bucket bar) — tránh scatter nhiễu
- ✅ Q4 trendline log–log bằng numpy (không dùng statsmodels)
- ✅ Q13/Q14: `date_created` là **số ngày**, không phải Unix timestamp
- ✅ Professional KPI cards, hover tooltips, toolbar zoom/pan/export

### 8.3 Phase 3: AI System ✅ ĐÃ TRIỂN KHAI
- ✅ Kiến trúc 3-tier hoàn chỉnh (AI API → Execution API → Logs API)
- ✅ Tab "Trợ lý AI" hoạt động end-to-end
- ✅ Code sinh bởi Gemini, hiển thị + cho phép sửa, chạy sandbox
- ✅ Xử lý rate limit 429, fallback models
- ✅ Lịch sử truy vấn (SQLite)
- ✅ 14 câu hỏi phân tích đã chuẩn bị cho vấn đáp

---

## 9. ĐIỂM MẠNH CỦA DỰ ÁN

### 9.1 Phân tích sâu, không dàn trải
✅ **Đúng yêu cầu**: Tập trung phân tích sâu vào phân khúc giá rẻ (dưới 100k)
- Không chỉ nói "có nhiều sản phẩm giá rẻ"
- Mà phân tích: loại sản phẩm nào, thương hiệu gì, bán như thế nào, chất lượng ra sao
- Đưa ra bằng chứng cụ thể: 23,160 sản phẩm, 28.1% doanh thu, 23.2 sales/SKU

### 9.2 Dữ liệu nói lên điều gì
✅ **Đúng yêu cầu**: Mọi insight đều có bằng chứng từ dữ liệu
- Không đưa ra ý kiến chủ quan
- Mỗi phát hiện đều có số liệu cụ thể
- Ví dụ: "Review impact 147.4x" - tính toán từ avg_sales của 2 nhóm

### 9.3 Mô hình dự đoán với assumption rõ ràng
✅ **Đúng yêu cầu**: Sử dụng review_count để dự đoán doanh thu
- Correlation 0.621 (strong positive)
- Assumption model: Revenue = Price × f(review_count)
- Kịch bản đầu tư cụ thể với ROI estimate

### 9.4 Trả lời câu hỏi "Thị trường ngách?"
✅ **Đúng yêu cầu**: Phân tích và kết luận rõ ràng
- KHÔNG phải thị trường ngách
- Đây là mass market với volume cao, giá thấp
- Có bằng chứng: 23,160 SKU, đa dạng danh mục, giá thấp

### 9.5 Trực quan hóa theo best-practice
✅ Áp dụng nguyên tắc từ *The Big Book of Dashboards*:
- Thanh (length) cho so sánh — không dùng pie/donut
- Sequential một hue cho biến tổng hợp
- Nền trung tính, sàn màu đủ tối
- Gom nhóm (aggregation) khi dữ liệu thô quá nhiễu (Q10)
- Tách panel riêng khi thang lệch (Q11/Q12)

---

## 10. HƯỚNG PHÁT TRIỂN & KHUYẾN NGHỊ

### 10.1 Chiến lược cho Seller trên TIKI

**Nếu bán sản phẩm giá rẻ (<100k):**
1. Tập trung tạo reviews (incentive program)
2. Chọn danh mục phụ kiện thời trang (volume cao)
3. Chấp nhận margin thấp, focus vào volume
4. Đầu tư vào ảnh sản phẩm (number_of_images)

**Nếu bán sản phẩm branded (>300k):**
1. Focus vào chất lượng và brand building
2. Target danh mục Balo/Vali hoặc Giày
3. Margin cao hơn, volume thấp hơn
4. Đầu tư vào video sản phẩm

### 10.2 Cơ hội cho thương hiệu Việt Nam
- OEM chiếm 73.8% nhưng giá thấp
- Branded có premium 4.1x
- Cơ hội: Xây dựng thương hiệu Việt trong phân khúc 300k–1M
- Học hỏi từ Converse, LAZA, Lusetti

### 10.3 Tối ưu cho TIKI Platform
1. **Review Generation Program**: Khuyến khích review nhiều hơn (31.3% → 50%+)
2. **Category Expansion**: Tăng SKU trong Backpacks/Suitcases
3. **Brand Partnership**: Hợp tác với branded để tăng AOV
4. **Long-tail Optimization**: 82% sản phẩm <300k cần chiến lược riêng

---

## 11. KẾT LUẬN

### 11.1 Đáp ứng yêu cầu đồ án
✅ **Dữ liệu**: 41,576 rows, 19 biến, 100% Vietnam
✅ **Phân tích sâu**: Focus vào phân khúc giá rẻ với bằng chứng cụ thể
✅ **7 tiêu chí trực quan**: Dashboard đáp ứng đầy đủ
✅ **14/14 câu hỏi**: Tất cả đã có biểu đồ trên dashboard
✅ **AI Integration**: Triển khai hoàn chỉnh, tuân thủ nguyên tắc human-in-the-loop
✅ **Giao diện tiếng Việt**: Toàn bộ nhãn, tiêu đề, KPI, hover

### 11.2 Giá trị thực tiễn
Dự án không chỉ là bài tập học thuật mà còn cung cấp:
- Insights thực tế về thị trường thời trang online VN
- Công cụ phân tích cho sellers và platform
- Framework để mở rộng sang danh mục khác

### 11.3 Sẵn sàng cho vấn đáp
- ✅ 14 câu hỏi phân tích đã chuẩn bị — tất cả có biểu đồ trên dashboard
- ✅ Dashboard interactive sẵn sàng demo (8 tabs, tiếng Việt)
- ✅ AI module hoạt động end-to-end (Gemini → sandbox → kết quả)
- ✅ Hiểu sâu về dữ liệu và insights

---

## PHỤ LỤC

### A. Files trong dự án
```
├── notebooks/
│   ├── 01_data_loading.ipynb          # Load & combine 6 CSV
│   ├── 02_data_quality.ipynb          # Quality checks
│   ├── 03_exploratory_analysis.ipynb  # Initial EDA
│   ├── 04_deep_segment_analysis.ipynb # Deep dive
│   └── 05_insights_summary.ipynb      # Insights JSON
├── dashboard/
│   ├── app.py                         # Main Dash app (8 tabs, callbacks)
│   ├── layouts/
│   │   ├── overview.py                # Tổng quan
│   │   ├── price_analysis.py          # Phân tích giá (Q1–Q3)
│   │   ├── sales_performance.py       # Hiệu suất bán hàng (Q5)
│   │   ├── brand_market.py            # Thương hiệu & thị trường (Q7–Q9)
│   │   ├── customer_engagement.py     # Tương tác khách hàng (Q4, Q6)
│   │   ├── product_features.py        # Tính năng sản phẩm (Q10–Q12)
│   │   ├── deep_dive.py              # Phân tích chuyên sâu (Q13–Q14)
│   │   └── ai_assistant.py           # Trợ lý AI (frontend)
│   └── callbacks/
│       └── ai_callbacks.py            # Callbacks cho AI tab
├── api/
│   ├── main.py                        # FastAPI app
│   ├── routers/
│   │   ├── ai_router.py              # /api/ai/generate
│   │   ├── execution_router.py       # /api/execute/run
│   │   └── logs_router.py            # /api/logs/history
│   ├── services/
│   │   ├── ai_service.py             # Gemini integration
│   │   ├── execution_service.py      # Sandbox runner
│   │   └── logs_service.py           # SQLite logging
│   ├── utils/
│   │   ├── code_validator.py         # Code safety checks
│   │   ├── data_loader.py            # Dataset loader (cùng nhãn price_segment)
│   │   └── sandbox.py                # RestrictedPython wrapper
│   ├── database/schema.sql           # SQLite schema
│   └── config.py                      # Settings
├── data/
│   └── processed/
│       ├── combined_tiki_data.csv     # 41,576 products
│       └── insights_summary.json      # Key findings
├── tests/
│   ├── test_api_health.py
│   ├── test_code_validator.py
│   └── test_sandbox_execute.py
├── run_dashboard.py                   # Chạy dashboard (port 8050)
├── run_api.py                         # Chạy API (port 8000)
├── requirements.txt                   # Dependencies
├── SKILLS_REPORT.md                   # Báo cáo này
├── DASHBOARD_QUESTIONS_MAPPING.md     # Mapping 14 Q ↔ biểu đồ
├── Current_Stage.md                   # Tiến độ
├── IMPLEMENTATION_PLAN.md             # Kế hoạch triển khai
├── book.md                            # Best-practice trích dẫn
└── README.md                          # Hướng dẫn dự án
```

### B. Cách chạy Dashboard
```bash
cd /Users/lyanhquan/code/HCMUS-TQHDL-Lab02
python run_dashboard.py
# Mở trình duyệt: http://localhost:8050
```

### C. Cách chạy API (cho tab Trợ lý AI)
```bash
# Tạo file .env với GEMINI_API_KEY
python run_api.py
# API chạy tại: http://localhost:8000
```

### D. Thống kê dự án
- **Lines of code**: ~5,000+ lines (Python)
- **Notebooks**: 5 files
- **Visualizations**: 30+ biểu đồ tương tác
- **Câu hỏi phân tích**: 14/14 đã trả lời (100%)
- **Ngôn ngữ giao diện**: Tiếng Việt
- **Technologies**: 15+ libraries/frameworks
- **Phase 1–3**: Tất cả hoàn thành

---

**Ngày hoàn thành Phase 1–3**: 2026-05-13
**Trạng thái**: Sẵn sàng cho vấn đáp và demo
