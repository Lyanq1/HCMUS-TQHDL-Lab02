"""Run validated user code and format API response."""

from __future__ import annotations

import time
from typing import Any

from api.utils.sandbox import execute_user_code


def run_approved_code(code: str) -> tuple[dict[str, Any], int]:
    start = time.perf_counter()
    result = execute_user_code(code)
    duration_ms = int((time.perf_counter() - start) * 1000)
    return result, duration_ms


def build_outputs(result: dict[str, Any], static_prefix: str = "/static") -> list[dict[str, str]]:
    from api.config import DATA_TEMP
    out = []
    for item in result.get("outputs") or []:
        fn = item.get("filename", "")
        html_content = None
        if item.get("kind") == "plotly_html":
            try:
                html_content = (DATA_TEMP / fn).read_text(encoding="utf-8")
            except Exception:
                pass
        out.append({"url": f"{static_prefix}/{fn}", "kind": item.get("kind", "file"), "html_content": html_content})
    return out
