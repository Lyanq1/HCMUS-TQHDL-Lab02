# Current Stage: Phase 1–3 Complete ✅

## Phase 1: Data Exploration & Deep EDA ✅ HOÀN THÀNH

### Key Insights Discovered:
1. **Price Segment Dominance**: Phân khúc dưới 100k chiếm 55.7% sản phẩm nhưng chỉ 28.1% doanh thu
2. **Revenue Concentration**: Top 100 sản phẩm (0.24% catalog) tạo 31.8% tổng doanh thu
3. **OEM vs Branded**: 73.8% OEM, branded có giá cao gấp 4.1x
4. **Review Impact**: Pearson r = 0.621 — sản phẩm 50+ review bán tốt hơn đáng kể
5. **Top Categories**: backpacks_suitcases, men_shoes, fashion_accessories

### Files Created:
- 5 EDA notebooks (01–05)
- Combined dataset: 41,576 sản phẩm
- Insights summary JSON

## Phase 2: Dashboard Implementation ✅ HOÀN THÀNH & NÂNG CẤP

### Dashboard Structure:
- **Framework**: Dash + Plotly + Bootstrap
- **Port**: 8050
- **8 Interactive Tabs** (toàn bộ tiếng Việt):
  1. **Tổng quan** — KPI cards, doanh thu theo danh mục, tỷ trọng khúc giá, bubble chart, so sánh chuẩn hóa
  2. **Phân tích giá** — Q1 KPI (100–300k), Q2 discount theo danh mục, Q3 ROI theo khúc giá, grouped bar, scatter log-scale
  3. **Hiệu suất bán hàng** — Top 10 bán chạy / doanh thu (thanh ngang), phân bố SKU, tổng lượng bán, Q5 sản phẩm tiềm năng
  4. **Thương hiệu & thị trường** — Q7 `make_subplots` 1×3 OEM vs Branded, Q8 top rating ≥50 SP, Q9 dot plot vị thế giá
  5. **Tương tác khách hàng** — Q4 scatter r=0.621 + trendline numpy, Q6 proxy conversion rate, phân bố review/rating
  6. **Tính năng sản phẩm** — Q10 bar gom nhóm ảnh→rating (cam đỏ), Q11/Q12 `make_subplots` 2 hàng (video, trả sau)
  7. **Phân tích chuyên sâu** — Q13 line chart tuổi listing, Q14 SP mới ≤183 ngày, bộ lọc danh mục tương tác
  8. **Trợ lý AI** — Sinh code Gemini → duyệt → chạy sandbox → kết quả

### Enhancements Made:
- ✅ Toàn bộ nhãn giao diện **tiếng Việt** (tab, title, axis, KPI, hover, colorbar)
- ✅ **14/14 câu hỏi** phân tích đã có biểu đồ trực tiếp (100%)
- ✅ Loại bỏ pie/donut → thanh ngang (theo *The Big Book of Dashboards*)
- ✅ Phối màu sequential một hue (xanh lam, cam đỏ) — nền trung tính `#f8fafc`/`#e2e8f0`
- ✅ `make_subplots` cho Q7 (1×3), Q11/Q12 (2 hàng) — tránh gộp thang lệch
- ✅ Q10: gom nhóm ảnh (bucket bar) thay scatter nhiễu
- ✅ Q4: trendline log–log bằng numpy polyfit (không statsmodels)
- ✅ Q13/Q14: `date_created` là số ngày, không phải Unix timestamp
- ✅ Tên sản phẩm cắt ngắn, thanh ngang cho label dài
- ✅ Toolbar: zoom, pan, chọn vùng, lasso, xuất ảnh PNG
- ✅ `price_segment` nhãn tiếng Việt (Dưới 100k, 100–300k, 300–500k, 500k–1tr, Trên 1tr)

### Files:
- `dashboard/app.py` — Main Dash app (8 tabs, callbacks, feature engineering)
- `dashboard/layouts/*.py` — 8 layout modules (7 phân tích + AI)
- `dashboard/callbacks/ai_callbacks.py` — Callbacks cho tab Trợ lý AI
- `run_dashboard.py` — Script khởi chạy

## Phase 3: AI System ✅ ĐÃ TRIỂN KHAI

### Kiến trúc 3-tier:
```
Dash tab "Trợ lý AI" → FastAPI
  ├── /api/ai/generate      (Gemini sinh code + giải thích)
  ├── /api/execute/run       (RestrictedPython sandbox)
  └── /api/logs/history      (SQLite lịch sử)
```

### Components:
- ✅ AI API — Gemini code generation (fallback models, xử lý 429)
- ✅ Execution API — RestrictedPython sandbox, code validation, timeout
- ✅ Logs API — SQLite logging (request_id, status, timestamps)
- ✅ Frontend — Nhập yêu cầu → xem code + giải thích → sửa → phê duyệt → kết quả

### Files:
- `api/main.py` — FastAPI app
- `api/routers/{ai,execution,logs}_router.py` — 3 routers
- `api/services/{ai,execution,logs}_service.py` — Business logic
- `api/utils/{code_validator,data_loader,sandbox}.py` — Utilities
- `api/database/schema.sql` — SQLite schema
- `api/config.py` — Settings
- `run_api.py` — Script khởi chạy API (port 8000)

## Cách chạy

```bash
cd /Users/lyanhquan/code/HCMUS-TQHDL-Lab02

# Dashboard
python run_dashboard.py
# Mở trình duyệt: http://localhost:8050

# API (cho tab Trợ lý AI)
python run_api.py
# API tại: http://localhost:8000
```

## Trạng thái: Sẵn sàng vấn đáp & demo
- Phase 1 (EDA): ✅
- Phase 2 (Dashboard): ✅ (8 tabs, 30+ biểu đồ, 14/14 Q, tiếng Việt)
- Phase 3 (AI): ✅ (Gemini + sandbox + logging)
