"""Load the combined TIKI dataset with the same derived columns as the dashboard."""

from __future__ import annotations

import pandas as pd

from api.config import DATA_PROCESSED


def load_prepared_df() -> pd.DataFrame:
    if not DATA_PROCESSED.exists():
        raise FileNotFoundError(f"Missing dataset file: {DATA_PROCESSED}")
    df = pd.read_csv(DATA_PROCESSED)
    df["discount_pct"] = ((df["original_price"] - df["price"]) / df["original_price"] * 100).round(2)
    df["revenue_estimate"] = df["price"] * df["quantity_sold"]
    df["price_segment"] = pd.cut(
        df["price"],
        bins=[0, 100_000, 300_000, 500_000, 1_000_000, float("inf")],
        labels=["Dưới 100k", "100–300k", "300–500k", "500k–1tr", "Trên 1tr"],
    )
    return df


def dataset_context_snippet(max_chars: int = 12000) -> str:
    """Short description of columns and dtypes for the AI system prompt."""
    df = load_prepared_df()
    lines = [
        "Cột và kiểu dữ liệu (sau khi tiền xử lý giống dashboard):",
        df.dtypes.to_string(),
        "",
        f"Số dòng: {len(df)}",
    ]
    text = "\n".join(lines)
    return text if len(text) <= max_chars else text[: max_chars - 20] + "\n...[truncated]"
