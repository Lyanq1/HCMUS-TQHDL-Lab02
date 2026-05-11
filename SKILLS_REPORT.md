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
- Phân khúc 0-100k VND: **55.7% sản phẩm** nhưng chỉ **28.1% doanh thu**
- Phân khúc 100-300k VND: **26.4% sản phẩm**, **28.8% doanh thu**
- **Kết luận**: 82.1% sản phẩm tập trung ở phân khúc giá rẻ (<300k)

### 2.2 Phân tích sâu phân khúc 0-100k VND

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
1. **Volume cao**: 23,160 sản phẩm trong phân khúc 0-100k
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

**Kịch bản đầu tư vào phân khúc 0-100k:**

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

## 3. CÁC INSIGHTS CHÍNH (5-10 INSIGHTS)

### Insight 1: Nghịch lý Volume vs Revenue
**Phát hiện:** Phân khúc 0-100k có 55.7% sản phẩm nhưng chỉ 28.1% doanh thu
**Ý nghĩa:** Chiến lược volume không hiệu quả về mặt doanh thu
**Cơ hội:** Tăng tỷ trọng sản phẩm 100-300k (balance tốt: 26.4% sản phẩm, 28.8% doanh thu)

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
**Dashboard có 7 tabs, mỗi tab phục vụ mục đích cụ thể:**
- **Overview**: Biểu đồ cột (so sánh doanh thu), Donut chart (phân bố), Bubble chart (đa chiều)
- **Price Analysis**: Grouped bar (so sánh %), Scatter plot log-scale (xu hướng)
- **Sales Performance**: Horizontal bar (tránh label dài), Dual charts (volume vs revenue)
- **Brand & Market**: Comparison chart (OEM vs Branded)
- **Customer Engagement**: Bar chart với text labels (impact rõ ràng)
- **Deep Dive**: Interactive filtering

### Tiêu chí 3: Rõ ràng và dễ hiểu ✅
**Thiết kế:**
- KPI cards với sub-metrics (context rõ ràng)
- Chart titles có insights ngay trong title
- Color coding nhất quán (xanh = revenue, đỏ = sales, tím = engagement)
- Truncated labels cho tên sản phẩm dài
- Tooltips hiển thị chi tiết khi hover

### Tiêu chí 4: Sự tích hợp và liên kết ✅
**Liên kết giữa các tabs:**
- Overview → Price Analysis: Từ tổng quan phân khúc đến chi tiết giá
- Price Analysis → Sales Performance: Từ giá đến hiệu suất bán
- Sales Performance → Brand & Market: Từ sản phẩm đến thương hiệu
- Brand & Market → Customer Engagement: Từ thương hiệu đến hành vi khách hàng
- Deep Dive: Tổng hợp tất cả với filtering

### Tiêu chí 5: Tương tác và điều hướng ✅
**Interactive features:**
- 7 tabs navigation (dễ chuyển đổi)
- Category filtering trong Deep Dive tab
- Hover tooltips trên tất cả charts
- Color-coded legends
- Responsive layout (Bootstrap grid)

### Tiêu chí 6: Thiết kế hấp dẫn ✅
**Visual design:**
- Color gradients (Blues, Greens, Reds, Purples, Viridis)
- Card-based layout với shadows
- Consistent spacing và alignment
- Professional color schemes
- Chart variety (bar, scatter, pie, donut, bubble)

### Tiêu chí 7: Phân tích dữ liệu - Xu hướng và Kết luận ✅
**Thể hiện xu hướng:**
- Price vs Sales scatter: Xu hướng giá cao = sales thấp
- Review impact: Xu hướng tăng mạnh khi có nhiều reviews
- Segment comparison: Xu hướng chuyển từ volume sang value

**Kết luận rõ ràng:**
- Mỗi chart có insight trong title
- KPI cards có context (sub-metrics)
- Correlation numbers hiển thị rõ (0.621)
- Multiplier effects (147.4x, 4.1x) được highlight

---

## 5. TÍCH HỢP AI (Tiêu chí 8)

### 5.1 Kiến trúc hệ thống AI

**Nguyên tắc thiết kế:**
✅ AI đề xuất và viết code
✅ Con người quyết định và phê duyệt
✅ Thực thi trên môi trường local
✅ Không thực thi ngầm - hiển thị code bắt buộc

**Kiến trúc 3-tier:**
```
Frontend (Dash) → AI API → Execution API → Local Python
                     ↓
                 Logs API (SQLite)
```

### 5.2 Các API đã thiết kế

#### A. AI API (FastAPI)
**Endpoint:** `POST /api/ai/generate`
**Input:**
- `user_request`: Yêu cầu phân tích bằng ngôn ngữ tự nhiên
- `context`: Thông tin về dataset (columns, dtypes, sample data)
- `conversation_history`: Lịch sử hội thoại

**Output:**
- `code`: Python code để thực hiện phân tích
- `explanation`: Giải thích bằng tiếng Việt về code
- `request_id`: ID để tracking

**AI Provider:** Hỗ trợ OpenAI, Google Gemini, hoặc Ollama (local)

#### B. Execution API (FastAPI)
**Endpoint:** `POST /api/execute/run`
**Input:**
- `code`: Code đã được con người chỉnh sửa và phê duyệt
- `request_id`: ID từ AI API
- `data_context`: Path đến dataset

**Output:**
- `status`: success/error
- `results`: Kết quả phân tích (numbers, dataframes)
- `plots`: Base64 encoded images của biểu đồ
- `logs`: Execution logs
- `execution_time`: Thời gian thực thi

**Security:**
- Whitelist libraries (pandas, numpy, matplotlib, seaborn)
- Timeout protection (max 30s)
- Sandbox environment (RestrictedPython)
- No file system write access

#### C. Logs API (FastAPI)
**Endpoint:** `POST /api/logs/save`
- Lưu: request, code, results, timestamp, user_edits

**Endpoint:** `GET /api/logs/history`
- Truy xuất lịch sử phân tích

**Storage:** SQLite database với schema:
```sql
CREATE TABLE analysis_logs (
    id INTEGER PRIMARY KEY,
    request_id TEXT,
    user_request TEXT,
    generated_code TEXT,
    edited_code TEXT,
    explanation TEXT,
    results TEXT,
    status TEXT,
    created_at TIMESTAMP
);
```

### 5.3 Frontend AI Assistant Tab

**Workflow người dùng:**

1. **Request Input Section**
   - Text area để nhập yêu cầu phân tích
   - Ví dụ: "Tính doanh thu trung bình của sản phẩm trong khoảng giá 100-300k"
   - Gợi ý câu hỏi phổ biến

2. **Code Display & Edit Section**
   - Syntax highlighting (Python)
   - Editable code editor
   - Explanation panel (tiếng Việt)
   - Ví dụ explanation: "Đoạn code này sẽ filter sản phẩm có giá 100-300k, sau đó tính mean của cột revenue_estimate"

3. **Approval Section**
   - Button "Chỉnh sửa Code" (nếu cần)
   - Button "Phê duyệt & Thực thi" (màu xanh, prominent)
   - Button "Hủy" (màu đỏ)
   - Checkbox xác nhận: "Tôi đã kiểm tra code và đồng ý thực thi"

4. **Results Display Section**
   - Numerical results (formatted tables)
   - Charts/plots (rendered images)
   - Execution logs
   - Download results button

5. **History Sidebar**
   - List các phân tích đã thực hiện
   - Click để xem lại code và results
   - Search/filter history

### 5.4 Câu hỏi phân tích đã chuẩn bị (cho vấn đáp)

**Nhóm 1: Price Analysis**
1. Tính doanh thu trung bình của sản phẩm trong khoảng giá 100-300k VND
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
13. Xu hướng ra mắt sản phẩm theo thời gian (date_created)
14. Phân tích sản phẩm mới (launched trong 6 tháng gần nhất)

---

## 6. CÔNG NGHỆ SỬ DỤNG

### 6.1 Data Analysis Stack
- **Python 3.8+**
- **pandas, numpy**: Data manipulation
- **matplotlib, seaborn**: Static visualizations
- **scipy**: Statistical analysis
- **Jupyter Notebook**: EDA environment

### 6.2 Dashboard Stack
- **Dash**: Web framework
- **Plotly**: Interactive charts
- **Bootstrap**: UI components
- **Flask**: Backend server

### 6.3 AI Integration Stack (Phase 3 - Planned)
- **FastAPI**: API framework
- **OpenAI API / Google Gemini**: AI models
- **RestrictedPython**: Code sandboxing
- **SQLite**: Logging database
- **python-dotenv**: Configuration management

---

## 7. KẾT QUẢ ĐẠT ĐƯỢC

### 7.1 Phase 1: EDA ✅ HOÀN THÀNH
- ✅ 5 notebooks phân tích chi tiết
- ✅ 41,576 sản phẩm đã được phân tích
- ✅ 7 insights chính với bằng chứng dữ liệu
- ✅ Phân tích sâu vào phân khúc giá rẻ (đặc điểm chính)
- ✅ Mô hình dự đoán doanh thu dựa trên review_count

### 7.2 Phase 2: Dashboard ✅ HOÀN THÀNH & NÂNG CẤP
- ✅ 7 tabs interactive với 28+ visualizations
- ✅ Đáp ứng đầy đủ 7 tiêu chí trực quan hóa
- ✅ Fixed UI issues (long labels, color coding)
- ✅ Enhanced với KPI cards, comparison charts
- ✅ Professional design với Bootstrap

### 7.3 Phase 3: AI System 🔄 ĐÃ THIẾT KẾ
- ✅ Kiến trúc 3-tier đã được thiết kế
- ✅ API specifications hoàn chỉnh
- ✅ 14 câu hỏi phân tích đã chuẩn bị
- ⏳ Implementation đang chờ triển khai

---

## 8. ĐIỂM MẠNH CỦA DỰ ÁN

### 8.1 Phân tích sâu, không dàn trải
✅ **Đúng yêu cầu**: Tập trung phân tích sâu vào phân khúc giá rẻ (0-100k)
- Không chỉ nói "có nhiều sản phẩm giá rẻ"
- Mà phân tích: loại sản phẩm nào, thương hiệu gì, bán như thế nào, chất lượng ra sao
- Đưa ra bằng chứng cụ thể: 23,160 sản phẩm, 28.1% doanh thu, 23.2 sales/SKU

### 8.2 Dữ liệu nói lên điều gì
✅ **Đúng yêu cầu**: Mọi insight đều có bằng chứng từ dữ liệu
- Không đưa ra ý kiến chủ quan
- Mỗi phát hiện đều có số liệu cụ thể
- Ví dụ: "Review impact 147.4x" - tính toán từ avg_sales của 2 nhóm

### 8.3 Mô hình dự đoán với assumption rõ ràng
✅ **Đúng yêu cầu**: Sử dụng review_count để dự đoán doanh thu
- Correlation 0.621 (strong positive)
- Assumption model: Revenue = Price × f(review_count)
- Kịch bản đầu tư cụ thể với ROI estimate

### 8.4 Trả lời câu hỏi "Thị trường ngách?"
✅ **Đúng yêu cầu**: Phân tích và kết luận rõ ràng
- KHÔNG phải thị trường ngách
- Đây là mass market với volume cao, giá thấp
- Có bằng chứng: 23,160 SKU, đa dạng danh mục, giá thấp

---

## 9. HƯỚNG PHÁT TRIỂN & KHUYẾN NGHỊ

### 9.1 Chiến lược cho Seller trên TIKI

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

### 9.2 Cơ hội cho thương hiệu Việt Nam
- OEM chiếm 73.8% nhưng giá thấp
- Branded có premium 4.1x
- Cơ hội: Xây dựng thương hiệu Việt trong phân khúc 300k-1M
- Học hỏi từ Converse, LAZA, Lusetti

### 9.3 Tối ưu cho TIKI Platform
1. **Review Generation Program**: Khuyến khích review nhiều hơn (31.3% → 50%+)
2. **Category Expansion**: Tăng SKU trong Backpacks/Suitcases
3. **Brand Partnership**: Hợp tác với branded để tăng AOV
4. **Long-tail Optimization**: 82% sản phẩm <300k cần chiến lược riêng

---

## 10. KẾT LUẬN

### 10.1 Đáp ứng yêu cầu đồ án
✅ **Dữ liệu**: 41,576 rows, 19 biến, 100% Vietnam
✅ **Phân tích sâu**: Focus vào phân khúc giá rẻ với bằng chứng cụ thể
✅ **7 tiêu chí trực quan**: Dashboard đáp ứng đầy đủ
✅ **AI Integration**: Thiết kế hoàn chỉnh, tuân thủ nguyên tắc

### 10.2 Giá trị thực tiễn
Dự án không chỉ là bài tập học thuật mà còn cung cấp:
- Insights thực tế về thị trường thời trang online VN
- Công cụ phân tích cho sellers và platform
- Framework để mở rộng sang danh mục khác

### 10.3 Sẵn sàng cho vấn đáp
- ✅ 14 câu hỏi phân tích đã chuẩn bị
- ✅ Dashboard interactive sẵn sàng demo
- ✅ AI module có kiến trúc rõ ràng để trình bày
- ✅ Hiểu sâu về dữ liệu và insights

---

## PHU LỤC

### A. Files trong dự án
```
├── notebooks/
│   ├── 01_data_loading.ipynb          # Load & combine 6 CSV
│   ├── 02_data_quality.ipynb          # Quality checks
│   ├── 03_exploratory_analysis.ipynb  # Initial EDA
│   ├── 04_deep_segment_analysis.ipynb # Deep dive
│   └── 05_insights_summary.ipynb      # Insights JSON
├── dashboard/
│   ├── app.py                         # Main Dash app
│   └── layouts/                       # 7 tab layouts
├── data/
│   └── processed/
│       ├── combined_tiki_data.csv     # 41,576 products
│       └── insights_summary.json      # Key findings
├── IMPLEMENTATION_PLAN.md             # Full plan
├── Current_Stage.md                   # Progress tracker
└── SKILLS_REPORT.md                   # This report
```

### B. Cách chạy Dashboard
```bash
cd /Users/lyanhquan/code/HCMUS-TQHDL-Lab02
python run_dashboard.py
# Open: http://localhost:8050
```

### C. Thống kê dự án
- **Lines of code**: ~3,500 lines (Python)
- **Notebooks**: 5 files
- **Visualizations**: 28+ interactive charts
- **Analysis time**: Phase 1-2 complete
- **Technologies**: 10+ libraries/frameworks

---

**Ngày hoàn thành Phase 1-2**: 2026-05-11
**Trạng thái**: Sẵn sàng cho vấn đáp và demo
**Next step**: Implement Phase 3 (AI System)
