"""GET /api/logs/* — audit history."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import DetailResponse, HistoryItem, HistoryResponse
from api.services import logs_service

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("/history", response_model=HistoryResponse)
def history(limit: int = 50) -> HistoryResponse:
    rows = logs_service.list_history(limit=min(limit, 200))
    items = [
        HistoryItem(
            id=r["id"],
            created_at=r["created_at"],
            user_prompt=r["user_prompt"],
            model=r["model"],
            last_status=r["last_status"],
        )
        for r in rows
    ]
    return HistoryResponse(items=items)


@router.get("/{request_id}", response_model=DetailResponse)
def detail(request_id: str) -> DetailResponse:
    row = logs_service.get_request_detail(request_id)
    if not row:
        raise HTTPException(status_code=404, detail="Không tìm thấy request_id")
    return DetailResponse(detail=row)
