"""
generate_data.py
-----------------
Generates a realistic synthetic dataset for a Food & Grocery Delivery
Analytics project (similar in spirit to Swiggy / Zomato / Blinkit / Zepto
style operational data).

Run:
    python scripts/generate_data.py

Outputs (into ../data/):
    customers.csv
    restaurants.csv
    delivery_partners.csv
    orders.csv
"""

import numpy as np
import pandas as pd
import os
import random
from datetime import datetime, timedelta

# ----------------------------------------------------------------------
# Reproducibility
# ----------------------------------------------------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# Reference lists
# ----------------------------------------------------------------------
CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Pune", "Hyderabad",
    "Chennai", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"
]

CITY_TIER = {
    "Mumbai": "Tier 1", "Delhi": "Tier 1", "Bengaluru": "Tier 1",
    "Pune": "Tier 1", "Hyderabad": "Tier 1", "Chennai": "Tier 1",
    "Kolkata": "Tier 1", "Ahmedabad": "Tier 2", "Jaipur": "Tier 2",
    "Lucknow": "Tier 2",
}

FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh",
    "Krishna", "Ishaan", "Rohan", "Ananya", "Diya", "Saanvi", "Aadhya",
    "Kiara", "Myra", "Anika", "Navya", "Riya", "Priya", "Rahul", "Amit",
    "Sneha", "Pooja", "Karan", "Neha", "Vikram", "Sanjay", "Meera",
    "Kavya"
]
LAST_NAMES = [
    "Sharma", "Verma", "Patel", "Gupta", "Kumar", "Singh", "Rao",
    "Reddy", "Nair", "Iyer", "Mehta", "Joshi", "Desai", "Chatterjee",
    "Das", "Kapoor", "Malhotra", "Agarwal", "Bansal", "Pillai"
]

ORDER_TYPES = ["Food Delivery", "Grocery"]

FOOD_CUISINES = [
    "North Indian", "South Indian", "Chinese", "Italian", "Fast Food",
    "Biryani", "Street Food", "Desserts", "Beverages", "Bakery"
]
GROCERY_CATEGORIES = [
    "Fruits & Vegetables", "Dairy & Eggs", "Snacks", "Staples",
    "Beverages", "Personal Care", "Household Essentials", "Bakery"
]

RESTAURANT_NAME_PREFIX = [
    "Spice", "Royal", "Urban", "The", "Green", "Tasty", "Fresh",
    "Golden", "Punjab", "South", "Metro", "City", "Sunrise", "Village"
]
RESTAURANT_NAME_SUFFIX = [
    "Kitchen", "Bites", "Grill", "Dhaba", "Cafe", "Corner", "Express",
    "House", "Treats", "Foods", "Mart", "Store", "Basket", "Bazaar"
]

PAYMENT_METHODS = ["UPI", "Credit/Debit Card", "Cash on Delivery", "Wallet"]
PAYMENT_WEIGHTS = [0.52, 0.23, 0.13, 0.12]

VEHICLES = ["Bike", "Scooter", "Bicycle", "E-Vehicle"]

STATUS_OPTIONS = ["Delivered", "Cancelled", "Returned"]
STATUS_WEIGHTS = [0.90, 0.07, 0.03]

CANCEL_REASONS = [
    "Customer changed mind", "Restaurant/store too busy",
    "Delivery partner unavailable", "Item out of stock",
    "Address issue", "Payment failure"
]

# ----------------------------------------------------------------------
# 1. Customers
# ----------------------------------------------------------------------
N_CUSTOMERS = 2000
customers = pd.DataFrame({
    "customer_id": [f"CUST{str(i).zfill(5)}" for i in range(1, N_CUSTOMERS + 1)],
    "customer_name": [f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}" for _ in range(N_CUSTOMERS)],
    "city": np.random.choice(CITIES, N_CUSTOMERS, p=[0.16, 0.15, 0.14, 0.10, 0.10, 0.09, 0.08, 0.06, 0.06, 0.06]),
    "age": np.random.randint(18, 55, N_CUSTOMERS),
    "gender": np.random.choice(["Male", "Female", "Other"], N_CUSTOMERS, p=[0.53, 0.45, 0.02]),
    "signup_date": [
        (datetime(2023, 1, 1) + timedelta(days=int(np.random.randint(0, 900)))).strftime("%Y-%m-%d")
        for _ in range(N_CUSTOMERS)
    ],
    "is_premium_member": np.random.choice([1, 0], N_CUSTOMERS, p=[0.28, 0.72]),
})
customers["city_tier"] = customers["city"].map(CITY_TIER)

# ----------------------------------------------------------------------
# 2. Restaurants / Grocery Stores
# ----------------------------------------------------------------------
N_PARTNERS_OUTLETS = 180
restaurants = pd.DataFrame({
    "restaurant_id": [f"OUT{str(i).zfill(4)}" for i in range(1, N_PARTNERS_OUTLETS + 1)],
})
restaurants["outlet_type"] = np.random.choice(ORDER_TYPES, N_PARTNERS_OUTLETS, p=[0.65, 0.35])
restaurants["outlet_name"] = [
    f"{random.choice(RESTAURANT_NAME_PREFIX)} {random.choice(RESTAURANT_NAME_SUFFIX)}"
    for _ in range(N_PARTNERS_OUTLETS)
]
restaurants["city"] = np.random.choice(CITIES, N_PARTNERS_OUTLETS)
restaurants["primary_category"] = restaurants["outlet_type"].apply(
    lambda t: random.choice(FOOD_CUISINES) if t == "Food Delivery" else random.choice(GROCERY_CATEGORIES)
)
restaurants["avg_prep_time_min"] = np.where(
    restaurants["outlet_type"] == "Food Delivery",
    np.random.randint(10, 35, N_PARTNERS_OUTLETS),
    np.random.randint(5, 15, N_PARTNERS_OUTLETS),
)
restaurants["partner_since"] = [
    (datetime(2022, 6, 1) + timedelta(days=int(np.random.randint(0, 1000)))).strftime("%Y-%m-%d")
    for _ in range(N_PARTNERS_OUTLETS)
]

# ----------------------------------------------------------------------
# 3. Delivery Partners
# ----------------------------------------------------------------------
N_DELIVERY_PARTNERS = 350
delivery_partners = pd.DataFrame({
    "partner_id": [f"DP{str(i).zfill(4)}" for i in range(1, N_DELIVERY_PARTNERS + 1)],
    "partner_name": [f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}" for _ in range(N_DELIVERY_PARTNERS)],
    "city": np.random.choice(CITIES, N_DELIVERY_PARTNERS),
    "vehicle_type": np.random.choice(VEHICLES, N_DELIVERY_PARTNERS, p=[0.45, 0.30, 0.15, 0.10]),
    "joining_date": [
        (datetime(2022, 1, 1) + timedelta(days=int(np.random.randint(0, 1300)))).strftime("%Y-%m-%d")
        for _ in range(N_DELIVERY_PARTNERS)
    ],
    "experience_years": np.round(np.random.uniform(0.1, 5, N_DELIVERY_PARTNERS), 1),
})

# ----------------------------------------------------------------------
# 4. Orders (main fact table)
# ----------------------------------------------------------------------
N_ORDERS = 18000
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime(2026, 6, 30)
date_range_days = (END_DATE - START_DATE).days

order_ids = [f"ORD{str(i).zfill(6)}" for i in range(1, N_ORDERS + 1)]

# Pick random customers & outlets, keeping city consistent between customer & outlet most of the time
cust_idx = np.random.randint(0, N_CUSTOMERS, N_ORDERS)
chosen_customers = customers.iloc[cust_idx].reset_index(drop=True)

rest_idx = np.random.randint(0, N_PARTNERS_OUTLETS, N_ORDERS)
chosen_outlets = restaurants.iloc[rest_idx].reset_index(drop=True)

dp_idx = np.random.randint(0, N_DELIVERY_PARTNERS, N_ORDERS)
chosen_partners = delivery_partners.iloc[dp_idx].reset_index(drop=True)

# Order timestamps with realistic peak-hour weighting (lunch & dinner peaks)
hour_weights = np.array([
    0.5, 0.3, 0.2, 0.2, 0.3, 0.5, 1.0, 1.5, 2.0, 2.5,   # 0-9
    3.5, 5.5, 7.0, 6.0, 3.5, 2.5, 2.5, 3.0, 5.5, 7.5,     # 10-19
    8.5, 6.5, 3.5, 1.5                                    # 20-23
])
hour_weights = hour_weights / hour_weights.sum()

order_days = np.random.randint(0, date_range_days + 1, N_ORDERS)
order_hours = np.random.choice(range(24), N_ORDERS, p=hour_weights)
order_minutes = np.random.randint(0, 60, N_ORDERS)

order_datetimes = [
    START_DATE + timedelta(days=int(d), hours=int(h), minutes=int(m))
    for d, h, m in zip(order_days, order_hours, order_minutes)
]

order_type = chosen_outlets["outlet_type"].values
items_count = np.where(
    order_type == "Food Delivery",
    np.random.randint(1, 6, N_ORDERS),
    np.random.randint(2, 20, N_ORDERS),
)

base_item_price = np.where(order_type == "Food Delivery",
                            np.random.uniform(80, 250, N_ORDERS),
                            np.random.uniform(20, 120, N_ORDERS))
order_value = np.round(items_count * base_item_price * np.random.uniform(0.85, 1.15, N_ORDERS), 2)

delivery_fee = np.round(np.where(order_value > 500, 0, np.random.uniform(15, 45, N_ORDERS)), 2)
discount = np.round(order_value * np.random.choice([0, 0.05, 0.10, 0.15, 0.20], N_ORDERS,
                                                     p=[0.35, 0.25, 0.20, 0.12, 0.08]), 2)

distance_km = np.round(np.random.gamma(2.2, 1.4, N_ORDERS).clip(0.5, 18), 2)
traffic_factor = np.random.uniform(0.9, 1.6, N_ORDERS)
prep_time = chosen_outlets["avg_prep_time_min"].values + np.random.randint(-3, 8, N_ORDERS)
travel_time = distance_km * np.random.uniform(2.5, 4.5, N_ORDERS) * traffic_factor
delivery_time_min = np.round(prep_time + travel_time, 1).clip(8, 120)
promised_time_min = np.round(prep_time * 1.1 + distance_km * 3.2, 1).clip(15, 90)

status = np.random.choice(STATUS_OPTIONS, N_ORDERS, p=STATUS_WEIGHTS)
cancel_reason = [
    random.choice(CANCEL_REASONS) if s == "Cancelled" else ("Quality/Wrong item" if s == "Returned" else None)
    for s in status
]

# Rating: correlated with on-time delivery
on_time = delivery_time_min <= promised_time_min * 1.15
rating = np.where(
    status != "Delivered", np.nan,
    np.clip(np.round(np.random.normal(np.where(on_time, 4.5, 3.4), 0.6, N_ORDERS), 1), 1, 5)
)

payment_method = np.random.choice(PAYMENT_METHODS, N_ORDERS, p=PAYMENT_WEIGHTS)
is_peak_hour = pd.Series(order_hours).isin([12, 13, 19, 20, 21]).astype(int).values

orders = pd.DataFrame({
    "order_id": order_ids,
    "order_datetime": [d.strftime("%Y-%m-%d %H:%M:%S") for d in order_datetimes],
    "order_date": [d.strftime("%Y-%m-%d") for d in order_datetimes],
    "order_hour": order_hours,
    "day_of_week": [d.strftime("%A") for d in order_datetimes],
    "is_peak_hour": is_peak_hour,
    "customer_id": chosen_customers["customer_id"].values,
    "city": chosen_customers["city"].values,
    "restaurant_id": chosen_outlets["restaurant_id"].values,
    "outlet_name": chosen_outlets["outlet_name"].values,
    "order_type": order_type,
    "category": chosen_outlets["primary_category"].values,
    "partner_id": chosen_partners["partner_id"].values,
    "vehicle_type": chosen_partners["vehicle_type"].values,
    "items_count": items_count,
    "order_value": order_value,
    "delivery_fee": delivery_fee,
    "discount_applied": discount,
    "final_amount": np.round(order_value + delivery_fee - discount, 2),
    "distance_km": distance_km,
    "promised_delivery_time_min": promised_time_min,
    "actual_delivery_time_min": delivery_time_min,
    "delayed": (delivery_time_min > promised_time_min * 1.15).astype(int),
    "payment_method": payment_method,
    "order_status": status,
    "cancel_return_reason": cancel_reason,
    "customer_rating": rating,
})

# ----------------------------------------------------------------------
# Save all files
# ----------------------------------------------------------------------
customers.to_csv(os.path.join(OUT_DIR, "customers.csv"), index=False)
restaurants.to_csv(os.path.join(OUT_DIR, "restaurants.csv"), index=False)
delivery_partners.to_csv(os.path.join(OUT_DIR, "delivery_partners.csv"), index=False)
orders.to_csv(os.path.join(OUT_DIR, "orders.csv"), index=False)

print("Dataset generated successfully:")
print(f"  customers.csv          -> {customers.shape}")
print(f"  restaurants.csv        -> {restaurants.shape}")
print(f"  delivery_partners.csv  -> {delivery_partners.shape}")
print(f"  orders.csv              -> {orders.shape}")
