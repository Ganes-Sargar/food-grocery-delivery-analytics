"""
analysis.py
-----------
Core exploratory data analysis for the Food & Grocery Delivery
Analytics project. Loads the generated dataset, computes key business
KPIs, and saves a set of charts to ../charts/.

Run:
    python scripts/analysis.py
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.dpi"] = 120

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_DIR = os.path.join(BASE_DIR, "data")
CHART_DIR = os.path.join(BASE_DIR, "charts")
os.makedirs(CHART_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# Load data
# ----------------------------------------------------------------------
orders = pd.read_csv(os.path.join(DATA_DIR, "orders.csv"), parse_dates=["order_date"])
customers = pd.read_csv(os.path.join(DATA_DIR, "customers.csv"))
restaurants = pd.read_csv(os.path.join(DATA_DIR, "restaurants.csv"))
delivery_partners = pd.read_csv(os.path.join(DATA_DIR, "delivery_partners.csv"))

delivered = orders[orders["order_status"] == "Delivered"].copy()

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ----------------------------------------------------------------------
# KPI summary
# ----------------------------------------------------------------------
kpis = {
    "total_orders": len(orders),
    "total_revenue": round(delivered["final_amount"].sum(), 2),
    "avg_order_value": round(delivered["final_amount"].mean(), 2),
    "cancellation_rate_pct": round((orders["order_status"] == "Cancelled").mean() * 100, 2),
    "return_rate_pct": round((orders["order_status"] == "Returned").mean() * 100, 2),
    "avg_delivery_time_min": round(delivered["actual_delivery_time_min"].mean(), 2),
    "on_time_delivery_rate_pct": round((delivered["delayed"] == 0).mean() * 100, 2),
    "avg_customer_rating": round(delivered["customer_rating"].mean(), 2),
    "food_vs_grocery_split_pct": (orders["order_type"].value_counts(normalize=True) * 100).round(2).to_dict(),
    "premium_member_share_pct": round(customers["is_premium_member"].mean() * 100, 2),
}

print("=" * 60)
print("KEY BUSINESS KPIs")
print("=" * 60)
for k, v in kpis.items():
    print(f"{k:35s}: {v}")

with open(os.path.join(BASE_DIR, "kpi_summary.txt"), "w") as f:
    f.write("FOOD & GROCERY DELIVERY ANALYTICS - KPI SUMMARY\n")
    f.write("=" * 55 + "\n\n")
    for k, v in kpis.items():
        f.write(f"{k}: {v}\n")

# ----------------------------------------------------------------------
# Chart 1: Monthly revenue trend
# ----------------------------------------------------------------------
delivered["order_month"] = delivered["order_date"].dt.to_period("M").astype(str)
monthly_rev = delivered.groupby("order_month")["final_amount"].sum().reset_index()

plt.figure(figsize=(9, 5))
sns.lineplot(data=monthly_rev, x="order_month", y="final_amount", marker="o", linewidth=2.5)
plt.title("Monthly Revenue Trend (Jan - Jun 2026)", fontsize=13, fontweight="bold")
plt.xlabel("Month")
plt.ylabel("Revenue (₹)")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "01_monthly_revenue_trend.png"))
plt.close()

# ----------------------------------------------------------------------
# Chart 2: Orders by day of week
# ----------------------------------------------------------------------
dow_orders = orders["day_of_week"].value_counts().reindex(day_order)

plt.figure(figsize=(9, 5))
sns.barplot(x=dow_orders.index, y=dow_orders.values)
plt.title("Order Volume by Day of Week", fontsize=13, fontweight="bold")
plt.xlabel("Day")
plt.ylabel("Number of Orders")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "02_orders_by_day_of_week.png"))
plt.close()

# ----------------------------------------------------------------------
# Chart 3: Orders by hour of day (peak hour analysis)
# ----------------------------------------------------------------------
hour_orders = orders["order_hour"].value_counts().sort_index()

plt.figure(figsize=(10, 5))
sns.barplot(x=hour_orders.index, y=hour_orders.values, color="#4C72B0")
plt.title("Order Volume by Hour of Day (Peak Hour Analysis)", fontsize=13, fontweight="bold")
plt.xlabel("Hour of Day (24h)")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "03_orders_by_hour.png"))
plt.close()

# ----------------------------------------------------------------------
# Chart 4: City-wise revenue
# ----------------------------------------------------------------------
city_rev = delivered.groupby("city")["final_amount"].sum().sort_values(ascending=False)

plt.figure(figsize=(9, 5))
sns.barplot(x=city_rev.values, y=city_rev.index, orient="h")
plt.title("Revenue by City", fontsize=13, fontweight="bold")
plt.xlabel("Revenue (₹)")
plt.ylabel("City")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "04_revenue_by_city.png"))
plt.close()

# ----------------------------------------------------------------------
# Chart 5: Food vs Grocery order share
# ----------------------------------------------------------------------
type_share = orders["order_type"].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(type_share.values, labels=type_share.index, autopct="%1.1f%%",
        startangle=90, colors=sns.color_palette("Set2"))
plt.title("Food Delivery vs Grocery — Order Share", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "05_food_vs_grocery_share.png"))
plt.close()

# ----------------------------------------------------------------------
# Chart 6: Delivery time distribution (on-time vs delayed)
# ----------------------------------------------------------------------
plt.figure(figsize=(9, 5))
sns.histplot(delivered["actual_delivery_time_min"], bins=40, kde=True, color="#55A868")
plt.axvline(delivered["actual_delivery_time_min"].mean(), color="red", linestyle="--",
            label=f'Mean = {delivered["actual_delivery_time_min"].mean():.1f} min')
plt.title("Distribution of Actual Delivery Time", fontsize=13, fontweight="bold")
plt.xlabel("Delivery Time (minutes)")
plt.ylabel("Number of Orders")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "06_delivery_time_distribution.png"))
plt.close()

# ----------------------------------------------------------------------
# Chart 7: Cancellation reasons
# ----------------------------------------------------------------------
cancel_df = orders[orders["order_status"].isin(["Cancelled", "Returned"])]
reason_counts = cancel_df["cancel_return_reason"].value_counts()

plt.figure(figsize=(9, 5))
sns.barplot(x=reason_counts.values, y=reason_counts.index, orient="h", color="#C44E52")
plt.title("Order Cancellation / Return Reasons", fontsize=13, fontweight="bold")
plt.xlabel("Count")
plt.ylabel("Reason")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "07_cancellation_reasons.png"))
plt.close()

# ----------------------------------------------------------------------
# Chart 8: Payment method preference
# ----------------------------------------------------------------------
pay_counts = orders["payment_method"].value_counts()

plt.figure(figsize=(8, 5))
sns.barplot(x=pay_counts.index, y=pay_counts.values, color="#8172B2")
plt.title("Preferred Payment Methods", fontsize=13, fontweight="bold")
plt.xlabel("Payment Method")
plt.ylabel("Number of Orders")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "08_payment_methods.png"))
plt.close()

# ----------------------------------------------------------------------
# Chart 9: Rating vs on-time delivery
# ----------------------------------------------------------------------
plt.figure(figsize=(7, 5))
sns.boxplot(data=delivered, x="delayed", y="customer_rating")
plt.xticks([0, 1], ["On-Time", "Delayed"])
plt.title("Customer Rating: On-Time vs Delayed Deliveries", fontsize=13, fontweight="bold")
plt.xlabel("")
plt.ylabel("Customer Rating")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "09_rating_vs_delay.png"))
plt.close()

# ----------------------------------------------------------------------
# Chart 10: Top 10 outlets by revenue
# ----------------------------------------------------------------------
top_outlets = delivered.groupby("outlet_name")["final_amount"].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(9, 5))
sns.barplot(x=top_outlets.values, y=top_outlets.index, orient="h", color="#DD8452")
plt.title("Top 10 Outlets by Revenue", fontsize=13, fontweight="bold")
plt.xlabel("Revenue (₹)")
plt.ylabel("Outlet")
plt.tight_layout()
plt.savefig(os.path.join(CHART_DIR, "10_top_outlets_by_revenue.png"))
plt.close()

print("\nAll charts saved to:", CHART_DIR)
print("KPI summary saved to:", os.path.join(BASE_DIR, "kpi_summary.txt"))
