from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_engagement_layout(df):
    # Review impact analysis
    review_bins = [0, 10, 50, 100, 500, float('inf')]
    review_labels = ['0-10', '10-50', '50-100', '100-500', '>500']
    df_copy = df.copy()
    df_copy['review_range'] = pd.cut(df_copy['review_count'], bins=review_bins, labels=review_labels)

    review_impact = df_copy.groupby('review_range').agg({
        'quantity_sold': 'mean',
        'revenue_estimate': 'mean',
        'rating_average': 'mean',
        'id': 'count'
    }).reset_index()
    review_impact.columns = ['review_range', 'avg_sold', 'avg_revenue', 'avg_rating', 'product_count']
    review_impact['review_range'] = review_impact['review_range'].astype(str)

    # Engagement metrics
    high_engagement = df[df['review_count'] >= 50]
    low_engagement = df[df['review_count'] < 10]

    # Rating distribution
    rated_df = df[df['rating_average'] > 0]
    rating_dist = rated_df.groupby(pd.cut(rated_df['rating_average'],
                                          bins=[0, 2, 3, 4, 4.5, 5],
                                          labels=['0–2★', '2–3★', '3–4★', '4–4,5★', '4,5–5★'])).size().reset_index()
    rating_dist.columns = ['rating_range', 'count']
    rating_dist['rating_range'] = rating_dist['rating_range'].astype(str)

    # Q4: Scatter with r=0.621 annotation + manual trendline (log-space via numpy polyfit)
    scatter_df = df[df['review_count'] > 0].copy()
    scatter_sample = scatter_df.sample(min(3000, len(scatter_df)))
    r_value = scatter_df['review_count'].corr(scatter_df['quantity_sold'])

    scatter_fig = px.scatter(
        scatter_sample,
        x='review_count',
        y='quantity_sold',
        color='rating_average',
        title="Q4 – Review và bán hàng (r = {:.3f}, màu = rating)".format(r_value),
        labels={
            "review_count": "Số review",
            "quantity_sold": "Số lượng đã bán",
            "rating_average": "Điểm rating",
        },
        log_x=True,
        log_y=True
    )
    # Add manual trendline in log-log space using numpy
    valid = scatter_df[(scatter_df['review_count'] > 0) & (scatter_df['quantity_sold'] > 0)]
    log_x = np.log10(valid['review_count'])
    log_y = np.log10(valid['quantity_sold'])
    coeffs = np.polyfit(log_x, log_y, 1)
    x_range = np.logspace(np.log10(valid['review_count'].min()), np.log10(valid['review_count'].max()), 100)
    y_trend = 10 ** (coeffs[0] * np.log10(x_range) + coeffs[1])
    scatter_fig.add_trace(go.Scatter(
        x=x_range, y=y_trend,
        mode='lines',
        line=dict(color='red', width=2, dash='dash'),
        name="Xu hướng (OLS log–log)",
        showlegend=True
    ))
    scatter_fig.add_annotation(
        x=0.02, y=0.97,
        xref='paper', yref='paper',
        text=f"<b>Pearson r = {r_value:.3f}</b><br>Tương quan dương mạnh",
        showarrow=False,
        font=dict(size=13, color='crimson'),
        align='left',
        bgcolor='rgba(255,255,255,0.85)',
        bordercolor='crimson',
        borderwidth=1
    )

    # Q6: Conversion rate — avg sales / (review_count + 1) as proxy, per review tier
    review_impact['conv_rate'] = (review_impact['avg_sold'] / review_impact['review_range'].map(
        {'0-10': 5, '10-50': 30, '50-100': 75, '100-500': 300, '>500': 750}
    )).round(2)

    sales_multiplier = (
        high_engagement['quantity_sold'].mean() / low_engagement['quantity_sold'].mean()
        if low_engagement['quantity_sold'].mean() > 0 else 0
    )

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Tương tác khách hàng"),
                html.P(
                    "SKU có nhiều review thường bán tốt hơn — hệ số tương quan Pearson (review → bán) cao cho thấy "
                    "đánh giá đi kèm nhu cầu mua.",
                    className="text-muted",
                ),
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{len(high_engagement):,}", className="text-success"),
                        html.P("Tương tác cao", className="mb-0"),
                        html.Small("≥ 50 review", className="text-muted")
                    ])
                ], className="h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{len(low_engagement):,}", className="text-warning"),
                        html.P("Tương tác thấp", className="mb-0"),
                        html.Small("< 10 review", className="text-muted")
                    ])
                ], className="h-100")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{sales_multiplier:.1f}x", className="text-info"),
                        html.P("Bội số bán (cao / thấp)", className="mb-0"),
                        html.Small("TB bán: cao vs thấp tương tác", className="text-muted")
                    ])
                ], className="h-100")
            ], width=3),
            # Q6: Conversion rate KPI
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{r_value:.3f}", className="text-danger"),
                        html.P("Pearson r (review → bán)", className="mb-0"),
                        html.Small("Q4 – tương quan dương", className="text-muted")
                    ])
                ], className="h-100")
            ], width=3),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        review_impact,
                        x='review_range',
                        y='avg_sold',
                        title="Ảnh hưởng khoảng review đến lượng bán TB",
                        labels={"review_range": "Khoảng số review", "avg_sold": "Đơn TB"},
                        color='avg_sold',
                        color_continuous_scale='YlOrRd',
                        text='avg_sold'
                    ).update_traces(texttemplate='%{text:.1f}', textposition='outside').update_layout(showlegend=False)
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        rating_dist,
                        x='rating_range',
                        y='count',
                        title="Phân bố rating (SKU có rating)",
                        labels={"rating_range": "Khoảng rating", "count": "Số SKU"},
                        color='count',
                        color_continuous_scale='Greens'
                    ).update_layout(showlegend=False)
                )
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(figure=scatter_fig)
            ], width=6),
            dbc.Col([
                # Q6: Estimated conversion rate (avg_sold / avg_review_count proxy) per tier
                dcc.Graph(
                    figure=px.bar(
                        review_impact,
                        x='review_range',
                        y='conv_rate',
                        title="Q6 – Tỷ lệ chuyển đổi ước tính theo bậc review (đơn TB / điểm giữa khoảng)",
                        labels={
                            "review_range": "Khoảng review",
                            "conv_rate": "Đơn / review (proxy)",
                        },
                        color='conv_rate',
                        color_continuous_scale='Teal',
                        text='conv_rate'
                    ).update_traces(
                        texttemplate='%{text:.2f}',
                        textposition='outside'
                    ).update_layout(showlegend=False)
                )
            ], width=6),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        review_impact,
                        x='review_range',
                        y='product_count',
                        title="Phân bố SKU theo khoảng số review",
                        labels={"review_range": "Khoảng review", "product_count": "Số SKU"},
                        color='product_count',
                        color_continuous_scale='Blues'
                    ).update_layout(showlegend=False)
                )
            ], width=6),
        ])
    ], fluid=True)
