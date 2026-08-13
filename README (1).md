# 🛵 Food & Grocery Delivery Analytics

An end-to-end data analytics project exploring operational and business performance
of a food & grocery quick-commerce platform (Swiggy / Zomato / Blinkit / Zepto style),
built using **Python, Pandas, Matplotlib, and Seaborn**.

---

## 📌 Problem Statement

Online food and grocery delivery platforms generate massive volumes of operational
data every single day — orders, delivery times, cancellations, ratings, and revenue.
Business teams need clear, data-backed answers to questions like:

- How is revenue trending month over month, and where is growth coming from?
- When do customers order the most (peak hours / peak days)?
- Which cities and outlets drive the most revenue?
- How reliable is delivery performance — what's our on-time delivery rate?
- Why do orders get cancelled or returned, and how does that affect customer ratings?
- What's the food vs. grocery order mix, and how do customers prefer to pay?

This project builds a complete analytics pipeline — from raw transactional data to
business insights — to answer exactly these questions.

---

## 🗂️ Project Structure

```
food-grocery-delivery-analytics/
│
├── data/                              # Raw datasets (CSV)
│   ├── orders.csv                     # 18,000 order-level transactions
│   ├── customers.csv                  # 2,000 customer profiles
│   ├── restaurants.csv                # 180 restaurant / grocery outlets
│   └── delivery_partners.csv          # 350 delivery partners
│
├── scripts/
│   ├── generate_data.py               # Generates the synthetic dataset
│   ├── analysis.py                    # Runs full EDA + saves charts
│   └── build_notebook.py              # Builds the Jupyter notebook
│
├── notebooks/
│   └── delivery_analytics_eda.ipynb   # Full exploratory analysis notebook
│
├── charts/                            # Exported visualizations (PNG)
├── kpi_summary.txt                    # Plain-text KPI summary
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📊 Dataset Overview

The dataset is synthetically generated to closely mirror real-world delivery
platform data (6 months of operations, Jan–Jun 2026), across 4 linked tables:

| Table | Description | Rows | Key Columns |
|---|---|---|---|
| `orders.csv` | Order-level transactions | 18,000 | order_id, order_datetime, order_type, order_value, final_amount, distance_km, delivery time, status, rating |
| `customers.csv` | Customer demographics | 2,000 | customer_id, city, age, gender, is_premium_member |
| `restaurants.csv` | Outlets (restaurants + grocery stores) | 180 | restaurant_id, outlet_type, category, avg_prep_time_min |
| `delivery_partners.csv` | Delivery fleet | 350 | partner_id, vehicle_type, experience_years |

> The generator (`scripts/generate_data.py`) uses realistic peak-hour weighting,
> gamma-distributed delivery distances, and rating logic tied to on-time
> performance — so patterns in the data reflect genuine delivery-ops dynamics
> rather than pure randomness.

---

## 🔑 Key KPIs (from this run)

| Metric | Value |
|---|---|
| Total Orders | 18,000 |
| Total Revenue | ₹93.4 Lakh (~₹9.34M) |
| Average Order Value | ₹574.6 |
| Cancellation Rate | 6.7% |
| Return Rate | 3.0% |
| Average Delivery Time | 32.6 minutes |
| On-Time Delivery Rate | 79.9% |
| Average Customer Rating | 4.22 / 5 |
| Food Delivery vs Grocery Split | 58.8% / 41.2% |
| Premium Member Share | 26.8% |

*(Full breakdown in [`kpi_summary.txt`](kpi_summary.txt))*

---

## 📈 Visual Insights

| | |
|---|---|
| ![Monthly Revenue](charts/01_monthly_revenue_trend.png) | ![Orders by Day](charts/02_orders_by_day_of_week.png) |
| ![Peak Hours](charts/03_orders_by_hour.png) | ![Revenue by City](charts/04_revenue_by_city.png) |
| ![Food vs Grocery](charts/05_food_vs_grocery_share.png) | ![Delivery Time](charts/06_delivery_time_distribution.png) |
| ![Cancellations](charts/07_cancellation_reasons.png) | ![Payment Methods](charts/08_payment_methods.png) |
| ![Rating vs Delay](charts/09_rating_vs_delay.png) | ![Top Outlets](charts/10_top_outlets_by_revenue.png) |

All 10 charts are saved individually in the [`charts/`](charts) folder.

---

## 💡 Key Insights

- **Peak demand** clusters sharply around lunch (12–1 PM) and dinner (7–9 PM) —
  staffing and delivery-partner allocation should flex around these windows.
- **On-time delivery strongly predicts satisfaction**: delayed orders receive
  noticeably lower ratings than on-time ones.
- **Cancellations (~7%)** are driven mainly by outlet overload and delivery-partner
  unavailability during peak hours — a capacity-planning problem, not a demand problem.
- **Grocery already makes up ~41% of orders**, and deserves its own operational
  playbook (larger baskets, different peak windows than food delivery).
- **UPI dominates payments (~52%)** — checkout experience should be UPI-first.
- **Revenue is concentrated** among a handful of top outlets and Tier-1 cities,
  useful for prioritizing marketing and account-management spend.

---

## 🛠️ Tech Stack

- **Python 3** — core language
- **Pandas / NumPy** — data generation, wrangling & aggregation
- **Matplotlib / Seaborn** — data visualization
- **Jupyter Notebook** — exploratory analysis & storytelling

---

## ▶️ How to Run This Project

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/food-grocery-delivery-analytics.git
   cd food-grocery-delivery-analytics
   ```

2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate the dataset**
   ```bash
   python scripts/generate_data.py
   ```

5. **Run the full analysis (saves charts to `charts/`)**
   ```bash
   python scripts/analysis.py
   ```

6. **Or explore interactively in Jupyter**
   ```bash
   jupyter notebook notebooks/delivery_analytics_eda.ipynb
   ```

---

## 🚀 Future Scope

- Build a live interactive dashboard (Power BI / Tableau / Streamlit).
- Add customer cohort & retention analysis using signup dates.
- Build a delivery-time prediction model (regression) using distance, prep
  time, and traffic conditions.
- Add a churn-prediction model for at-risk customers.

---

## 👤 Author

**Your Name Here**
📧 your.email@example.com
🔗 [LinkedIn](https://linkedin.com/in/your-profile) • [GitHub](https://github.com/your-username)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
