"""Wire AI Assistant tab to FastAPI (Gemini + execute + logs)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[2] / ".env")
from dash import Input, Output, State, callback, html, no_update
import dash_bootstrap_components as dbc

API_BASE = os.environ.get("DASH_API_BASE", "http://127.0.0.1:8000").rstrip("/")


def register_ai_callbacks(app) -> None:
    @app.callback(
        Output("ai-explanation", "children"),
        Output("ai-code", "value"),
        Output("ai-request-id-store", "data"),
        Output("ai-status", "children"),
        Output("ai-run-output", "children"),
        Input("ai-generate-btn", "n_clicks"),
        State("ai-user-request", "value"),
        prevent_initial_call=True,
    )
    def on_generate(_n_clicks, user_request):
        if not user_request or not str(user_request).strip():
            return (
                no_update,
                no_update,
                no_update,
                dbc.Alert("Nhập yêu cầu trước khi gửi.", color="warning", className="py-2"),
                no_update,
            )
        try:
            r = requests.post(
                f"{API_BASE}/api/ai/generate",
                json={"user_request": str(user_request).strip(), "conversation": None},
                timeout=120,
            )
        except requests.RequestException as e:
            return (
                no_update,
                no_update,
                no_update,
                dbc.Alert(f"Không kết nối được API ({API_BASE}): {e}", color="danger"),
                no_update,
            )

        if r.status_code != 200:
            detail = r.text
            try:
                body = r.json()
                detail = body.get("detail", detail)
            except Exception:
                body = None
            if r.status_code == 429:
                msg = detail
                if isinstance(detail, dict):
                    msg = detail.get("message", str(detail))
                    prov = detail.get("provider_detail")
                    if prov:
                        msg = html.Div(
                            [
                                html.P(str(msg)),
                                html.P("Chi tiết từ Google (rút gọn):", className="small text-muted mb-1"),
                                html.Pre(str(prov)[:1200], className="small bg-light p-2 rounded"),
                            ]
                        )
                return (
                    no_update,
                    no_update,
                    no_update,
                    dbc.Alert(
                        [
                            html.Strong("Hết quota / giới hạn tốc độ Gemini (429). "),
                            msg
                            if isinstance(msg, (html.Div, html.P))
                            else html.P(str(msg), className="mb-0"),
                            html.P(
                                [
                                    "Gợi ý: đợi 1–2 phút; trong ",
                                    html.Code(".env"),
                                    " đặt ",
                                    html.Code("GEMINI_MODEL=gemini-1.5-flash"),
                                    " và ",
                                    html.Code("GEMINI_FALLBACK_MODELS=gemini-1.5-flash-8b"),
                                    "; hoặc bật billing / xem ",
                                    html.A("rate limits", href="https://ai.google.dev/gemini-api/docs/rate-limits", target="_blank"),
                                    ".",
                                ],
                                className="small mt-2 mb-0",
                            ),
                        ],
                        color="warning",
                        className="py-2",
                    ),
                    no_update,
                )
            return (
                no_update,
                no_update,
                no_update,
                dbc.Alert(f"Lỗi API ({r.status_code}): {detail}", color="danger"),
                no_update,
            )

        data = r.json()
        rid = data.get("request_id")
        code = data.get("code", "")
        explanation = data.get("explanation", "")
        model_used = data.get("model_used") or ""
        status_children: list[Any] = [
            html.Strong("Trạng thái: Chờ duyệt — "),
            "Đã nhận code từ Gemini. Hãy đọc, chỉnh sửa nếu cần, rồi bấm ",
            html.Strong("Phê duyệt & chạy"),
            f". request_id: `{rid}`",
        ]
        if model_used:
            status_children.extend(
                [html.Br(), html.Small(f"Mô hình API: `{model_used}`", className="text-muted")]
            )
        status = dbc.Alert(status_children, color="info", className="py-2")
        return explanation, code, rid, status, html.P("*(Chưa chạy — kết quả cũ đã xóa)*", className="text-muted small")

    @app.callback(
        Output("ai-run-output", "children", allow_duplicate=True),
        Output("ai-status", "children", allow_duplicate=True),
        Input("ai-run-btn", "n_clicks"),
        State("ai-code", "value"),
        State("ai-request-id-store", "data"),
        prevent_initial_call=True,
    )
    def on_run(_n, code, request_id):
        if not code or not str(code).strip():
            return (
                html.P("Không có code để chạy.", className="text-warning"),
                dbc.Alert("Nhập hoặc sinh code trước.", color="warning", className="py-2"),
            )
        payload: dict = {"code": str(code)}
        if request_id:
            payload["request_id"] = request_id
        try:
            r = requests.post(
                f"{API_BASE}/api/execute/run",
                json=payload,
                timeout=180,
            )
        except requests.RequestException as e:
            return (
                html.P(str(e), className="text-danger"),
                dbc.Alert(f"Lỗi kết nối Execute API: {e}", color="danger"),
            )

        if r.status_code != 200:
            detail = r.text
            try:
                detail = r.json().get("detail", detail)
            except Exception:
                pass
            return (
                html.Pre(str(detail), className="text-danger small"),
                dbc.Alert(f"Lỗi thực thi ({r.status_code})", color="danger", className="py-2"),
            )

        data = r.json()
        status_txt = data.get("status", "")
        stdout = data.get("stdout") or ""
        stderr = data.get("stderr") or ""
        outputs = data.get("outputs") or []

        parts: list[Any] = []
        color = "success" if status_txt == "success" else "danger" if status_txt in ("error", "validation_error") else "warning"
        parts.append(dbc.Badge(status_txt.upper(), color=color, className="me-2"))
        parts.append(html.Span(f" ({data.get('duration_ms', 0)} ms)", className="text-muted small"))

        if stdout:
            parts.append(html.H6("Đầu ra chuẩn (stdout)", className="mt-3"))
            parts.append(html.Pre(stdout, className="bg-dark text-light p-2 rounded small", style={"whiteSpace": "pre-wrap"}))
        if stderr:
            parts.append(html.H6("Lỗi / traceback (stderr)", className="mt-3"))
            parts.append(html.Pre(stderr, className="bg-warning bg-opacity-25 p-2 rounded small", style={"whiteSpace": "pre-wrap"}))

        # Debug: hiển thị số lượng outputs
        if outputs:
            parts.append(html.P(f"[Debug] Tìm thấy {len(outputs)} output(s)", className="small text-info"))

        for idx, o in enumerate(outputs):
            parts.append(html.H6(f"Biểu đồ #{idx+1}", className="mt-3"))
            html_content = o.get("html_content")
            has_content = html_content and len(html_content) > 100

            # Debug info
            parts.append(html.P(
                f"[Debug] html_content: {'Có (' + str(len(html_content)) + ' chars)' if html_content else 'Không có'}, "
                f"url: {o.get('url', 'N/A')}, kind: {o.get('kind', 'N/A')}",
                className="small text-muted"
            ))

            if has_content:
                parts.append(
                    html.Div(
                        html.Iframe(
                            srcDoc=html_content,
                            style={"width": "100%", "height": "520px", "border": "none", "overflow": "hidden"},
                        ),
                        className="border rounded bg-light p-2",
                        style={"backgroundColor": "#f8fafc", "overflow": "hidden"},
                    )
                )
            else:
                url = o.get("url", "")
                full = f"{API_BASE}{url}" if url.startswith("/") else url
                parts.append(html.P(f"Fallback: load từ {full}", className="small text-warning"))
                parts.append(
                    html.Div(
                        html.Iframe(
                            src=full,
                            style={"width": "100%", "height": "520px", "border": "none", "overflow": "hidden"},
                        ),
                        className="border rounded bg-light p-2",
                        style={"backgroundColor": "#f8fafc", "overflow": "hidden"},
                    )
                )

        status_el = dbc.Alert(
            "Trạng thái: Đã chạy trên máy (sandbox API)." if status_txt == "success" else f"Trạng thái: {status_txt}",
            color="success" if status_txt == "success" else "warning",
            className="py-2",
        )
        return html.Div(parts), status_el

    @app.callback(
        Output("ai-history-output", "children"),
        Input("ai-history-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def on_history(_n):
        try:
            r = requests.get(f"{API_BASE}/api/logs/history", params={"limit": 30}, timeout=30)
        except requests.RequestException as e:
            return html.P(f"Lỗi tải lịch sử: {e}", className="text-danger")

        if r.status_code != 200:
            return html.P(r.text, className="text-danger")

        items = r.json().get("items", [])
        if not items:
            return html.P("Chưa có log.")

        rows = []
        for it in items:
            rows.append(
                html.Li(
                    [
                        html.Code(it.get("id", "")[:8] + "…"),
                        " — ",
                        html.Span(it.get("created_at", ""), className="text-muted"),
                        " — ",
                        (it.get("user_prompt") or "")[:80] + ("…" if len(it.get("user_prompt") or "") > 80 else ""),
                        " — ",
                        html.Span(str(it.get("last_status")), className="fw-bold"),
                    ]
                )
            )
        return html.Ul(rows, className="mb-0")
