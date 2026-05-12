#!/usr/bin/env python3
"""Run the FastAPI backend from the project root (required for imports and data paths)."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=True)
