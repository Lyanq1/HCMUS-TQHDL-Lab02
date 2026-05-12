# TIKI E-Commerce Data Visualization Project

Dashboard phân tích dữ liệu thời trang TIKI với tích hợp AI.

## Project Structure

```
final/
├── dataset/              # CSV files gốc
├── data/
│   ├── processed/        # Dữ liệu đã xử lý
│   └── temp/            # Kết quả tạm thời
├── notebooks/           # Jupyter notebooks EDA
├── dashboard/           # Dashboard application
├── api/                 # FastAPI backend
├── config/              # Configuration files
└── docs/               # Documentation
```

## Phase 1: EDA (Completed)

5 notebooks phân tích dữ liệu:
- `01_data_loading.ipynb` - Load và consolidate data
- `02_data_quality.ipynb` - Kiểm tra chất lượng dữ liệu
- `03_exploratory_analysis.ipynb` - Phân tích khám phá
- `04_deep_segment_analysis.ipynb` - Phân tích sâu segments
- `05_insights_summary.ipynb` - Tổng hợp insights

## Phase 2: Dashboard (Complete)

Interactive dashboard với Dash + Plotly:
- Overview Dashboard
- Price Analysis
- Sales Performance
- Brand & Market Analysis
- Customer Engagement
- Product Features
- Deep Dive Explorer
- AI Analysis Assistant (tab tích hợp FastAPI)

## Phase 3: AI Integration (Complete)

Hệ thống human-in-the-loop theo `requirement.md`:
- **POST `/api/ai/generate`** — Gemini (Google AI Studio) trả JSON: `code` + `explanation` (comment tiếng Việt trong code), lưu SQLite.
- **POST `/api/execute/run`** — Chạy mã đã chỉnh sửa/phê duyệt trong sandbox (process + timeout), biến `df` có sẵn; biểu đồ Plotly gán `fig` → file HTML dưới `data/temp/`, phục vụ qua **`GET /static/...`**.
- **GET `/api/logs/history`** và **GET `/api/logs/{request_id}`** — Lịch sử yêu cầu / thực thi.
- Tab **AI Assistant** trên Dash: gửi yêu cầu → chỉnh code → Phê duyệt & chạy → xem stdout / iframe biểu đồ.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Đặt GEMINI_API_KEY (Google AI Studio). Tuỳ chọn: GEMINI_MODEL (mặc định gemini-1.5-flash),
# GEMINI_FALLBACK_MODELS (danh sách model dự phòng khi 429), DASH_API_BASE.
# Nếu gặp lỗi quota với gemini-2.0-flash trên free tier, đổi GEMINI_MODEL sang gemini-1.5-flash.
```

3. Run EDA notebooks:
```bash
jupyter notebook notebooks/
```

4. Chạy API backend (terminal 1 — bắt buộc trước khi dùng tab AI):
```bash
cd /path/to/HCMUS-TQHDL-Lab02
python run_api.py
# API: http://127.0.0.1:8000  (health: /health)
```

5. Chạy dashboard (terminal 2):
```bash
python run_dashboard.py
# Mở http://127.0.0.1:8050 — tab "AI Assistant"
```

**Gợi ý câu hỏi demo (vấn đáp):** so sánh OEM vs thương hiệu theo `revenue_estimate`; phân bố `quantity_sold` theo `price_segment`; scatter `review_count` vs `quantity_sold` (log scale); top 5 `category` theo tổng doanh thu; mối quan hệ `discount_pct` và `rating_average` theo nhóm giá.

## Requirements

- Python 3.8+
- pandas, numpy, matplotlib, seaborn, plotly
- dash, dash-bootstrap-components
- fastapi, uvicorn, google-generativeai, requests, python-dotenv

**Kiểm thử:** `pytest tests/` (mặc định không chạy sandbox tích hợp; đặt `RUN_SANDBOX_TESTS=1` nếu môi trường pandas/plotly/NumPy tương thích).

## Data

TIKI e-commerce fashion products:
- 41,616 products across 6 categories
- 19 features including price, sales, ratings, reviews
- 100% Vietnam data

## Key Insights

1. **Price Segments**: Dominant segment analysis
2. **Revenue Concentration**: Top performers drive majority of revenue
3. **Review Impact**: Strong correlation between reviews and sales
4. **Brand Structure**: OEM vs branded product dynamics
5. **Market Opportunities**: High engagement, low sales products

See `data/processed/insights_summary.json` for detailed findings.
