"""SQLite persistence for AI requests and executions."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from api.config import DB_PATH


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    schema = Path(__file__).resolve().parent.parent / "database" / "schema.sql"
    sql = schema.read_text(encoding="utf-8")
    conn = _connect()
    try:
        conn.executescript(sql)
        conn.commit()
    finally:
        conn.close()


def save_ai_request(
    request_id: str,
    user_prompt: str,
    model: str,
    explanation: str,
    generated_code: str,
    raw_model_response: str,
) -> None:
    conn = _connect()
    try:
        conn.execute(
            """
            INSERT INTO ai_requests (id, user_prompt, model, explanation, generated_code, raw_model_response)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (request_id, user_prompt, model, explanation, generated_code, raw_model_response),
        )
        conn.commit()
    finally:
        conn.close()


def save_execution(
    request_id: str,
    final_code: str,
    status: str,
    stdout: str,
    stderr: str,
    duration_ms: int,
    output_paths: list[dict[str, Any]] | None,
) -> int:
    conn = _connect()
    try:
        cur = conn.execute(
            """
            INSERT INTO executions (request_id, final_code, status, stdout, stderr, duration_ms, output_paths)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                request_id,
                final_code,
                status,
                stdout,
                stderr,
                duration_ms,
                json.dumps(output_paths or []),
            ),
        )
        conn.commit()
        return int(cur.lastrowid or 0)
    finally:
        conn.close()


def list_history(limit: int = 50) -> list[dict[str, Any]]:
    conn = _connect()
    try:
        cur = conn.execute(
            """
            SELECT r.id, r.created_at, r.user_prompt, r.model,
                   (SELECT e.status FROM executions e WHERE e.request_id = r.id ORDER BY e.id DESC LIMIT 1) AS last_status
            FROM ai_requests r
            ORDER BY r.created_at DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def get_request_detail(request_id: str) -> dict[str, Any] | None:
    conn = _connect()
    try:
        cur = conn.execute("SELECT * FROM ai_requests WHERE id = ?", (request_id,))
        row = cur.fetchone()
        if not row:
            return None
        out: dict[str, Any] = dict(row)
        cur2 = conn.execute(
            "SELECT * FROM executions WHERE request_id = ? ORDER BY id DESC",
            (request_id,),
        )
        out["executions"] = [dict(r) for r in cur2.fetchall()]
        return out
    finally:
        conn.close()
