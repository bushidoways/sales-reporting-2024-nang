from __future__ import annotations

import numpy as np
import pandas as pd

def monthly_kpis(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Month"] = df["Date"].dt.to_period("M").dt.to_timestamp()

    out = (
        df.groupby("Month")
          .agg(
              net_revenue=("Grand Total", "sum"),
              orders=("Order#", "nunique"),
              qty=("QTY", "sum"),
              retail=("Retail", "sum"),
              discount=("Discount", "sum"),
              voucher=("Voucher", "sum"),
          )
          .reset_index()
    )
    out["aov"] = out["net_revenue"] / out["orders"].replace(0, np.nan)
    out["effective_discount_rate"] = (out["discount"] + out["voucher"]) / out["retail"].replace(0, np.nan)
    return out

def channel_mix(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df.groupby("Type")
          .agg(net_revenue=("Grand Total", "sum"), orders=("Order#", "nunique"))
          .reset_index()
    )
    out["share"] = out["net_revenue"] / out["net_revenue"].sum()
    return out.sort_values("net_revenue", ascending=False)

def day_of_month_pattern(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["day_of_month"] = df["Date"].dt.day
    return (
        df.groupby("day_of_month")
          .agg(net_revenue=("Grand Total", "sum"), orders=("Order#", "nunique"))
          .reset_index()
          .sort_values("day_of_month")
    )

def product_pareto(df: pd.DataFrame) -> pd.DataFrame:
    total = df["Grand Total"].sum()
    prod = (
        df.groupby("Product Name")
          .agg(net_revenue=("Grand Total", "sum"))
          .sort_values("net_revenue", ascending=False)
          .reset_index()
    )
    prod["share"] = prod["net_revenue"] / total if total else 0
    prod["cum_share"] = prod["share"].cumsum()
    return prod
