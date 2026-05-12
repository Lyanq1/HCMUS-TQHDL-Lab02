"""POST /api/ai/generate — Gemini code generation."""

from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException

from api.schemas import GenerateRequest, GenerateResponse
from api.services import ai_service, logs_service
from api.services.ai_service import GeminiQuotaError

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest) -> GenerateResponse:
    request_id = str(uuid.uuid4())
    try:
        result = ai_service.generate_analysis_code(req.user_request, req.conversation)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except GeminiQuotaError as e:
        detail: str | dict = str(e)
        if e.last_error:
            detail = {"message": str(e), "provider_detail": e.last_error[:2000]}
        raise HTTPException(status_code=429, detail=detail) from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Lỗi gọi Gemini: {e}") from e

    logs_service.save_ai_request(
        request_id=request_id,
        user_prompt=req.user_request,
        model=result.model_used,
        explanation=result.explanation,
        generated_code=result.code,
        raw_model_response=result.raw_text,
    )

    return GenerateResponse(
        request_id=request_id,
        code=result.code,
        explanation=result.explanation,
        model_used=result.model_used,
    )
