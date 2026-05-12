from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

_OEM_BAR = "#c2410c"
_BRANDED_BAR = "#0369a1"


def _build_q7_oem_branded_figure(comparison: pd.DataFrame) -> go.Figure:
    """Q7: Không gộp SKU + giá + sales trên một trục Y (thang lệch → vô nghĩa)"""
    xcat = ["OEM", "Branded"]
    y_products = [comparison.loc[0, "Products"], comparison.loc[1, "Products"]]
    y_price_k = [comparison.loc[0, "Avg Price"] / 1000, comparison.loc[1, "Avg Price"] / 1000]
    y_sales = [comparison.loc[0, "Avg Sales"], comparison.loc[1, "Avg Sales"]]

    fig = make_subplots(
        rows=1,
        cols=3,
        subplot_titles=(
            "Số SKU trong catalog",
            "Giá TB (nghìn VND)",
            "Doanh số TB / SKU (đơn)",
        ),
        horizontal_spacing=0.07,
    )

    colors = [_OEM_BAR, _BRANDED_BAR]

    fig.add_trace(
        go.Bar(
            x=xcat,
            y=y_products,
            marker_color=colors,
            text=[f"{y_products[0]:,}", f"{y_products[1]:,}"],
            textposition="outside",
            textfont_size=11,
            hovertemplate="%{x}<br>%{y:,} SKU<extra></extra>",
            showlegend=False,
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=xcat,
            y=y_price_k,
            marker_color=colors,
            text=[f"{y_price_k[0]:.0f}k", f"{y_price_k[1]:.0f}k"],
            textposition="outside",
            textfont_size=11,
            hovertemplate="%{x}<br>%{y:.1f}k VND<extra></extra>",
            showlegend=False,
        ),
        row=1,
        col=2,
    )
    fig.add_trace(
        go.Bar(
            x=xcat,
            y=y_sales,
            marker_color=colors,
            text=[f"{y_sales[0]:.1f}", f"{y_sales[1]:.1f}"],
            textposition="outside",
            textfont_size=11,
            hovertemplate="%{x}<br>%{y:.1f} đơn / SKU<extra></extra>",
            showlegend=False,
        ),
        row=1,
        col=3,
    )

    fig.update_layout(
        title="Q7 – OEM so với thương hiệu",
        barmode="group",
        height=400,
        paper_bgcolor="#f8fafc",
        plot_bgcolor="#e2e8f0",
        font=dict(color="#0f172a", family="system-ui, sans-serif"),
        margin=dict(l=40, r=24, t=72, b=72),
    )
    for i in range(1, 4):
        fig.update_xaxes(row=1, col=i, tickfont_size=11)
        fig.update_yaxes(
            row=1,
            col=i,
            showgrid=True,
            gridcolor="#cbd5e1",
            zeroline=True,
            zerolinecolor="#94a3b8",
        )

    # Chú thích màu (không cần legend 6 trace)
    fig.add_annotation(
        xref="paper",
        yref="paper",
        x=0,
        y=-0.12,
        xanchor="left",
        showarrow=False,
        text=(
            f"<span style='color:{_OEM_BAR};font-weight:700'>■</span> OEM &nbsp; "
            f"<span style='color:{_BRANDED_BAR};font-weight:700'>■</span> Có thương hiệu"
        ),
        font=dict(size=12),
    )
    return fig


def create_brand_layout(df):
    # Top brands by revenue
    top_brands = df.groupby('brand').agg({
        'revenue_estimate': 'sum',
        'quantity_sold': 'sum',
        'id': 'count',
        'price': 'mean'
    }).nlargest(10, 'revenue_estimate').reset_index()
    top_brands.columns = ['brand', 'revenue', 'sold', 'products', 'avg_price']

    # OEM vs Branded comparison
    oem_df = df[df['brand'] == 'OEM']
    branded_df = df[df['brand'] != 'OEM']

    comparison = pd.DataFrame({
        'Type': ['OEM', 'Branded'],
        'Products': [len(oem_df), len(branded_df)],
        'Avg Price': [oem_df['price'].mean(), branded_df['price'].mean()],
        'Total Revenue': [oem_df['revenue_estimate'].sum(), branded_df['revenue_estimate'].sum()],
        'Avg Sales': [oem_df['quantity_sold'].mean(), branded_df['quantity_sold'].mean()]
    })

    # Brand concentration
    brand_revenue = df.groupby('brand')['revenue_estimate'].sum().sort_values(ascending=False)
    top_10_share = (brand_revenue.head(10).sum() / brand_revenue.sum() * 100)

    # Q8: Brand with highest avg rating (min 50 products), sorted horizontal bar
    brand_rating = df.groupby('brand').agg(
        avg_rating=('rating_average', 'mean'),
        product_count=('id', 'count')
    ).reset_index()
    brand_rating_50 = brand_rating[brand_rating['product_count'] >= 50].copy()
    brand_rating_50 = brand_rating_50[brand_rating_50['avg_rating'] > 0]
    top_rated_brands = brand_rating_50.nlargest(15, 'avg_rating').sort_values('avg_rating', ascending=True)

    # Q9: Price positioning of top 10 brands (min/avg/max price per brand)
    top10_brand_names = top_brands['brand'].tolist()
    price_pos = df[df['brand'].isin(top10_brand_names)].groupby('brand').agg(
        price_min=('price', 'min'),
        price_avg=('price', 'mean'),
        price_max=('price', 'max')
    ).reset_index().sort_values('price_avg', ascending=True)

    # Build dot plot for price positioning using go.Scatter
    price_pos_fig = go.Figure()
    for _, row in price_pos.iterrows():
        price_pos_fig.add_trace(go.Scatter(
            x=[row['price_min'] / 1000, row['price_avg'] / 1000, row['price_max'] / 1000],
            y=[row['brand']] * 3,
            mode='markers+lines',
            name=row['brand'],
            marker=dict(size=[8, 14, 8], symbol=['circle', 'diamond', 'circle']),
            line=dict(width=2),
            hovertemplate=(
                f"<b>{row['brand']}</b><br>"
                "Giá: %{x:.0f}k VND<br><extra></extra>"
            )
        ))
    price_pos_fig.update_layout(
        title="Q9 – Vị thế giá top 10 thương hiệu (tối thiểu ● TB ◆ tối đa, nghìn VND)",
        xaxis_title="Giá (nghìn VND)",
        yaxis_title='',
        showlegend=False,
        height=420
    )

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Thương hiệu & cấu trúc thị trường"),
                html.P(
                    f"Nhận định: OEM chiếm phần lớn catalog; giá TB thương hiệu thường cao hơn OEM. "
                    f"Top 10 thương hiệu gom khoảng {top_10_share:.1f}% doanh thu ước tính.",
                    className="text-muted",
                ),
            ])
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{len(oem_df):,}", className="text-secondary"),
                        html.P("Sản phẩm OEM", className="mb-0"),
                        html.Small(f"{len(oem_df)/len(df)*100:.1f}% catalog", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{len(branded_df):,}", className="text-primary"),
                        html.P("Sản phẩm có thương hiệu", className="mb-0"),
                        html.Small(f"{len(branded_df)/len(df)*100:.1f}% catalog", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4(f"{branded_df['price'].mean()/oem_df['price'].mean():.1f}x", className="text-success"),
                        html.P("Chênh giá (lần)", className="mb-0"),
                        html.Small("Thương hiệu so với OEM", className="text-muted")
                    ])
                ], className="h-100")
            ], width=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        top_brands,
                        y='brand',
                        x='revenue',
                        orientation='h',
                        title="Top 10 thương hiệu theo doanh thu",
                        labels={"brand": "", "revenue": "Doanh thu (VNĐ)"},
                        color='revenue',
                        color_continuous_scale='Teal'
                    ).update_layout(showlegend=False, height=400)
                )
            ], width=6),
            dbc.Col([
                dcc.Graph(figure=_build_q7_oem_branded_figure(comparison))
            ], width=6),
        ], className="mb-4"),

        # Q8: Brand avg rating (min 50 products) — horizontal sorted bar
        dbc.Row([
            dbc.Col([
                html.H5("Q8 – Thương hiệu có Rating trung bình cao nhất (≥ 50 sản phẩm)",
                        className="text-secondary mb-2"),
                html.P(
                    "Chỉ thương hiệu ≥ 50 sản phẩm và có rating. Thanh ngang đã sắp — dễ so sánh cao/thấp.",
                    className="text-muted small",
                ),
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    figure=px.bar(
                        top_rated_brands,
                        x='avg_rating',
                        y='brand',
                        orientation='h',
                        title="Q8 – Top 15 thương hiệu theo rating TB (≥ 50 SP)",
                        labels={"avg_rating": "Rating TB (0–5)", "brand": ""},
                        color='avg_rating',
                        color_continuous_scale='RdYlGn',
                        text='avg_rating',
                        hover_data={'product_count': True}
                    ).update_traces(
                        texttemplate='%{text:.2f}',
                        textposition='outside'
                    ).update_layout(
                        showlegend=False,
                        height=450,
                        xaxis=dict(range=[0, 5.5])
                    )
                )
            ], width=6),

            # Q9: Price positioning dot plot
            dbc.Col([
                dcc.Graph(figure=price_pos_fig)
            ], width=6),
        ], className="mb-4"),

        # dbc.Row([
        #     dbc.Col([
        #         dcc.Graph(
        #             figure=px.scatter(
        #                 top_brands,
        #                 x='products',
        #                 y='revenue',
        #                 size='sold',
        #                 color='brand',
        #                 text='brand',
        #                 title="Top Brands: Product Count vs Revenue (bubble size = units sold)",
        #                 labels={'products': 'Product Count', 'revenue': 'Revenue (VND)'}
        #             ).update_traces(textposition='top center', textfont_size=9)
        #         )
        #     ], width=12),
        # ])
    ], fluid=True)
