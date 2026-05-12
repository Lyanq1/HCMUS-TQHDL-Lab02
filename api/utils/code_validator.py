"""AST-based validation: whitelist imports and block dangerous constructs."""

from __future__ import annotations

import ast
from typing import Iterable

ALLOWED_MODULES: frozenset[str] = frozenset(
    {
        "pandas",
        "pd",
        "numpy",
        "np",
        "plotly",
        "plotly.express",
        "plotly.graph_objects",
        "px",
        "go",
        "json",
        "math",
        "re",
    }
)

FORBIDDEN_NAMES: frozenset[str] = frozenset(
    {
        "open",
        "exec",
        "eval",
        "compile",
        "__import__",
        "input",
        "breakpoint",
        "globals",
        "locals",
        "vars",
        "getattr",
        "setattr",
        "delattr",
        "memoryview",
        "help",
    }
)


class _Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: list[str] = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            top = alias.name.split(".")[0]
            if top not in ALLOWED_MODULES and alias.name not in ALLOWED_MODULES:
                self.errors.append(f"Import không được phép: {alias.name}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module is None:
            self.errors.append("from ? import ... không được phép (thiếu module)")
            return
        top = node.module.split(".")[0]
        full = node.module
        if top not in ALLOWED_MODULES and full not in ALLOWED_MODULES:
            self.errors.append(f"ImportFrom không được phép: {node.module}")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if isinstance(node.value, ast.Name) and node.value.id in {"os", "sys", "subprocess", "socket", "shutil", "pathlib"}:
            self.errors.append(f"Truy cập thuộc tính không an toàn: {node.value.id}.{node.attr}")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_NAMES:
            self.errors.append(f"Lời gọi không được phép: {node.func.id}()")
        self.generic_visit(node)


def validate_user_code(source: str) -> tuple[bool, list[str]]:
    try:
        tree = ast.parse(source, mode="exec")
    except SyntaxError as e:
        return False, [f"Lỗi cú pháp: {e}"]

    visitor = _Visitor()
    visitor.visit(tree)
    if visitor.errors:
        return False, visitor.errors

    lowered = source.lower()
    if "import subprocess" in lowered or "from subprocess" in lowered:
        return False, ["Chuỗi mã chứa import subprocess (cấm)"]
    if "os.system" in lowered:
        return False, ["Chuỗi mã chứa os.system (cấm)"]
    if "import socket" in lowered or "from socket" in lowered:
        return False, ["Chuỗi mã chứa import socket (cấm)"]

    return True, []


def assert_valid(source: str) -> None:
    ok, errs = validate_user_code(source)
    if not ok:
        raise ValueError("; ".join(errs))
