"""POST /api/execute/run — run human-approved code locally."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.schemas import ExecuteRequest, ExecuteResponse, OutputFile
from api.services import execution_service, logs_service
from api.utils.code_validator import validate_user_code

router = APIRouter(prefix="/execute", tags=["execute"])


@router.post("/run", response_model=ExecuteResponse)
def run_code(req: ExecuteRequest) -> ExecuteResponse:
    ok, errs = validate_user_code(req.code)
    if not ok:
        raise HTTPException(status_code=400, detail="; ".join(errs))

    result, duration_ms = execution_service.run_approved_code(req.code)
    status = result.get("status", "error")
    stdout = result.get("stdout") or ""
    stderr = result.get("stderr") or ""
    outputs_raw = execution_service.build_outputs(result)

    logs_service.save_execution(
        request_id=req.request_id,
        final_code=req.code,
        status=status,
        stdout=stdout,
        stderr=stderr,
        duration_ms=duration_ms,
        output_paths=outputs_raw,
    )

    outputs = [OutputFile(url=o["url"], kind=o["kind"]) for o in outputs_raw]

    return ExecuteResponse(
        request_id=req.request_id,
        status=status,
        stdout=stdout,
        stderr=stderr,
        duration_ms=duration_ms,
        outputs=outputs,
    )
