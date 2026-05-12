import pytest

from api.utils.code_validator import validate_user_code


def test_allows_pandas_import():
    ok, errs = validate_user_code("import pandas as pd\nx = 1\n")
    assert ok, errs


def test_rejects_os_import():
    ok, errs = validate_user_code("import os\nos.system('ls')\n")
    assert not ok


def test_rejects_open_call():
    ok, errs = validate_user_code("open('/etc/passwd')\n")
    assert not ok


def test_rejects_subprocess_import():
    ok, errs = validate_user_code("import pandas as pd\nimport subprocess\n")
    assert not ok


def test_syntax_error():
    ok, errs = validate_user_code("def broken(\n")
    assert not ok
    assert any("cú pháp" in e or "Syntax" in e for e in errs)
