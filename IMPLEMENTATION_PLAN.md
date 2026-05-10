# TIKI E-Commerce Data Visualization Project - Implementation Plan

## Project Overview

**Dataset Summary:**
- 6 CSV files with 41,616 total rows
- 19 features including: id, name, description, original_price, price, fulfillment_type, brand, review_count, rating_average, favourite_count, pay_later, current_seller, date_created, number_of_images, vnd_cashback, has_video, category, quantity_sold
- 100% Vietnam data (TIKI platform)
- Categories: Backpacks/Suitcases, Fashion Accessories, Men/Women Bags, Men/Women Shoes

---

## Phase 1: Data Exploration & Deep EDA

### Objective
Conduct thorough exploratory data analysis to extract meaningful insights, focusing on specific market segments rather than shallow broad analysis.

### Key Tasks

**1.1 Data Loading & Consolidation**
- Load all 6 CSV files into pandas DataFrames
- Add category column to distinguish product types
- Combine into unified dataset
- Validate data integrity (check for duplicates, missing values)

**1.2 Data Quality Assessment**
- Identify missing values per column
- Detect outliers in price, rating_average, quantity_sold
- Check data type consistency
- Analyze date_created range and distribution
- Validate price relationships (price <= original_price)

**1.3 Initial Exploratory Analysis**
- Overall statistics: mean, median, std for numerical columns
- Price distribution across all products
- Brand distribution and market concentration
- Category-wise product counts
- Review and rating patterns

**1.4 Deep Segment Analysis (CRITICAL)**

Focus on identifying dominant market segments, then drill deep:

**Price Segment Analysis:**
- Segment products into price ranges (0-100k, 100-300k, 300-500k, 500k-1M, 1M+)
- Identify which segment dominates
- For dominant segment, analyze:
  - Specific product types within this range
  - Which categories contribute most
  - Brand concentration in this segment
  - Quality indicators (rating_average, review_count)
  - Sales performance (quantity_sold)
  - Is this a niche market or mass market?

**Sales Performance Deep Dive:**
- Identify top-selling products (by quantity_sold)
- Analyze characteristics of best sellers:
  - Price positioning
  - Brand patterns
  - Review count correlation
  - Rating patterns
  - Discount patterns (original_price vs price)
- Compare similar products to understand what drives sales

**Revenue Potential Analysis:**
- Calculate estimated revenue: price × quantity_sold
- Identify high-revenue products vs high-volume products
- Use review_count as proxy for market interest
- Build assumptions/models to predict revenue potential:
  - Correlation between review_count and quantity_sold
  - Price elasticity patterns
  - Category-specific conversion patterns

**Brand & Market Structure:**
- Identify major brands vs OEM products
- Market share by brand
- Price positioning by brand
- Quality perception (rating) by brand
- Sales performance by brand

**Customer Engagement Patterns:**
- Analyze review_count distribution
- Rating patterns and their relationship to sales
- Favourite_count as engagement indicator
- Identify products with high engagement but low sales (opportunity?)
- Products with high sales but low engagement (commodity?)

**1.5 Insight Generation**
- Document 5-10 key insights with data evidence
- Identify market opportunities
- Prepare data stories for visualization
- Define analysis questions for presentation

### Technologies
- Python 3.8+
- pandas, numpy for data manipulation
- matplotlib, seaborn for exploratory plots
- scipy for statistical analysis

### Files to Create
- `notebooks/01_data_loading.ipynb`
- `notebooks/02_data_quality.ipynb`
- `notebooks/03_exploratory_analysis.ipynb`
- `notebooks/04_deep_segment_analysis.ipynb`
- `notebooks/05_insights_summary.ipynb`
- `data/processed/combined_tiki_data.csv`
- `data/processed/insights_summary.json`

---

## Phase 2: Dashboard Design

### Objective
Design interactive dashboard that tells the data story discovered in EDA, with purpose-appropriate visualizations and clear navigation.

### Key Tasks

**2.1 Define Core Visualizations**

**Overview Section:**
- KPI cards: Total products, Total revenue estimate, Avg rating, Total brands
- Price distribution histogram with segment highlights
- Category breakdown (treemap or pie chart)
- Sales performance overview (bar chart: top 10 products)

**Price Analysis Section:**
- Price range distribution (bar chart)
- Price vs Sales scatter plot (with trend line)
- Discount analysis: original_price vs price (box plot by category)
- Price positioning by brand (violin plot)

**Sales Performance Section:**
- Top products by quantity_sold (horizontal bar chart)
- Revenue heatmap (category × price segment)
- Sales trend over time (line chart using date_created)
- Correlation matrix: price, rating, review_count, quantity_sold

**Brand & Market Section:**
- Brand market share (sunburst chart)
- Brand positioning map (scatter: avg_price vs avg_rating)
- OEM vs Branded comparison (grouped bar charts)
- Top brands by revenue (bar chart)

**Customer Engagement Section:**
- Review count distribution (histogram)
- Rating distribution (bar chart)
- Engagement vs Sales (scatter: review_count vs quantity_sold)
- High-potential products (high engagement, low sales)

**Deep Dive Section (Interactive):**
- Product detail explorer (filterable table)
- Similar product comparison tool
- Custom segment analyzer (user-defined filters)

**2.2 Design Interactive Elements**
- Cross-filtering: selecting a category filters all charts
- Drill-down: click price segment to see products within
- Hover tooltips: show detailed info on data points
- Range sliders: filter by price, rating, quantity_sold
- Category/brand multi-select filters
- Date range selector for temporal analysis

**2.3 Dashboard Layout & Navigation**

```
Header: Title, Filters (Category, Brand, Price Range)
├── Tab 1: Overview Dashboard
├── Tab 2: Price Analysis
├── Tab 3: Sales Performance
├── Tab 4: Brand & Market
├── Tab 5: Customer Engagement
├── Tab 6: Deep Dive Explorer
└── Tab 7: AI Analysis Assistant
```

### Technologies
- Plotly for interactive visualizations
- Dash for dashboard framework
- Bootstrap/CSS for styling

### Files to Create
- `dashboard/app.py`
- `dashboard/layouts/overview.py`
- `dashboard/layouts/price_analysis.py`
- `dashboard/layouts/sales_performance.py`
- `dashboard/layouts/brand_market.py`
- `dashboard/layouts/engagement.py`
- `dashboard/layouts/deep_dive.py`
- `dashboard/components/filters.py`
- `dashboard/components/charts.py`
- `dashboard/assets/styles.css`

---

## Phase 3: AI System Architecture

### System Architecture

```
Frontend (Dash) → AI API → AI Model → Code + Explanation
                ↓
Frontend (Display & Edit) → Human Approval
                ↓
Execution API → Local Python → Results
                ↓
Logs API (SQLite)
```

### Key Components

**AI API (FastAPI)**
- Endpoint: POST /api/ai/generate
- Input: user_request, context, conversation_history
- Output: code, explanation, request_id

**Execution API (FastAPI)**
- Endpoint: POST /api/execute/run
- Input: code, request_id, data_context
- Output: status, results, logs, execution_time
- Security: whitelist libraries, timeout, sandbox

**Logs API (FastAPI)**
- Endpoint: POST /api/logs/save
- Endpoint: GET /api/logs/history
- Storage: SQLite database

**Frontend AI Assistant Tab**
1. Request Input Section
2. Code Display & Edit Section (syntax highlighting)
3. Approval Section (Approve & Execute button)
4. Results Display Section
5. History Sidebar

### Technologies
- FastAPI for APIs
- OpenAI API / Google Gemini / Ollama
- RestrictedPython for sandboxing
- SQLite for logging

### Files to Create
- `api/main.py`
- `api/routers/ai_router.py`
- `api/routers/execution_router.py`
- `api/routers/logs_router.py`
- `api/services/ai_service.py`
- `api/services/execution_service.py`
- `api/services/logs_service.py`
- `api/utils/code_validator.py`
- `api/utils/sandbox.py`
- `api/database/logs.db`
- `api/database/schema.sql`
- `dashboard/layouts/ai_assistant.py`
- `config/ai_config.yaml`

---

## Phase 4: Implementation Timeline

**Week 1-2: Phase 1 - EDA**
- Data loading and quality assessment
- Deep segment analysis
- Insight generation

**Week 2-3: Phase 2 - Dashboard**
- Layout and visualization implementation
- Interactive features
- Styling

**Week 3-4: Phase 3 - AI APIs**
- AI API implementation
- Execution API with sandbox
- Logs API

**Week 4-5: Phase 3 - Frontend Integration**
- AI assistant tab
- Approval workflow
- Results display

**Week 5-6: Integration & Testing**
- End-to-end testing
- Documentation
- Presentation preparation

---

## Phase 5: Analysis & Insights Preparation

### Key Insights to Develop
1. Price segment dominance and revenue distribution
2. Brand concentration and market structure
3. Review-sales correlation patterns
4. Discount strategy effectiveness
5. Category opportunities and gaps

### Prepared Analysis Questions
1. Average revenue per product in specific price ranges
2. Correlation between review_count and quantity_sold
3. Brand performance analysis (rating vs sales)
4. Discount percentage distribution by category
5. High-potential products identification
6. Video impact on sales
7. Image count vs rating relationship
8. Product launch trends over time

### Presentation Materials
- Executive summary of findings
- Key visualizations
- Demo script for AI module
- Backup slides with detailed analysis

---

## Project Structure

```
D:\_HCMUS\4th_year\TQHDL\final\
├── dataset/                          # Original CSV files
├── data/
│   ├── processed/                    # Cleaned data
│   └── temp/                         # Execution results
├── notebooks/                        # EDA notebooks
├── dashboard/                        # Dashboard app
│   ├── layouts/
│   ├── components/
│   └── assets/
├── api/                              # FastAPI backend
│   ├── routers/
│   ├── services/
│   ├── utils/
│   └── database/
├── config/                           # Configuration
├── docs/                             # Documentation
├── presentation/                     # Presentation materials
├── tests/                            # Tests
├── requirements.txt
└── README.md
```

---

## Success Criteria

1. **Data Analysis**: Minimum 5 meaningful insights with data evidence
2. **Visualizations**: All 7 criteria met (purpose-appropriate, clear, integrated, interactive, attractive, trends, conclusions)
3. **AI Integration**: Complete workflow (request → code → approval → execution → results → logging)
4. **Presentation**: AI module successfully answers prepared questions
5. **Code Quality**: Clean, documented, testable
6. **Documentation**: Complete user guide and API docs
