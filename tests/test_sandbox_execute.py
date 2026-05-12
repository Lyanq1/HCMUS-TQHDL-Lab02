"""Optional integration tests for sandbox execution (needs working pandas + plotly)."""

import os

import pytest

RUN = os.environ.get("RUN_SANDBOX_TESTS") == "1"


@pytest.mark.skipif(not RUN, reason="Set RUN_SANDBOX_TESTS=1 to run (requires pandas/plotly compatible with NumPy).")
def test_execute_user_code_subprocess():
    from api.utils.sandbox import execute_user_code

    code = "# Đoạn này in kích thước df\nprint(len(df))\n"
    r = execute_user_code(code, timeout_sec=90)
    assert r["status"] == "success"
    assert r["stdout"].strip().isdigit()


@pytest.mark.skipif(not RUN, reason="Set RUN_SANDBOX_TESTS=1 to run.")
def test_execute_body_print_len():
    from api.utils.sandbox import _execute_body

    code = "# Đoạn này in số dòng\nprint(len(df))\n"
    r = _execute_body(code)
    assert r["status"] == "success"
    out = r["stdout"].strip()
    assert out.isdigit()
    assert int(out) > 1000
