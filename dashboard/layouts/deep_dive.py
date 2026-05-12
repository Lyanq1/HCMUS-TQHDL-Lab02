from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# Dataset docs (Dataset_description.md): date_created is **days** between crawl/update and
# listing creation — NOT a Unix timestamp. Parsing as unit='s' collapses everything near 1970.


def _listing_age_days(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def create_deepdive_layout(df):
    categories = df['category'].unique().tolist()

    df_time = df.copy()
    df_time['listing_age_days'] = _listing_age_days(df_time['date_created'])
    valid_age = df_time['listing_age_days'].notna() & (df_time['listing_age_days'] >= 0)
    has_temporal_data = int(valid_age.sum()) > 100

    if has_temporal_data:
        df_dated = df_time.loc[valid_age].copy()

        # Q13: Distribution of catalog by listing age (ordinal axis = age bands).
        # Line chart connects counts across ordered age bands (book.md: line for trends along ordered x).
        # Use a slightly negative left edge so listing_age_days == 0 maps to the first bin (not NaN).
        age_bins = [-0.001, 30, 60, 90, 120, 180, 270, 365, 548, 730, 1095, float('inf')]
        age_labels = [
            '0–30 ngày', '31–60 ngày', '61–90 ngày', '91–120 ngày', '121–180 ngày', '181–270 ngày',
            '271–365 ngày', '1–1,5 năm', '1,5–2 năm', '2–3 năm', '>3 năm',
        ]
        df_dated['age_band'] = pd.cut(
            df_dated['listing_age_days'],
            bins=age_bins,
            labels=age_labels,
            right=True,
        )
        # observed=False keeps every age band on the x-axis (zeros for empty bins) for a proper line shape
        launch_trend = (
            df_dated.groupby('age_band', observed=False)
            .size()
            .reset_index(name='product_count')
        )
        launch_trend['age_band'] = pd.Categorical(
            launch_trend['age_band'], categories=age_labels, ordered=True
        )
        launch_trend = launch_trend.sort_values('age_band')

        line_fig = px.line(
            launch_trend,
            x='age_band',
            y='product_count',
            title='Q13 – Phân bố catalog theo tuổi listing (số ngày từ crawl đến tạo SP, không phải Unix timestamp)',
            labels={
                'age_band': 'Tuổi listing (khoảng ngày tại thời điểm crawl)',
                'product_count': 'Số sản phẩm',
            },
            markers=True,
        )
        line_fig.update_traces(line=dict(width=3), marker=dict(size=8))
        line_fig.update_xaxes(tickangle=-35)
        line_fig.update_layout(height=400)

        # Q14: "Mới ~6 tháng" = listing age ≤ 183 days (dataset has no calendar date)
        new_cutoff_days = 183
        new_products = df_dated[df_dated['listing_age_days'] <= new_cutoff_days]
        new_by_cat = (
            new_products.groupby('category')
            .size()
            .reset_index(name='new_products')
            .sort_values('new_products', ascending=True)
        )
        new_products_count = len(new_products)

        if new_by_cat.empty:
            bar_fig = px.bar(
                pd.DataFrame({'category': ['(không có dữ liệu)'], 'new_products': [0]}),
                x='new_products',
                y='category',
                orientation='h',
                title=f'Q14 – Không có sản phẩm nào với tuổi listing ≤ {new_cutoff_days} ngày',
            )
        else:
            bar_fig = px.bar(
                new_by_cat,
                x='new_products',
                y='category',
                orientation='h',
                title=(
                    f'Q14 – Sản phẩm "mới" (tuổi listing ≤ {new_cutoff_days} ngày ~ 6 tháng), '
                    f'tổng: {new_products_count:,}'
                ),
                labels={'new_products': 'Số sản phẩm', 'category': ''},
                color='new_products',
                color_continuous_scale='Blues',
                text='new_products',
            )
            bar_fig.update_traces(texttemplate='%{text:,}', textposition='outside')
        bar_fig.update_layout(showlegend=False, height=350)

        temporal_section = [
            dbc.Row([
                dbc.Col([
                    html.H5("Q13 – Phân tích thời gian (date_created)", className="text-secondary mb-2"),
                    html.P(
                        "Cột date_created trong bộ dữ liệu TIKI là số ngày (khoảng cách ngày giữa ngày crawl/cập nhật "
                        "và ngày tạo listing), không phải timestamp Unix — vì vậy không thể vẽ theo lịch tháng/năm. "
                        "Thay vào đó: line chart theo các khoảng tuổi listing (trục X có thứ tự), phù hợp Ch.1 "
                        "(đường nối các mức trên trục ordinal).",
                        className="text-muted small",
                    ),
                ]),
            ]),
            dbc.Row([dbc.Col([dcc.Graph(figure=line_fig)], width=12)], className="mb-4"),
            dbc.Row([
                dbc.Col([
                    html.H5("Q14 – Sản phẩm mới theo danh mục (proxy 6 tháng)", className="text-secondary mb-2"),
                    html.P(
                        "Vì không có ngày lịch tuyệt đối, dùng ngưỡng tuổi listing ≤ 183 ngày làm proxy "
                        '"ra mắt trong ~6 tháng" tại thời điểm crawl.',
                        className="text-muted small",
                    ),
                ]),
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(figure=bar_fig)], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H2(f"{new_products_count:,}", className="text-primary"),
                            html.P(f'Sản phẩm listing ≤ {new_cutoff_days} ngày tuổi', className="mb-0"),
                            html.Small(
                                "Proxy cho “mới trong ~6 tháng”; định nghĩa theo Dataset_description.md",
                                className="text-muted",
                            ),
                        ]),
                    ], className="mt-5"),
                ], width=6),
            ], className="mb-4"),
        ]
    else:
        temporal_section = [
            dbc.Row([
                dbc.Col([
                    dbc.Alert(
                        "Không đủ giá trị date_created hợp lệ (số ngày) để vẽ Q13/Q14.",
                        color="warning",
                    ),
                ]),
            ], className="mb-4"),
        ]

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Phân tích chuyên sâu"),
                html.P(
                    "Xu hướng thời gian (Q13/Q14) và khám phá giá–bán theo danh mục.",
                    className="text-muted",
                ),
            ])
        ], className="mb-4"),

        # Q13 & Q14 temporal charts
        *temporal_section,

        html.Hr(),

        # Existing interactive category filter
        dbc.Row([
            dbc.Col([
                html.H5("Danh mục — khám phá giá và lượng bán", className="text-secondary mb-2"),
                html.Label("Chọn danh mục:"),
                dcc.Dropdown(
                    id='category-filter',
                    options=[{'label': cat, 'value': cat} for cat in categories],
                    value=categories[0]
                )
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='deepdive-chart')
            ], width=12),
        ])
    ], fluid=True)
