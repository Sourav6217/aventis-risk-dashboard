import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aventis Ops Risk Dashboard", layout="wide")

st.title("Aventis Finance – Operational Risk Command Center")

st.write("Upload daily feed status or use sample data")

# File upload
uploaded_file = st.file_uploader(
    "Upload Daily Feed Status (CSV)",
    type=["csv"]
)

# Load data
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully")
else:
    df = pd.read_csv("data/sample_daily_feed.csv")
    st.info("Using sample data")

# Display data
st.subheader("Daily Feed Snapshot")
st.dataframe(df)
st.markdown("---")
st.subheader("Executive Summary")

# KPI calculations
total_clients = len(df)

late_clients = df[df["received_day"] > 1]
late_pct = (len(late_clients) / total_clients) * 100

total_records = df["records_total"].sum()
invalid_records = df["records_invalid"].sum()
dqi = 1 - (invalid_records / total_records)

avg_latency = df["latency_minutes"].mean()

# KPI tiles
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("Total Clients", total_clients)

with k2:
    st.metric("Late Submission %", f"{late_pct:.2f}%")

with k3:
    st.metric("Data Quality Index (DQI)", f"{dqi:.3f}")

with k4:
    st.metric("Avg Latency (min)", f"{avg_latency:.1f}")
