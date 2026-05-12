from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

_CHART_PAPER = "#f8fafc"
_CHART_PLOT = "#e2e8f0"
_GRID = "#cbd5e1"
_BAR_PRIMARY = "#0369a1"
_BAR_COUNT = "#64748b"


def _style_fig(fig: go.Figure, *, height: int = 400) -> go.Figure:
    fig.update_layout(
        paper_bgcolor=_CHART_PAPER,
        plot_bgcolor=_CHART_PLOT,
        font=dict(color="#0f172a", family="system-ui, sans-serif"),
        height=height,
        margin=dict(l=48, r=24, t=56, b=48),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor=_GRID, zeroline=True, zerolinecolor="#94a3b8")
    return fig


def _feature_impact_two_panel(stats: pd.DataFrame, x_col: str, title_top: str) -> go.Figure:
    """
    Q11/Q12: Không gộp avg_sold (vài–vài chục) với count (nghìn) trên một trục — hai panel, mỗi panel một thang Y.
    """
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.14,
        row_heights=[0.52, 0.48],
        subplot_titles=(
            title_top,
            "Số SKU trong nhóm (catalog)",
        ),
    )
    fig.add_trace(
        go.Bar(
            x=stats[x_col],
            y=stats["avg_sold"],
            name="Lượng bán TB",
            marker_color=_BAR_PRIMARY,
            text=stats["avg_sold"].round(1),
            texttemplate="%{text}",
            textposition="outside",
            hovertemplate="%{x}<br>Lượng bán TB: %{y:.2f} đơn<extra></extra>",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=stats[x_col],
            y=stats["count"],
            name="Số SKU",
            marker_color=_BAR_COUNT,
            text=stats["count"].astype(int),
            texttemplate="%{text:,}",
            textposition="outside",
            hovertemplate="%{x}<br>SKU: %{y:,}<extra></extra>",
        ),
        row=2,
        col=1,
    )
    fig.update_yaxes(title_text="Đơn TB / SKU", row=1, col=1)
    fig.update_yaxes(title_text="Số SKU", row=2, col=1)
    fig.update_xaxes(title_text="", row=2, col=1)
    _style_fig(fig, height=440)
    fig.update_layout(showlegend=False)
    return fig


def create_features_layout(df):
    # --- Q11: Video (has_video)
    video_stats = (
        df.groupby("has_video")
        .agg(
            avg_sold=("quantity_sold", "mean"),
            avg_revenue=("revenue_estimate", "mean"),
            count=("id", "count"),
        )
        .reset_index()
    )
    video_stats.columns = ["has_video", "avg_sold", "avg_revenue", "count"]
    video_stats["has_video"] = video_stats["has_video"].map(
        {True: "Có video", False: "Không video"}
    )

    # --- Q12: Pay later
    paylater_stats = (
        df.groupby("pay_later")
        .agg(
            avg_sold=("quantity_sold", "mean"),
            avg_revenue=("revenue_estimate", "mean"),
            count=("id", "count"),
        )
        .reset_index()
    )
    paylater_stats.columns = ["pay_later", "avg_sold", "avg_revenue", "count"]
    paylater_stats["pay_later"] = paylater_stats["pay_later"].map(
        {True: "Trả sau", False: "Không trả sau"}
    )

    fig_video = _feature_impact_two_panel(
        video_stats,
        "has_video",
        "Q11 – Video: lượng bán TB / SKU (có video hay không)",
    )
    fig_pay = _feature_impact_two_panel(
        paylater_stats,
        "pay_later",
        "Q12 – Trả sau: lượng bán TB / SKU",
    )

    # --- Q10: Ảnh hưởng number_of_images → rating (gom nhóm, tránh scatter nhiễu + outlier trục X)
    df_rated = df[df["rating_average"] > 0].copy()
    # Khoảng ảnh dễ diễn giải; gom 21+ để tránh vài SKU 50–70 ảnh kéo giãn trục
    img_edges = [-0.001, 5, 10, 15, 20, 10_000]
    img_labels = ["1–5 ảnh", "6–10", "11–15", "16–20", "21+"]
    df_rated["img_bucket"] = pd.cut(
        df_rated["number_of_images"],
        bins=img_edges,
        labels=img_labels,
        right=True,
        include_lowest=True,
    )
    q10_agg = (
        df_rated.groupby("img_bucket", observed=True)
        .agg(
            mean_rating=("rating_average", "mean"),
            median_rating=("rating_average", "median"),
            n=("id", "count"),
        )
        .reset_index()
        .dropna(subset=["img_bucket"])
    )
    q10_agg["img_bucket"] = q10_agg["img_bucket"].astype(str)

    fig_q10 = px.bar(
        q10_agg,
        x="img_bucket",
        y="mean_rating",
        title="Q10 – Rating TB theo số ảnh (gom nhóm, n khi rê chuột)",
        labels={
            "img_bucket": "Nhóm số ảnh",
            "mean_rating": "Rating TB (0–5)",
        },
        text=q10_agg["mean_rating"].round(2),
        color="mean_rating",
        color_continuous_scale=[
            [0.0, "#fff7ed"],
            [0.35, "#fed7aa"],
            [0.65, "#fb923c"],
            [1.0, "#9a3412"],
        ],
    )
    # px.bar không forward customdata trên mọi bản Plotly — gán qua trace
    _n_cd = q10_agg[["n"]].to_numpy()
    fig_q10.update_traces(
        customdata=_n_cd,
        textposition="outside",
        texttemplate="%{text:.2f}",
        textfont_size=11,
        hovertemplate="<b>%{x}</b><br>Rating TB: %{y:.2f}<br>SKU (n): %{customdata[0]:,}<extra></extra>",
    )
    fig_q10.update_layout(
        coloraxis_showscale=True,
        coloraxis_colorbar=dict(
            title=dict(text="Rating TB", side="right"),
            thickness=12,
            len=0.55,
            bgcolor="rgba(255,255,255,0.9)",
        ),
        yaxis=dict(range=[0, 5.25]),
    )
    _style_fig(fig_q10, height=400)
    fig_q10.update_layout(margin=dict(r=72))

    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Phân tích tính năng sản phẩm"),
                            html.P(
                                "Q10–Q12: video, pay later, số ảnh — trình bày theo thang riêng hoặc gom nhóm để tránh nhiễu.",
                                className="text-muted",
                            ),
                        ]
                    )
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H4(
                                                f"{df['has_video'].sum():,}",
                                                className="text-info",
                                            ),
                                            html.P("SKU có video", className="mb-0"),
                                            html.Small(
                                                f"{df['has_video'].sum()/len(df)*100:.1f}% catalog",
                                                className="text-muted",
                                            ),
                                        ]
                                    )
                                ],
                                className="h-100",
                            )
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H4(
                                                f"{df['number_of_images'].mean():.1f}",
                                                className="text-warning",
                                            ),
                                            html.P("Ảnh TB / SKU", className="mb-0"),
                                            html.Small(
                                                f"Min–max: {df['number_of_images'].min()}–{df['number_of_images'].max()}",
                                                className="text-muted",
                                            ),
                                        ]
                                    )
                                ],
                                className="h-100",
                            )
                        ],
                        width=4,
                    ),
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H4(
                                                f"{df['pay_later'].sum():,}",
                                                className="text-success",
                                            ),
                                            html.P("SKU hỗ trợ trả sau", className="mb-0"),
                                            html.Small(
                                                f"{df['pay_later'].sum()/len(df)*100:.1f}% catalog",
                                                className="text-muted",
                                            ),
                                        ]
                                    )
                                ],
                                className="h-100",
                            )
                        ],
                        width=4,
                    ),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col([dcc.Graph(figure=fig_video)], width=6),
                    dbc.Col([dcc.Graph(figure=fig_pay)], width=6),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5(
                                "Q10 – Ảnh hưởng số lượng ảnh đến rating",
                                className="text-secondary mb-2",
                            ),
                            html.P(
                                "Biểu đồ phân tán thô + outlier số ảnh dễ nhiễu. Thay bằng "
                                "**rating TB theo bucket số ảnh** (kèm n trong nhãn) — đúng câu hỏi “ảnh có liên quan rating không”, "
                                "theo hướng gom nhóm (book.md: aggregation để thấy pattern).",
                                className="text-muted small",
                            ),
                        ]
                    )
                ]
            ),
            dbc.Row([dbc.Col([dcc.Graph(figure=fig_q10)], width=12)]),
        ],
        fluid=True,
    )
