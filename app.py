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
