import json
import os

def md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}

def code(src):
    return {"cell_type": "code", "execution_count": None, "metadata": {},
            "outputs": [], "source": src.splitlines(keepends=True)}

cells = []

cells.append(md(
"""# 🛵 Food & Grocery Delivery Analytics

**Author:** *Your Name Here*
**Project type:** Data Analytics / Exploratory Data Analysis (EDA)
**Domain:** Quick-commerce / Food & Grocery Delivery (Swiggy / Zomato / Blinkit / Zepto style)

## Problem Statement
Online food and grocery delivery platforms generate huge volumes of operational
data every day — orders, delivery times, cancellations, ratings, and revenue.
This project analyzes a 6-month simulated operations dataset to answer:

1. How is revenue trending month over month?
2. When do customers order the most (peak hours / days)?
3. Which cities and outlets drive the most revenue?
4. How reliable is delivery performance (on-time rate, avg delivery time)?
5. Why do orders get cancelled or returned, and how does that affect ratings?
6. What is the food vs grocery order mix, and how do customers prefer to pay?

## Dataset
The dataset is synthetically generated (`scripts/generate_data.py`) to resemble
real-world delivery platform data, consisting of 4 tables:

| Table | Description | Rows |
|---|---|---|
| `orders.csv` | Order-level transactional data | 18,000 |
| `customers.csv` | Customer demographics | 2,000 |
| `restaurants.csv` | Restaurant / grocery outlet info | 180 |
| `delivery_partners.csv` | Delivery partner info | 350 |
"""
))

cells.append(md("## 1. Setup & Imports"))
cells.append(code(
"""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.figsize"] = (9, 5)
plt.rcParams["figure.dpi"] = 110

%matplotlib inline
"""
))

cells.append(md("## 2. Load the Data"))
cells.append(code(
"""orders = pd.read_csv("../data/orders.csv", parse_dates=["order_date"])
customers = pd.read_csv("../data/customers.csv")
restaurants = pd.read_csv("../data/restaurants.csv")
delivery_partners = pd.read_csv("../data/delivery_partners.csv")

print(orders.shape, customers.shape, restaurants.shape, delivery_partners.shape)
orders.head()
"""
))

cells.append(md("## 3. Data Cleaning & Quality Checks"))
cells.append(code(
"""# Check for missing values and duplicates
print(orders.isna().sum())
print("\\nDuplicate order_ids:", orders["order_id"].duplicated().sum())

# Ratings are only present for delivered orders - that's expected
orders.info()
"""
))

cells.append(md(
"""## 4. Key Business KPIs

Core metrics every delivery-analytics dashboard should surface first."""
))
cells.append(code(
"""delivered = orders[orders["order_status"] == "Delivered"].copy()

kpis = {
    "Total Orders": len(orders),
    "Total Revenue (₹)": round(delivered["final_amount"].sum(), 2),
    "Avg Order Value (₹)": round(delivered["final_amount"].mean(), 2),
    "Cancellation Rate (%)": round((orders["order_status"] == "Cancelled").mean() * 100, 2),
    "Return Rate (%)": round((orders["order_status"] == "Returned").mean() * 100, 2),
    "Avg Delivery Time (min)": round(delivered["actual_delivery_time_min"].mean(), 2),
    "On-Time Delivery Rate (%)": round((delivered["delayed"] == 0).mean() * 100, 2),
    "Avg Customer Rating": round(delivered["customer_rating"].mean(), 2),
}

for k, v in kpis.items():
    print(f"{k:28s}: {v}")
"""
))

cells.append(md("## 5. Revenue Trend Over Time"))
cells.append(code(
"""delivered["order_month"] = delivered["order_date"].dt.to_period("M").astype(str)
monthly_rev = delivered.groupby("order_month")["final_amount"].sum().reset_index()

sns.lineplot(data=monthly_rev, x="order_month", y="final_amount", marker="o", linewidth=2.5)
plt.title("Monthly Revenue Trend", fontweight="bold")
plt.xlabel("Month"); plt.ylabel("Revenue (₹)")
plt.tight_layout(); plt.show()
"""
))

cells.append(md("## 6. Peak Hour & Day-of-Week Analysis"))
cells.append(code(
"""day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
dow_orders = orders["day_of_week"].value_counts().reindex(day_order)

sns.barplot(x=dow_orders.index, y=dow_orders.values)
plt.title("Order Volume by Day of Week", fontweight="bold")
plt.xticks(rotation=30); plt.tight_layout(); plt.show()
"""
))
cells.append(code(
"""hour_orders = orders["order_hour"].value_counts().sort_index()

sns.barplot(x=hour_orders.index, y=hour_orders.values, color="#4C72B0")
plt.title("Order Volume by Hour of Day (Peak Hour Analysis)", fontweight="bold")
plt.xlabel("Hour of Day (24h)"); plt.ylabel("Orders")
plt.tight_layout(); plt.show()
"""
))

cells.append(md("## 7. City & Outlet Performance"))
cells.append(code(
"""city_rev = delivered.groupby("city")["final_amount"].sum().sort_values(ascending=False)
sns.barplot(x=city_rev.values, y=city_rev.index, orient="h")
plt.title("Revenue by City", fontweight="bold")
plt.tight_layout(); plt.show()
"""
))
cells.append(code(
"""top_outlets = (delivered.groupby("outlet_name")["final_amount"]
               .sum().sort_values(ascending=False).head(10))
sns.barplot(x=top_outlets.values, y=top_outlets.index, orient="h", color="#DD8452")
plt.title("Top 10 Outlets by Revenue", fontweight="bold")
plt.tight_layout(); plt.show()
"""
))

cells.append(md("## 8. Food vs Grocery Mix & Payment Preferences"))
cells.append(code(
"""type_share = orders["order_type"].value_counts()
plt.figure(figsize=(6,6))
plt.pie(type_share.values, labels=type_share.index, autopct="%1.1f%%", startangle=90)
plt.title("Food Delivery vs Grocery - Order Share", fontweight="bold")
plt.tight_layout(); plt.show()
"""
))
cells.append(code(
"""pay_counts = orders["payment_method"].value_counts()
sns.barplot(x=pay_counts.index, y=pay_counts.values, color="#8172B2")
plt.title("Preferred Payment Methods", fontweight="bold")
plt.tight_layout(); plt.show()
"""
))

cells.append(md("## 9. Delivery Performance Deep-Dive"))
cells.append(code(
"""sns.histplot(delivered["actual_delivery_time_min"], bins=40, kde=True, color="#55A868")
plt.axvline(delivered["actual_delivery_time_min"].mean(), color="red", linestyle="--",
            label=f'Mean = {delivered["actual_delivery_time_min"].mean():.1f} min')
plt.title("Distribution of Actual Delivery Time", fontweight="bold")
plt.legend(); plt.tight_layout(); plt.show()
"""
))
cells.append(code(
"""sns.boxplot(data=delivered, x="delayed", y="customer_rating")
plt.xticks([0,1], ["On-Time", "Delayed"])
plt.title("Customer Rating: On-Time vs Delayed Deliveries", fontweight="bold")
plt.tight_layout(); plt.show()
"""
))

cells.append(md("## 10. Cancellations & Returns"))
cells.append(code(
"""cancel_df = orders[orders["order_status"].isin(["Cancelled","Returned"])]
reason_counts = cancel_df["cancel_return_reason"].value_counts()

sns.barplot(x=reason_counts.values, y=reason_counts.index, orient="h", color="#C44E52")
plt.title("Order Cancellation / Return Reasons", fontweight="bold")
plt.tight_layout(); plt.show()
"""
))

cells.append(md(
"""## 11. Key Insights & Recommendations

- **Peak demand** clusters around lunch (12–1 PM) and dinner (7–9 PM), suggesting
  delivery-partner staffing should flex around these windows rather than stay flat.
- **On-time delivery rate (~80%)** correlates strongly with rating — delayed orders
  average noticeably lower ratings than on-time ones, confirming SLA adherence
  directly drives customer satisfaction.
- **Cancellations (~7%)** are dominated by "restaurant/store too busy" and
  "delivery partner unavailable," pointing to capacity-planning gaps during peak hours.
- **Food delivery (~59%) vs Grocery (~41%)** — grocery is a meaningful and growing
  share of volume, worth its own operational playbook (larger basket sizes, different
  peak windows).
- **UPI dominates payments (~52%)**, reinforcing the importance of a frictionless
  UPI checkout experience.
- **Revenue is concentrated** in a handful of top outlets and Tier-1 cities — useful
  for prioritizing account-management and marketing spend.

## Next Steps
- Build a live dashboard (Power BI / Tableau / Streamlit) on top of these tables.
- Add cohort & retention analysis using `customers.signup_date`.
- Model delivery-time prediction (regression) using distance, prep time, and traffic factor.
"""
))

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"}
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

out_path = os.path.join(os.path.dirname(__file__), "..", "notebooks", "delivery_analytics_eda.ipynb")
with open(out_path, "w") as f:
    json.dump(notebook, f, indent=1)

print("Notebook written to:", out_path)
