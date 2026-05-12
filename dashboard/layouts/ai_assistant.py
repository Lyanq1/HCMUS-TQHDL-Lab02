"""AI Assistant tab: Gemini code generation, human edit/approve, local execution via FastAPI."""

from __future__ import annotations

import os

import dash_bootstrap_components as dbc
from dash import dcc, html

API_HINT = os.environ.get("DASH_API_BASE", "http://127.0.0.1:8000")


def create_ai_layout(df):
    del df  # DataFrame loaded in app for other tabs; execution uses API-side CSV.
    return dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Trợ lý AI"),
                            html.P(
                                "Luồng: gửi yêu cầu → AI sinh code + giải thích (chờ duyệt) → bạn chỉnh sửa → "
                                "Phê duyệt & chạy trên máy (API sandbox). Không chạy code cho đến khi bạn bấm nút.",
                                className="text-muted",
                            ),
                            # html.Small(
                            #     f"Backend API: {API_HINT} — chạy `python run_api.py` trước khi dùng tab này.",
                            #     className="text-secondary",
                            # ),
                        ]
                    )
                ],
                className="mb-3",
            ),
            dcc.Store(id="ai-request-id-store", data=None),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Label("Yêu cầu phân tích / câu hỏi"),
                            dbc.Textarea(
                                id="ai-user-request",
                                placeholder="Ví dụ: So sánh doanh thu ước tính OEM vs thương hiệu theo danh mục...",
                                rows=4,
                                className="mb-2",
                            ),
                            dbc.ButtonGroup(
                                [
                                    dbc.Button("Gửi cho AI", id="ai-generate-btn", color="primary", n_clicks=0),
                                    dbc.Button(
                                        "Phê duyệt & chạy",
                                        id="ai-run-btn",
                                        color="success",
                                        n_clicks=0,
                                    ),
                                    dbc.Button("Tải lịch sử", id="ai-history-btn", color="secondary", outline=True, n_clicks=0),
                                ],
                                className="mb-3",
                            ),
                            html.Div(id="ai-status", className="mb-2"),
                        ],
                        width=12,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("Giải thích (Markdown)"),
                            dcc.Markdown(id="ai-explanation", className="border rounded p-3 bg-light", children="*(Chưa có kết quả)*"),
                        ],
                        md=6,
                    ),
                    dbc.Col(
                        [
                            html.H5("Mã Python (có thể sửa trước khi chạy)"),
                            dbc.Textarea(
                                id="ai-code",
                                rows=22,
                                className="font-monospace small",
                                spellCheck=False,
                                style={"fontFamily": "ui-monospace, monospace"},
                            ),
                        ],
                        md=6,
                    ),
                ],
                className="mb-3",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("Kết quả thực thi"),
                            html.Div(id="ai-run-output", className="border rounded p-3"),
                        ],
                        width=12,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H5("Lịch sử (theo request_id)"),
                            html.Div(id="ai-history-output", className="small text-muted"),
                        ],
                        width=12,
                    ),
                ]
            ),
        ],
        fluid=True,
    )
