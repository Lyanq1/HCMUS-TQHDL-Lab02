"""FastAPI entry: AI generation, sandboxed execution, static plot files, SQLite logs."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.config import CORS_ORIGINS, DATA_TEMP
from api.routers import ai_router, execution_router, logs_router
from api.services.logs_service import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    DATA_TEMP.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(title="TIKI AI Assistant API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router.router, prefix="/api")
app.include_router(execution_router.router, prefix="/api")
app.include_router(logs_router.router, prefix="/api")

app.mount("/static", StaticFiles(directory=str(DATA_TEMP)), name="static")


@app.get("/health")
def health():
    return {"status": "ok"}
