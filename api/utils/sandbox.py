"""
Run user-approved Python in an isolated process with timeout.

Pandas/Plotly are incompatible with strict RestrictedPython.compile_restricted
for typical analysis snippets; we use AST validation (code_validator) plus
a subprocess with a minimal global namespace instead.
"""

from __future__ import annotations

import builtins
import io
import json
import math
import traceback
import uuid
from contextlib import redirect_stderr, redirect_stdout
from multiprocessing import get_context
from typing import Any, Sequence

from api.config import DATA_TEMP, EXECUTION_TIMEOUT_SEC
from api.utils.code_validator import assert_valid

# Modules user code may load via `import` (must stay in sync with code_validator whitelist).
_ALLOWED_IMPORT_QNAMES: frozenset[str] = frozenset(
    {
        "pandas",
        "numpy",
        "plotly",
        "plotly.express",
        "plotly.graph_objects",
        "plotly.io",
        "json",
        "math",
        "re",
    }
)


def _import_name_allowed(name: str) -> bool:
    name = name.strip()
    if name in _ALLOWED_IMPORT_QNAMES:
        return True
    parts = name.split(".")
    if len(parts) >= 2 and parts[0] == "plotly":
        return parts[1] in {"express", "graph_objects", "io", "subplots", "offline"}
    return False


def _restricted_import(
    name: str,
    globals_: dict | None = None,
    locals_: dict | None = None,
    fromlist: Sequence[str] = (),
    level: int = 0,
):
    """Minimal __import__ so `import pandas` works under a custom __builtins__ dict."""
    if level != 0:
        raise ImportError("Import tương đối không được phép.")
    if fromlist:
        for sub in fromlist:
            if sub == "*":
                raise ImportError("from ... import * không được phép.")
            full = f"{name}.{sub}" if name else sub
            if not _import_name_allowed(full):
                raise ImportError(f"Không được import: {full!r}")
        return builtins.__import__(name, globals_, locals_, fromlist, level)
    if not _import_name_allowed(name):
        raise ImportError(f"Không được import module: {name!r}")
    return builtins.__import__(name, globals_, locals_, fromlist, level)


def _execute_body(code: str) -> dict[str, Any]:
    """Runs in child process."""
    import numpy as np
    import pandas as pd
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio

    from api.utils.data_loader import load_prepared_df

    buf_out = io.StringIO()
    buf_err = io.StringIO()
    outputs: list[dict[str, str]] = []
    status = "success"
    err_msg = ""

    df = load_prepared_df()
    globs: dict[str, Any] = {
        "df": df,
        "pd": pd,
        "np": np,
        "px": px,
        "go": go,
        "json": json,
        "math": math,
        "__builtins__": {
            "__import__": _restricted_import,
            "len": len,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
            "tuple": tuple,
            "set": set,
            "range": range,
            "enumerate": enumerate,
            "zip": zip,
            "min": min,
            "max": max,
            "sum": sum,
            "abs": abs,
            "round": round,
            "print": print,
            "isinstance": isinstance,
            "repr": repr,
            "sorted": sorted,
        },
    }

    try:
        assert_valid(code)
    except ValueError as e:
        return {
            "status": "validation_error",
            "stdout": "",
            "stderr": str(e),
            "outputs": [],
        }

    DATA_TEMP.mkdir(parents=True, exist_ok=True)

    try:
        with redirect_stdout(buf_out), redirect_stderr(buf_err):
            exec(compile(code, "<user_code>", "exec"), globs, {})

        fig = globs.get("fig")
        if fig is not None:
            if hasattr(fig, "write_html"):
                fname = f"fig_{uuid.uuid4().hex}.html"
                fpath = DATA_TEMP / fname
                pio.write_html(fig, file=str(fpath), include_plotlyjs="cdn", full_html=True)
                outputs.append({"filename": fname, "kind": "plotly_html"})
            else:
                buf_err.write("Biến `fig` không phải đối tượng Plotly Figure hợp lệ.\n")

    except Exception:
        status = "error"
        err_msg = traceback.format_exc()
        buf_err.write(err_msg)

    return {
        "status": status,
        "stdout": buf_out.getvalue(),
        "stderr": buf_err.getvalue(),
        "outputs": outputs,
    }


def _mp_worker(code: str, conn: Any) -> None:
    try:
        conn.send(_execute_body(code))
    except Exception:
        conn.send(
            {
                "status": "error",
                "stdout": "",
                "stderr": traceback.format_exc(),
                "outputs": [],
            }
        )
    finally:
        conn.close()


def execute_user_code(code: str, timeout_sec: int | None = None) -> dict[str, Any]:
    """
    Validate and execute code in a spawned subprocess with join timeout.
    Returns dict: status, stdout, stderr, outputs (list of {filename, kind}).
    """
    assert_valid(code)
    timeout = timeout_sec if timeout_sec is not None else EXECUTION_TIMEOUT_SEC

    ctx = get_context("spawn")
    parent_conn, child_conn = ctx.Pipe(duplex=False)
    proc = ctx.Process(target=_mp_worker, args=(code, child_conn))
    proc.start()
    proc.join(timeout=timeout)

    try:
        if proc.is_alive():
            proc.terminate()
            proc.join(5)
            return {
                "status": "timeout",
                "stdout": "",
                "stderr": f"Thực thi vượt quá {timeout} giây và đã bị dừng.",
                "outputs": [],
            }

        if parent_conn.poll(2.0):
            return parent_conn.recv()
        return {
            "status": "error",
            "stdout": "",
            "stderr": "Không nhận được kết quả từ tiến trình thực thi.",
            "outputs": [],
        }
    finally:
        try:
            parent_conn.close()
        except Exception:
            pass
