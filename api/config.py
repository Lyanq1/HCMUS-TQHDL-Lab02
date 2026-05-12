"""Load settings from environment (project root .env)."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")

GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
# gemini-2.0-flash often hits free-tier "limit: 0" in some regions; 1.5-flash is a safer default.
GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
# Comma-separated list, tried in order after retries on the primary model fail with 429/quota.
GEMINI_FALLBACK_MODELS: str = os.getenv(
    "GEMINI_FALLBACK_MODELS",
    "gemini-1.5-flash-8b",
)

DATA_PROCESSED: Path = _ROOT / "data" / "processed" / "combined_tiki_data.csv"
DATA_TEMP: Path = _ROOT / "data" / "temp"
INSIGHTS_JSON: Path = _ROOT / "data" / "processed" / "insights_summary.json"
DATASET_DESC: Path = _ROOT / "dataset" / "Dataset_description.md"

DB_PATH: Path = Path(os.getenv("AI_LOGS_DB", str(_ROOT / "api" / "database" / "logs.db")))

EXECUTION_TIMEOUT_SEC: int = int(os.getenv("EXECUTION_TIMEOUT_SEC", "60"))

CORS_ORIGINS: list[str] = [
    "http://127.0.0.1:8050",
    "http://localhost:8050",
]
