import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aventis Ops Risk Dashboard", layout="wide")

st.title("Aventis Finance – Operational Risk Command Center")
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Operational Snapshot",
    "🚨 Risk Alerts",
    "📐 Risk Scoring (FMEA)",
    "🧪 Data Protection",
    "📑 Governance"
])
with tab1:
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
st.markdown("---")
st.subheader("🚨 Risk Alerts & Early Warnings")

# Thresholds
LATE_THRESHOLD = 10       # %
DQI_THRESHOLD = 0.95
LATENCY_THRESHOLD = 15    # minutes
with tab2:
    # Risk Alerts & Early Warnings code

# Alert flags
alerts = []

if late_pct > LATE_THRESHOLD:
    alerts.append("Late Submission Risk: Clients missing T+1 deadline")

if dqi < DQI_THRESHOLD:
    alerts.append("Data Quality Risk: Schema drift or validation errors")

if avg_latency > LATENCY_THRESHOLD:
    alerts.append("Technology Risk: High ingestion latency detected")

# Display alerts
if alerts:
    for alert in alerts:
        st.error(alert)
else:
    st.success("All KRIs within acceptable limits")
st.markdown("---")
st.subheader("📊 FMEA Risk Scoring (RPN)")

st.write(
    "Score each risk dimension to quantify operational risk priority."
)
with tab3:
# FMEA sliders
severity = st.slider(
    "Severity (Impact on SLA / Regulatory Compliance)",
    min_value=1,
    max_value=10,
    value=8
)

occurrence = st.slider(
    "Occurrence (Frequency of the Issue)",
    min_value=1,
    max_value=10,
    value=7
)

detection = st.slider(
    "Detection (Ability to Detect Before SLA Breach)",
    min_value=1,
    max_value=10,
    value=6
)

# RPN calculation
rpn = severity * occurrence * detection

st.metric("Risk Priority Number (RPN)", rpn)

# Risk classification
if rpn >= 400:
    st.error("CRITICAL RISK – Immediate architectural intervention required")
elif rpn >= 200:
    st.warning("HIGH RISK – Automation and process controls needed")
elif rpn >= 100:
    st.info("MEDIUM RISK – Monitor closely")
else:
    st.success("LOW RISK – Acceptable operational risk")
st.markdown("---")
st.subheader("🧪 Quarantine Pattern – Data Flow Protection")
with tab4:
    # Quarantine pattern metrics and progress bar

# Quarantine calculations
total_records = df["records_total"].sum()
invalid_records = df["records_invalid"].sum()

quarantine_rate = invalid_records / total_records
processed_rate = 1 - quarantine_rate

# Display metrics
q1, q2 = st.columns(2)

with q1:
    st.metric(
        "Quarantined Records %",
        f"{quarantine_rate * 100:.2f}%"
    )

with q2:
    st.metric(
        "Safely Processed Records %",
        f"{processed_rate * 100:.2f}%"
    )
with tab5:
    # KRI → Compliance mapping table

# Visual indicator
st.write("Data Processing Health")

st.progress(processed_rate)

# Explanation
st.caption(
    "Invalid records are isolated in a quarantine queue, "
    "allowing valid data to reach DataHub without blocking the SLA."
)
st.markdown("---")
st.subheader("📑 Governance & Compliance Mapping (KRI → KCI)")

gov_data = {
    "Key Risk Indicator (KRI)": [
        "Late Submission %",
        "Data Quality Index (DQI)",
        "Average Pipeline Latency"
    ],
    "Operational Threshold": [
        "> 10%",
        "< 95%",
        "> 15 minutes"
    ],
    "Regulatory / Business Impact": [
        "T+3 SLA Breach & Financial Penalty",
        "Incorrect Credit Reporting & Audit Observation",
        "Operational Failure & Client Impact"
    ],
    "Current Status": [
        "BREACH" if late_pct > 10 else "OK",
        "BREACH" if dqi < 0.95 else "OK",
        "BREACH" if avg_latency > 15 else "OK"
    ]
}

gov_df = pd.DataFrame(gov_data)

st.table(gov_df)
