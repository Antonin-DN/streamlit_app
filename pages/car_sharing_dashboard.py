import streamlit as st
import pandas as pd

st.title("Car sharing Dashboard")
st.write("Bienvenu dans le Dashboard")

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

# ── 5. SIDEBAR – FILTRES ───────────────────────────────────────────────────────

st.sidebar.title("Filtres")

cars_brand = st.sidebar.multiselect(
    "Sélectionner une marque",
    options=trips_merged["brand"].unique(),
    default=trips_merged["brand"].unique()
)

trips_merged = trips_merged[trips_merged["brand"].isin(cars_brand)]

# ── 6. MÉTRIQUES BUSINESS ─────────────────────────────────────────────────────

total_trips    = len(trips_merged)
total_distance = trips_merged["distance"].sum()
top_car        = trips_merged.groupby("model")["revenue"].sum().idxmax()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Trips", value=total_trips)
with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car)
with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")

# ── 7. APERÇU DU DATAFRAME ────────────────────────────────────────────────────

st.subheader("Aperçu des données")
st.write(trips_merged.head())

