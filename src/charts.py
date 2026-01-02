from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def save_monthly_charts(monthly: pd.DataFrame, out_dir: str | Path) -> None:
    out_dir = Path(out_dir)
    _ensure_dir(out_dir)

    m = monthly.copy()
    m["MonthLabel"] = pd.to_datetime(m["Month"]).dt.strftime("%b")

    # Monthly net revenue
    plt.figure(figsize=(10, 4))
    plt.plot(m["MonthLabel"], m["net_revenue"])
    plt.xlabel("Month (2024)")
    plt.ylabel("Net Revenue (IDR)")
    plt.title("Monthly Net Revenue (2024)")
    plt.tight_layout()
    plt.savefig(out_dir / "monthly_net_revenue_2024.png", dpi=160)
    plt.close()

    # Monthly orders
    plt.figure(figsize=(10, 4))
    plt.plot(m["MonthLabel"], m["orders"])
    plt.xlabel("Month (2024)")
    plt.ylabel("Orders")
    plt.title("Monthly Orders (2024)")
    plt.tight_layout()
    plt.savefig(out_dir / "monthly_orders_2024.png", dpi=160)
    plt.close()

    # Discount rate
    plt.figure(figsize=(10, 4))
    plt.plot(m["MonthLabel"], m["effective_discount_rate"] * 100)
    plt.xlabel("Month (2024)")
    plt.ylabel("Effective Discount Rate (%)")
    plt.title("Effective Discount Rate by Month (2024)")
    plt.tight_layout()
    plt.savefig(out_dir / "effective_discount_rate_2024.png", dpi=160)
    plt.close()

def save_channel_mix(channel: pd.DataFrame, out_dir: str | Path) -> None:
    out_dir = Path(out_dir)
    _ensure_dir(out_dir)

    c = channel.copy()
    plt.figure(figsize=(10, 4))
    plt.bar(c["Type"], c["net_revenue"])
    plt.xlabel("Channel")
    plt.ylabel("Net Revenue (IDR)")
    plt.title("Channel Mix by Net Revenue (2024)")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(out_dir / "channel_mix_net_revenue_2024.png", dpi=160)
    plt.close()

def save_payday_pattern(dom: pd.DataFrame, out_dir: str | Path) -> None:
    out_dir = Path(out_dir)
    _ensure_dir(out_dir)

    plt.figure(figsize=(10, 4))
    plt.plot(dom["day_of_month"], dom["net_revenue"])
    plt.xlabel("Day of Month")
    plt.ylabel("Net Revenue (IDR)")
    plt.title("Day-of-Month Revenue Pattern (2024)")
    plt.tight_layout()
    plt.savefig(out_dir / "payday_effect_day_of_month_2024.png", dpi=160)
    plt.close()

def save_product_pareto(prod: pd.DataFrame, out_dir: str | Path) -> None:
    out_dir = Path(out_dir)
    _ensure_dir(out_dir)

    plt.figure(figsize=(10, 4))
    plt.plot(np.arange(1, len(prod) + 1), prod["cum_share"] * 100)
    plt.xlabel("Products ranked by revenue")
    plt.ylabel("Cumulative share of net revenue (%)")
    plt.title("Product Revenue Concentration (Pareto) — 2024")
    plt.tight_layout()
    plt.savefig(out_dir / "product_pareto_cumulative_2024.png", dpi=160)
    plt.close()
