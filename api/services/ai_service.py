"""Gemini-powered code + explanation generation with strict JSON output."""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass
from typing import Any

import google.generativeai as genai

from api.config import DATASET_DESC, GEMINI_API_KEY, GEMINI_FALLBACK_MODELS, GEMINI_MODEL, INSIGHTS_JSON


class GeminiQuotaError(Exception):
    """Raised when all models/retries fail due to API quota or rate limits (HTTP 429)."""

    def __init__(self, message: str, last_error: str | None = None):
        super().__init__(message)
        self.last_error = last_error


@dataclass
class GenerateResult:
    code: str
    explanation: str
    raw_text: str
    model_used: str


def _load_optional_text(path: Any, max_chars: int) -> str:
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text if len(text) <= max_chars else text[: max_chars - 30] + "\n...[truncated]"


def _build_system_instruction() -> str:
    from api.utils.data_loader import dataset_context_snippet

    dataset_doc = _load_optional_text(DATASET_DESC, 6000)
    insights = _load_optional_text(INSIGHTS_JSON, 4000)
    dtypes_block = dataset_context_snippet(8000)

    return f"""Bạn là trợ lý phân tích dữ liệu cho đồ án Trực quan hóa dữ liệu (Việt Nam).

## Quy tắc bắt buộc (theo đề bài)
1. CHỈ được viết Python thao tác trên biến `df` đã được load sẵn (pandas DataFrame). KHÔNG được bịa số liệu, KHÔNG được giả định thống kê không tính từ `df`.
2. Mọi con số trong phần giải thích phải phản ánh kết quả sau khi chạy code (sinh viên sẽ chạy code trên máy). Trong `explanation` chỉ mô tả ý nghĩa và cách đọc biểu đồ/bảng, không liệt kê số cụ thể nếu không được tính từ code.
3. Code phải có comment tiếng Việt trước mỗi khối logic quan trọng, giải thích ngắn gọn đoạn đó làm gì (ví dụ: "Đoạn này lọc OEM và tính trung bình giá theo category").
4. Chỉ được import: pandas (as pd), numpy (as np), plotly.express (as px), plotly.graph_objects (as go), json, math, re.
5. Nếu vẽ biểu đồ Plotly, gán figure vào biến `fig` ở cuối (một figure chính). Có thể dùng print() để in bảng tóm tắt (head, describe, value_counts).
6. Không truy cập file, mạng, os, subprocess.

## Ngữ cảnh dataset (mô tả gốc)
{dataset_doc}

## Tóm tắt insights đã có (tham khảo định hướng, không thay thế việc phân tích từ df)
{insights if insights else "(Không có file insights.)"}

## Cấu trúc dữ liệu thực tế
{dtypes_block}

## Định dạng trả lời
Trả về DUY NHẤT một JSON hợp lệ (không markdown), hai khóa:
- "explanation": chuỗi markdown tiếng Việt, hướng dẫn sinh viên hiểu code và cách đọc kết quả.
- "code": mã Python đầy đủ một đoạn script (có thể nhiều dòng, escape newline trong JSON chuẩn).
"""


def _parse_json_response(text: str) -> dict[str, Any]:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
        if m:
            return json.loads(m.group(1).strip())
        raise


def _models_to_try() -> list[str]:
    primary = (GEMINI_MODEL or "gemini-1.5-flash").strip()
    raw = GEMINI_FALLBACK_MODELS or ""
    fallbacks = [m.strip() for m in raw.split(",") if m.strip()]
    seen: set[str] = set()
    out: list[str] = []
    for m in [primary, *fallbacks]:
        if m and m not in seen:
            seen.add(m)
            out.append(m)
    return out


def _is_quota_or_rate_limit(exc: BaseException) -> bool:
    name = type(exc).__name__
    if name in ("ResourceExhausted", "TooManyRequests"):
        return True
    msg = str(exc).lower()
    if "429" in msg or "quota" in msg or "rate limit" in msg or "resource exhausted" in msg:
        return True
    try:
        from google.api_core import exceptions as gexc

        return isinstance(exc, (gexc.ResourceExhausted, gexc.TooManyRequests))
    except ImportError:
        return False


def _retry_delay_seconds(exc: BaseException) -> float:
    m = re.search(r"retry in ([\d.]+)\s*s", str(exc), re.I)
    if m:
        return min(float(m.group(1)) + 0.75, 90.0)
    return 3.0


def _generate_once(model_name: str, prompt: str) -> str:
    model = genai.GenerativeModel(
        model_name,
        generation_config=genai.GenerationConfig(
            temperature=0.25,
            response_mime_type="application/json",
        ),
    )
    response = model.generate_content(prompt)
    raw = (response.text or "").strip()
    if not raw:
        raise ValueError("Gemini trả về nội dung rỗng (có thể bị chặn an toàn).")
    return raw


def generate_analysis_code(user_request: str, conversation: list[dict[str, str]] | None = None) -> GenerateResult:
    if not GEMINI_API_KEY:
        raise RuntimeError("Thiếu GEMINI_API_KEY trong môi trường (.env).")

    genai.configure(api_key=GEMINI_API_KEY)
    system_instruction = _build_system_instruction()

    parts: list[str] = [f"Yêu cầu phân tích của người dùng:\n{user_request.strip()}"]
    if conversation:
        tail = conversation[-6:]
        conv = "\n".join(f"{m.get('role', 'user')}: {m.get('content', '')}" for m in tail)
        parts.append("Hội thoại gần đây (tùy chọn):\n" + conv)

    user_block = "\n\n".join(parts)
    prompt = system_instruction + "\n\n---\n\n" + user_block

    models = _models_to_try()
    attempts_per_model = int(os.getenv("GEMINI_RETRY_PER_MODEL", "3"))
    last_exc: BaseException | None = None
    last_detail = ""

    for model_name in models:
        for attempt in range(attempts_per_model):
            try:
                raw = _generate_once(model_name, prompt)
                data = _parse_json_response(raw)
                code = str(data.get("code", "")).strip()
                explanation = str(data.get("explanation", "")).strip()
                if not code:
                    raise ValueError("Model không trả về trường code hợp lệ.")
                return GenerateResult(
                    code=code,
                    explanation=explanation,
                    raw_text=raw,
                    model_used=model_name,
                )
            except (json.JSONDecodeError, ValueError) as e:
                # Bad output: do not burn fallbacks for JSON issues; surface to user
                raise
            except Exception as e:
                last_exc = e
                last_detail = str(e)
                if not _is_quota_or_rate_limit(e):
                    raise
                if attempt + 1 < attempts_per_model:
                    time.sleep(_retry_delay_seconds(e))
                else:
                    break

    friendly = (
        "Google Gemini báo hết quota hoặc vượt giới hạn (429) cho tất cả model đã cấu hình. "
        "Hãy: (1) Đợi vài phút rồi thử lại; (2) Đổi GEMINI_MODEL / GEMINI_FALLBACK_MODELS trong .env "
        "(ví dụ gemini-1.5-flash hoặc gemini-1.5-flash-8b); (3) Kiểm tra billing / quota tại "
        "https://ai.google.dev/gemini-api/docs/rate-limits"
    )
    raise GeminiQuotaError(friendly, last_error=last_detail) from last_exc
