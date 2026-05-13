"""Pydantic request/response models for the AI API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    user_request: str = Field(..., min_length=1, max_length=8000)
    conversation: list[dict[str, str]] | None = None


class GenerateResponse(BaseModel):
    request_id: str
    code: str
    explanation: str
    model_used: str | None = None


class ExecuteRequest(BaseModel):
    request_id: str | None = None
    code: str = Field(..., min_length=1)


class OutputFile(BaseModel):
    url: str
    kind: str
    html_content: str | None = None


class ExecuteResponse(BaseModel):
    request_id: str | None = None
    status: str
    stdout: str
    stderr: str
    duration_ms: int
    outputs: list[OutputFile]


class HistoryItem(BaseModel):
    id: str
    created_at: str
    user_prompt: str
    model: str | None
    last_status: str | None


class HistoryResponse(BaseModel):
    items: list[HistoryItem]


class DetailResponse(BaseModel):
    detail: dict[str, Any]
