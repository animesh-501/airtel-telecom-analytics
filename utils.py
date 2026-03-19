"""
utils.py — Shared utilities for Airtel Telecom Analytics Pipeline
Animesh Choubey | github.com/animesh-501

Used by all 4 phase notebooks. Import with:
    from utils import log, section, save_fig, force_numeric, snapshot
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# ─── LOGGING ─────────────────────────────────────────────────────────────────

_log_lines = []

def log(msg: str, store: bool = True):
    """Print with timestamp and optionally store for report export."""
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    if store:
        _log_lines.append(line)

def section(title: str):
    """Print a bold section header."""
    bar = "=" * 60
    log(f"\n{bar}\n  {title}\n{bar}")

def get_log_lines() -> list:
    return _log_lines.copy()

def reset_log():
    _log_lines.clear()

def save_report(path: str):
    """Write accumulated log lines to a text file."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(_log_lines))
    log(f"📄 Report saved → {path}", store=False)


# ─── DATAFRAME HELPERS ───────────────────────────────────────────────────────

def force_numeric(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    """
    Strip ' INR' suffix and coerce columns to numeric.
    Shared across all phases — defined once here.
    """
    df = df.copy()
    for col in cols:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                       .str.replace(" INR", "", regex=False)
                       .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def snapshot(df: pd.DataFrame, name: str):
    """Log shape, null count, and duplicate count for a dataframe."""
    log(f"\n  [{name}]")
    log(f"    Shape      : {df.shape[0]:,} rows × {df.shape[1]} cols")
    log(f"    Nulls      : {df.isnull().sum().sum():,}")
    log(f"    Duplicates : {df.duplicated().sum():,}")


def validate_categorical(df: pd.DataFrame, col: str, valid_values: set, label: str = ""):
    """Warn if unexpected values exist in a categorical column."""
    found = set(df[col].dropna().unique())
    unexpected = found - valid_values
    if unexpected:
        log(f"  ⚠  {label or col}: unexpected values → {unexpected}")
    else:
        log(f"  ✓  {label or col}: all values valid")


# ─── CHART HELPERS ───────────────────────────────────────────────────────────

def save_fig(output_dir: str, name: str, dpi: int = 130):
    """Save current matplotlib figure and close it."""
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, f"{name}.png")
    plt.savefig(path, bbox_inches="tight", dpi=dpi)
    plt.close()
    log(f"  ✓ Chart saved → {path}")
    return path


# ─── RISK SCORING ────────────────────────────────────────────────────────────

# Risk score weights — documented in one place so they're easy to tune
RISK_WEIGHTS = {
    # Each unpaid bill adds this many points (strong signal of payment default risk)
    "unpaid_count":      15,
    # Each ₹1 of arrears adds this many points (scaled down since arrears can be large)
    "total_arrears":     0.01,
    # Each support ticket adds points (high-contact customers more likely to churn)
    "ticket_count":      5,
    # Escalated tickets are a stronger churn signal than regular tickets
    "escalated_count":   20,
    # Low CSAT = dissatisfied customer; max CSAT is 5 so (5 - score) is inverse satisfaction
    "csat_inverse":      10,
    # New customers churn more; cap tenure at 72 months, invert so low tenure = high risk
    "tenure_inverse":    0.5,
    # Higher-value plans see more price sensitivity churn
    "plan_price":        0.05,
}

def compute_risk_score(df: pd.DataFrame) -> pd.Series:
    """
    Compute a churn risk score per customer row.
    Uses RISK_WEIGHTS (above) — edit weights there, not here.

    Returns a Series of float scores (higher = more at risk).
    """
    score = (
        df.get("unpaid_count",    0) * RISK_WEIGHTS["unpaid_count"]
      + df.get("total_arrears",   0) * RISK_WEIGHTS["total_arrears"]
      + df.get("ticket_count",    0) * RISK_WEIGHTS["ticket_count"]
      + df.get("escalated_count", 0) * RISK_WEIGHTS["escalated_count"]
      + (5 - df.get("avg_csat",   0)) * RISK_WEIGHTS["csat_inverse"]
      + (72 - df.get("tenure_months", 0).clip(0, 72)) * RISK_WEIGHTS["tenure_inverse"]
      + df.get("plan_price",      0) * RISK_WEIGHTS["plan_price"]
    )
    return score.round(2)


RISK_BINS   = [0, 30, 60, 100, float("inf")]
RISK_LABELS = ["Low Risk", "Medium Risk", "High Risk", "Critical Risk"]

def segment_risk(scores: pd.Series) -> pd.Series:
    """Bin continuous risk scores into named segments."""
    return pd.cut(scores, bins=RISK_BINS, labels=RISK_LABELS)
