import streamlit as st
import pandas as pd

# ── 1. CHARGEMENT DES DONNÉES ──────────────────────────────────────────────────

@st.cache_data
def load_data():
    trips  = pd.read_csv("datasets/trips.csv")
    cars   = pd.read_csv("datasets/cars.csv")
    cities = pd.read_csv("datasets/cities.csv")
    return trips, cars, cities

trips, cars, cities = load_data()

# ── 2. JOINTURES ───────────────────────────────────────────────────────────────

trips_merged = trips.merge(cars, left_on="car_id", right_on="id", suffixes=("", "_car"))
trips_merged = trips_merged.merge(cities, left_on="city_id", right_on="city_id", suffixes=("", "_city"))

# ── 3. NETTOYAGE ───────────────────────────────────────────────────────────────

trips_merged = trips_merged.drop(
    columns=["id_car", "city_id", "id_customer", "id"],
    errors="ignore"
)

# ── 4. FORMAT DES DATES ────────────────────────────────────────────────────────

trips_merged["pickup_date"]  = pd.to_datetime(trips_merged["pickup_time"]).dt.date
trips_merged["dropoff_date"] = pd.to_datetime(trips_merged["dropoff_time"]).dt.date