from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from io_utils import load_sales
from metrics import monthly_kpis, channel_mix, day_of_month_pattern, product_pareto
from charts import (
    save_monthly_charts,
    save_channel_mix,
    save_payday_pattern,
    save_product_pareto,
)

def main() -> None:
    parser = argparse.ArgumentParser(description="Run Sales Reporting 2024 analysis (anonymized).")
    parser.add_argument("--input", required=True, help="Path to CSV/XLSX sales data.")
    parser.add_argument("--out", default="reports", help="Output directory (default: reports).")
    args = parser.parse_args()

    out_root = Path(args.out)
    charts_dir = out_root / "charts"
    out_root.mkdir(parents=True, exist_ok=True)
    charts_dir.mkdir(parents=True, exist_ok=True)

    df = load_sales(args.input)

    m = monthly_kpis(df)
    c = channel_mix(df)
    dom = day_of_month_pattern(df)
    prod = product_pareto(df)

    # Save tables
    m.to_csv(out_root / "monthly_kpis.csv", index=False)
    c.to_csv(out_root / "channel_mix.csv", index=False)
    dom.to_csv(out_root / "day_of_month_pattern.csv", index=False)
    prod.head(200).to_csv(out_root / "product_top200.csv", index=False)

    # Save charts
    save_monthly_charts(m, charts_dir)
    save_channel_mix(c, charts_dir)
    save_payday_pattern(dom, charts_dir)
    save_product_pareto(prod, charts_dir)

    # One-line summary for quick reference
    summary = pd.DataFrame([{
        "net_revenue": float(df["Grand Total"].sum()),
        "orders": int(df["Order#"].nunique()),
        "qty": int(df["QTY"].sum()),
        "aov": float(df["Grand Total"].sum() / max(df["Order#"].nunique(), 1)),
    }])
    summary.to_csv(out_root / "summary.csv", index=False)

    print("Done. Outputs written to:", out_root.resolve())

if __name__ == "__main__":
    main()
