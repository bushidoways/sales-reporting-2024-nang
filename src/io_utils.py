from __future__ import annotations

import pandas as pd

REQUIRED_COLUMNS = [
    "Date", "Order#", "Type", "Product Name", "QTY", "Retail", "Discount", "Voucher", "Grand Total"
]

def load_sales(path: str) -> pd.DataFrame:
    """Load sales data from CSV or Excel into a clean DataFrame."""
    if path.lower().endswith((".xlsx", ".xls")):
        # default: read first sheet
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path)

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df["QTY"] = pd.to_numeric(df["QTY"], errors="coerce").fillna(0).astype(int)

    for c in ["Retail", "Discount", "Voucher", "Grand Total"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    return df
