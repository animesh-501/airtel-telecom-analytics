"""
config.py — Central configuration for Airtel Telecom Analytics Pipeline
Animesh Choubey | github.com/animesh-501

Edit values here — all 4 phase notebooks import from this file.
"""

import os

# ─── RANDOM SEEDS ────────────────────────────────────────────────────────────
SEED = 42

# ─── DATA SIZES ──────────────────────────────────────────────────────────────
N_CUSTOMERS  = 1_000
N_BILLING    = 5_000
N_CHURN      = 400
N_TICKETS    = 2_000

# SDV synthetic expansion multipliers
SDV_CUSTOMERS_ROWS = 2_000
SDV_BILLING_ROWS   = 8_000
SDV_CHURN_ROWS     = 800

# ─── DIRECTORIES ─────────────────────────────────────────────────────────────
RAW_DIR      = "airtel_raw_data"
CLEAN_DIR    = "airtel_clean_data"
EDA_DIR      = "airtel_eda_outputs"
FORECAST_DIR = "airtel_forecast_outputs"

for _d in [RAW_DIR, CLEAN_DIR, EDA_DIR, FORECAST_DIR]:
    os.makedirs(_d, exist_ok=True)

# ─── NOISE INJECTION ─────────────────────────────────────────────────────────
# Customers / churn
NULL_RATE_CUSTOMERS = 0.07
DUPE_RATE_CUSTOMERS = 0.02

# Billing (slightly more noise — mirrors real billing systems)
NULL_RATE_BILLING   = 0.06
DUPE_RATE_BILLING   = 0.03

# ─── TELECOM DOMAIN DATA ─────────────────────────────────────────────────────
REGIONS = {
    "North": ["Delhi", "UP", "Haryana", "Punjab", "Rajasthan", "Uttarakhand"],
    "South": ["Tamil Nadu", "Karnataka", "Kerala", "Andhra Pradesh", "Telangana"],
    "East":  ["West Bengal", "Bihar", "Odisha", "Jharkhand", "Assam"],
    "West":  ["Maharashtra", "Gujarat", "Goa", "MP", "Chhattisgarh"],
}

PREPAID_PLANS  = ["Smart Recharge 49", "Smart Recharge 149",
                  "Smart Recharge 299", "Smart Recharge 599"]
POSTPAID_PLANS = ["Airtel Infinity 199", "Airtel Infinity 299",
                  "Airtel Infinity 499", "Airtel Infinity 999"]

PLAN_PRICE = {
    "Smart Recharge 49":   49,   "Smart Recharge 149":  149,
    "Smart Recharge 299":  299,  "Smart Recharge 599":  599,
    "Airtel Infinity 199": 199,  "Airtel Infinity 299": 299,
    "Airtel Infinity 499": 499,  "Airtel Infinity 999": 999,
}

VALID_PLAN_TYPES      = {"Prepaid", "Postpaid"}
VALID_PAYMENT_STATUS  = {"Paid", "Unpaid", "Partial"}
VALID_CHURN_TYPES     = {"Voluntary", "Involuntary"}

CHURN_REASONS    = ["Price Too High", "Poor Network", "Better Offer Elsewhere",
                    "Relocation", "Payment Default", "Customer Service Issues", "Device Change"]
COMPETITORS      = ["Jio", "Vi", "BSNL", "Tata Play", ""]
ISSUE_CATEGORIES = ["Billing Dispute", "Network Issue", "Payment Issue",
                    "Plan Change", "Account Issue", "Port Request", "Data Speed"]
CHANNELS         = ["App", "Call", "WhatsApp", "Store", "Web"]
ACQ_CHANNELS     = ["Online", "Store", "Agent", "Referral", "Campaign"]

# ─── PROPHET SETTINGS ────────────────────────────────────────────────────────
# With only ~12 months of data, a lower changepoint_prior_scale prevents overfitting.
# Original was 0.3 (too flexible for short series). 0.05 gives smoother forecasts.
PROPHET_CHANGEPOINT_SCALE = 0.05
PROPHET_FORECAST_PERIODS  = 6   # months ahead

# ─── YDATA PROFILING ─────────────────────────────────────────────────────────
# minimal=True is dramatically faster (avoids correlation & interaction matrices).
# Set to False only if you have time and want the full report.
YDATA_MINIMAL = True

# ─── MATPLOTLIB ──────────────────────────────────────────────────────────────
CHART_DPI     = 130
CHART_STYLE   = "whitegrid"
CHART_PALETTE = "Set2"
