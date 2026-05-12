from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

def create_price_layout(df):
    # Segment analysis
    segment_stats = df.groupby('price_segment').agg({
        'id': 'count',
        'revenue_estimate': 'sum',
        'quantity_sold': ['sum', 'mean'],
        'rating_average': 'mean',
        'discount_pct': 'mean'
    }).reset_index()
    segment_stats.columns = ['segment', 'count', 'revenue', 'total_sold', 'avg_sold', 'avg_rating', 'avg_discount']
    segment_stats['revenue_pct'] = (segment_stats['revenue'] / segment_stats['revenue'].sum() * 100).round(1)
    segment_stats['product_pct'] = (segment_stats['count'] / segment_stats['count'].sum() * 100).round(1)
    # Q3: ROI = revenue / product_count per segment, sorted descending
    segment_stats['roi'] = (segment_stats['revenue'] / segment_stats['count']).round(0)
    segment_stats_roi = segment_stats.sort_values('roi', ascending=False)

    # Price vs performance
    price_perf = df.groupby('price_segment').agg({
        'quantity_sold': 'mean',
        'review_count': 'mean'
    }).reset_index()

    # Q1: Mean revenue for 100-300k segment
    seg_100_300 = df[df["price_segment"] == "100–300k"]
    mean_rev_100_300 = seg_100_300['revenue_estimate'].mean() if len(seg_100_300) > 0 else 0
    total_rev_100_300 = seg_100_300['revenue_estimate'].sum() if len(seg_100_300) > 0 else 0
    product_count_100_300 = len(seg_100_300)

    # Q2: Avg discount % by category, sorted descending
    discount_by_cat = (
        df.groupby('category')['discount_pct']
        .mean()
        .reset_index()
        .rename(columns={'discount_pct': 'avg_discount_pct'})
        .sort_values('avg_discount_pct', ascending=True)
    )

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Phân tích theo khúc giá"),
                html.P(
                    "Nhận định: phân khúc dưới 100k chiếm phần lớn SKU nhưng tỷ trọng doanh thu thấp hơn "
                    "so với khúc giá cao hơn — cần đọc kèm biểu đồ tỷ lệ % sản phẩm / % doanh thu.",
                    className="text-muted",
                ),
            ])
        ], className="mb-4"),

        # Q1: KPI Cards for 100-300k segment
        dbc.Row([
            dbc.Col([
                html.H5("Q1 – Phân khúc 100–300k VND", className="text-secondary mb-3")
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{mean_rev_100_300/1e6:.2f}M", className="text-success"),
                        html.P("Doanh thu TB / sản phẩm", className="mb-0"),
                        html.Small("Phân khúc 100–300k VND", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{total_rev_100_300/1e9:.1f}B", className="text-primary"),
                        html.P("Tổng doanh thu", className="mb-0"),
                        html.Small("Phân khúc 100–300k VND", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{product_count_100_300:,}", className="text-info"),
                        html.P("Số sản phẩm", className="mb-0"),
                        html.Small("Phân khúc 100–300k VND (điểm ngọt)", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=go.Figure(data=[
                        go.Bar(name="% sản phẩm", x=segment_stats['segment'], y=segment_stats['product_pct'], marker_color='lightblue'),
                        go.Bar(name="% doanh thu", x=segment_stats['segment'], y=segment_stats['revenue_pct'], marker_color='lightgreen')
                    ]).update_layout(
                        title="Phân bố % sản phẩm và % doanh thu theo khúc giá",
                        barmode='group',
                        xaxis_title='Khúc giá',
                        yaxis_title='Tỷ lệ (%)',
                    )
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        segment_stats,
                        x='segment',
                        y='avg_sold',
                        title="Lượng bán trung bình / sản phẩm theo khúc giá",
                        labels={"segment": "Khúc giá", "avg_sold": "Đơn TB / SP"},
                        color='avg_sold',
                        color_continuous_scale='Reds'
                    ).update_layout(showlegend=False)
                )
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.scatter(
                        df.sample(min(5000, len(df))),
                        x='price',
                        y='quantity_sold',
                        color='price_segment',
                        title="Giá và khối lượng bán (mẫu ngẫu nhiên)",
                        labels={"price": "Giá (VNĐ)", "quantity_sold": "Số lượng đã bán"},
                        log_x=True,
                        log_y=True
                    )
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        price_perf,
                        x='price_segment',
                        y='review_count',
                        title="Số review trung bình theo khúc giá",
                        labels={"price_segment": "Khúc giá", "review_count": "Review TB"},
                        color='review_count',
                        color_continuous_scale='Purples'
                    ).update_layout(showlegend=False)
                )
            ], width=6),
        ], className="mb-4"),

        # Q2: Discount by category (horizontal bar — tên category dài, book.md: "horizontal when labels are long")
        dbc.Row([
            dbc.Col([
                html.H5("Q2 – Tỷ lệ Discount theo Danh mục", className="text-secondary mb-2")
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        discount_by_cat,
                        x='avg_discount_pct',
                        y='category',
                        orientation='h',
                        title="Giảm giá TB (%) theo danh mục (đã sắp xếp)",
                        labels={"avg_discount_pct": "Giảm giá TB (%)", "category": ""},
                        color='avg_discount_pct',
                        color_continuous_scale='Oranges',
                        text='avg_discount_pct'
                    ).update_traces(
                        texttemplate='%{text:.1f}%',
                        textposition='outside'
                    ).update_layout(showlegend=False, height=350)
                )
            ], width=6),

            # Q3: ROI by segment — sorted bar (book.md: sorted bar to spot highest ROI instantly)
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        segment_stats_roi,
                        x='segment',
                        y='roi',
                        title="Q3 – ROI theo khúc giá (doanh thu / số SP, đã sắp xếp)",
                        labels={"segment": "Khúc giá", "roi": "ROI (VNĐ / SP)"},
                        color='roi',
                        color_continuous_scale='Greens',
                        text='roi'
                    ).update_traces(
                        texttemplate='%{text:,.0f}',
                        textposition='outside'
                    ).update_layout(showlegend=False, height=350)
                )
            ], width=6),
        ]),
    ], fluid=True)
