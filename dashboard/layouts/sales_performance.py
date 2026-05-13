from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# --- Màu theo hướng The Big Book of Dashboards (Ch.1): purposeful, sequential/categorical gọn,
# tránh “cầu vồng” trang trí; ưu tiên length/position; sequential = một hue (xanh lam / xanh ngọc).
# Tránh đỏ–xanh lá (traffic light); dùng tông lạnh (blue / teal) dễ đọc.

# Sequential: đậm = giá trị lớn hơn. Sàn màu phải đủ tối so với plot_bg (#e2e8f0) — tránh #cbd5e1/#93c5fd
# (thanh nhỏ trông như “trắng”, chìm nền).
_SEQ_BLUE = [
    [0.0, "#64748b"],
    [0.28, "#4f6fae"],
    [0.55, "#2563eb"],
    [0.82, "#1e40af"],
    [1.0, "#000080"],
]

# Teal–xanh lá: dùng cho biểu đồ phân bổ SKU
_SEQ_TEAL = [
    [0.0, "#99f6e4"],
    [0.25, "#2dd4bf"],
    [0.55, "#0d9488"],
    [0.80, "#0f766e"],
    [1.0, "#134e4a"],
]

# Cam–hổ phách: dùng cho biểu đồ tổng lượng bán theo danh mục
_SEQ_AMBER = [
    [0.0, "#fde68a"],
    [0.25, "#fbbf24"],
    [0.55, "#d97706"],
    [0.80, "#b45309"],
    [1.0, "#78350f"],
]

# Một màu cho ranking (độ dài thanh là encoding chính — book.md: length mạnh nhất).
_FILL_VOLUME = "#1e40af"
_FILL_REVENUE = "#0f766e"

_SALES_GRAPH_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "scrollZoom": True,
    "toImageButtonOptions": {"format": "png", "filename": "bieu_do_ban_hang"},
    "modeBarButtonsToAdd": ["select2d", "lasso2d"],
}

_CHART_PAPER = "#f8fafc"
_CHART_PLOT = "#e2e8f0"
_GRID = "#cbd5e1"


def _style_sales_figure(
    fig: go.Figure,
    *,
    show_legend: bool = False,
    margin_bottom: int = 8,
    margin_right: int = 8,
) -> go.Figure:
    """Nền trung tính, lưới nhẹ; hover rõ; legend chỉ khi cần (book.md: không dùng màu thừa)."""
    fig.update_traces(
        marker_line_width=1,
        marker_line_color="rgba(15, 23, 42, 0.25)",
        hoverlabel=dict(
            bgcolor="#0f172a",
            font_size=13,
            font_family="system-ui, sans-serif",
            font_color="#f8fafc",
        ),
    )
    fig.update_layout(
        paper_bgcolor=_CHART_PAPER,
        plot_bgcolor=_CHART_PLOT,
        font=dict(color="#0f172a", family="system-ui, sans-serif"),
        title_font_size=15,
        margin=dict(l=8, r=margin_right, t=48, b=margin_bottom),
        xaxis=dict(
            showgrid=True,
            gridcolor=_GRID,
            gridwidth=0.6,
            zeroline=True,
            zerolinecolor="#94a3b8",
            zerolinewidth=1,
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=_GRID,
            gridwidth=0.6,
            zeroline=True,
            zerolinecolor="#94a3b8",
            zerolinewidth=1,
        ),
        hovermode="closest",
        showlegend=show_legend,
        legend=dict(
            bgcolor="rgba(255,255,255,0.9)",
            bordercolor="#e2e8f0",
            borderwidth=1,
            font=dict(size=11),
        ),
        transition=dict(duration=250, easing="cubic-in-out"),
    )
    return fig


def _colorbar(title: str) -> dict:
    return dict(
        title=dict(text=title, side="right", font=dict(size=11)),
        thickness=12,
        len=0.55,
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor="#e2e8f0",
        borderwidth=1,
        outlinewidth=0,
    )


def create_sales_layout(df):
    top_products = df.nlargest(20, "quantity_sold").copy()
    top_products["short_name"] = top_products["name"].str[:40] + "..."

    top_revenue = df.nlargest(10, "revenue_estimate").copy()
    top_revenue["short_name"] = top_revenue["name"].str[:30] + "..."

    sales_bins = [0, 10, 50, 100, 500, float("inf")]
    sales_labels = ["0-10", "10-50", "50-100", "100-500", ">500"]
    df_copy = df.copy()
    df_copy["sales_range"] = pd.cut(
        df_copy["quantity_sold"], bins=sales_bins, labels=sales_labels
    )
    sales_dist = df_copy["sales_range"].value_counts().sort_index()
    sales_df = sales_dist.reset_index()
    sales_df.columns = ["sales_range", "product_count"]

    cat_perf = (
        df.groupby("category")
        .agg({"quantity_sold": "sum", "revenue_estimate": "sum"})
        .reset_index()
    )

    # Q5: reviews cao / sales thấp — loại SKU quantity_sold = 0 (nhiễu: score = review_count/(0+1) = review_count).
    df_potential = df[(df["review_count"] >= 20) & (df["quantity_sold"] > 0)].copy()
    df_potential["potential_score"] = df_potential["review_count"] / (
        df_potential["quantity_sold"] + 1
    )
    top_potential = df_potential.nlargest(10, "potential_score").copy()
    top_potential["short_name"] = top_potential["name"].str[:35] + "..."

    # Top 10 volume: một màu — so sánh bằng độ dài thanh (book.md).
    tp10_vol = top_products.head(10).sort_values("quantity_sold", ascending=True)
    fig_vol = px.bar(
        tp10_vol,
        y="short_name",
        x="quantity_sold",
        orientation="h",
        title="Top 10 bán chạy theo số lượng",
        labels={"short_name": "", "quantity_sold": "Đơn đã bán"},
        text="quantity_sold",
    )
    fig_vol.update_traces(
        marker_color=_FILL_VOLUME,
        textposition="outside",
        texttemplate="%{text:,}",
        textfont_size=11,
        textfont_color="#0f172a",
    )
    fig_vol.update_layout(height=400)
    _style_sales_figure(fig_vol)

    tp10_rev = top_revenue.sort_values("revenue_estimate", ascending=True)
    fig_rev = px.bar(
        tp10_rev,
        y="short_name",
        x="revenue_estimate",
        orientation="h",
        title="Top 10 sản phẩm theo doanh thu ước tính",
        labels={"short_name": "", "revenue_estimate": "Doanh thu (VNĐ)"},
        text="revenue_estimate",
    )
    fig_rev.update_traces(
        marker_color=_FILL_REVENUE,
        textposition="outside",
        texttemplate="%{text:.3s}",
        textfont_size=11,
        textfont_color="#0f172a",
    )
    fig_rev.update_layout(height=400)
    _style_sales_figure(fig_rev)

    # Phân bố: ordinal → sequential một hue theo số sản phẩm (categorical vừa đủ, book.md Fig 1.20).
    fig_dist = px.bar(
        sales_df,
        x="sales_range",
        y="product_count",
        color="product_count",
        color_continuous_scale=_SEQ_TEAL,
        title="Phân bố SKU theo mức bán (số lượng)",
        labels={"sales_range": "Khoảng đã bán", "product_count": "Số SKU", "color": "Số SP"},
        category_orders={"sales_range": sales_labels},
        text="product_count",
    )
    fig_dist.update_traces(
        textposition="outside",
        texttemplate="%{text:,}",
        textfont_size=11,
        textfont_color="#0f172a",
    )
    fig_dist.update_layout(
        coloraxis_showscale=True,
        coloraxis_colorbar=_colorbar("Số sản phẩm"),
    )
    _style_sales_figure(fig_dist, margin_right=72, margin_bottom=16)

    # Category: sequential theo tổng bán — một biến, một gradient (tránh nhiều màu không cần thiết).
    fig_cat = px.bar(
        cat_perf,
        x="category",
        y="quantity_sold",
        color="quantity_sold",
        color_continuous_scale=_SEQ_AMBER,
        title="Tổng lượng bán theo danh mục",
        labels={"category": "Danh mục", "quantity_sold": "Tổng đơn", "color": "Đơn"},
        text="quantity_sold",
    )
    fig_cat.update_traces(
        textposition="outside",
        texttemplate="%{text:,}",
        textfont_size=11,
        textfont_color="#0f172a",
    )
    fig_cat.update_layout(
        coloraxis_showscale=True,
        coloraxis_colorbar=_colorbar("Tổng đơn"),
    )
    fig_cat.update_xaxes(tickangle=-35)
    _style_sales_figure(fig_cat, margin_right=72, margin_bottom=56)

    tp_sorted = top_potential.sort_values("potential_score", ascending=True)
    # Sequential theo score: mỗi thanh khác sắc độ, dễ tách nền hơn một màu chàm đặc (book.md: sequential = một biến).
    fig_q5 = px.bar(
        tp_sorted,
        x="potential_score",
        y="short_name",
        orientation="h",
        color="potential_score",
        color_continuous_scale=_SEQ_BLUE,
        title="Q5 – Top 10 sản phẩm tiềm năng (nhiều review / ít bán)",
        labels={
            "potential_score": "Điểm tiềm năng (review / bán)",
            "short_name": "",
            "color": "Điểm",
        },
        hover_data={
            "review_count": True,
            "quantity_sold": True,
            "price": True,
        },
        text="potential_score",
    )
    fig_q5.update_traces(
        textposition="outside",
        texttemplate="%{text:.2f}",
        textfont_size=12,
        textfont_color="#0f172a",
    )
    fig_q5.update_layout(
        height=440,
        coloraxis_showscale=True,
        coloraxis_colorbar=_colorbar("Điểm tiềm năng"),
    )
    _style_sales_figure(fig_q5, margin_right=76)

    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Phân tích hiệu suất bán hàng"),
                            html.P(
                                "Một nhóm SKU rất nhỏ thường gom phần lớn doanh thu — đọc kèm top ranking và phân bố.",
                                className="text-muted",
                            ),
                            html.P(
                                [
  
                                ],
                                className="small text-muted mb-0",
                            ),
                        ]
                    )
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [dcc.Graph(figure=fig_vol, config=_SALES_GRAPH_CONFIG)],
                        width=6,
                    ),
                    dbc.Col(
                        [dcc.Graph(figure=fig_rev, config=_SALES_GRAPH_CONFIG)],
                        width=6,
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [dcc.Graph(figure=fig_dist, config=_SALES_GRAPH_CONFIG)],
                        width=6,
                    ),
                    dbc.Col(
                        [dcc.Graph(figure=fig_cat, config=_SALES_GRAPH_CONFIG)],
                        width=6,
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5(
                                "Q5 – Top 10 Sản phẩm Tiềm năng (reviews cao, sales thấp)",
                                className="text-secondary mb-2",
                            ),
                            html.P(
                                [
                                    "Điểm tiềm năng = review_count / (quantity_sold + 1). ",
                                    html.Strong("Loại SKU có quantity_sold = 0"),
                                    " — tránh nhiễu (điểm trùng review_count, phá thang). ",
                                    "Chỉ xét listing đã có ít nhất một đơn bán.",
                                ],
                                className="text-muted small",
                            ),
                        ]
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [dcc.Graph(figure=fig_q5, config=_SALES_GRAPH_CONFIG)],
                        width=12,
                    ),
                ]
            ),
        ],
        fluid=True,
    )
