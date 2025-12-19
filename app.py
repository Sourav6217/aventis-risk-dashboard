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

# ---------------- TAB 1 ----------------
with tab1:
    st.write("Upload daily feed status or use sample data")

    uploaded_file = st.file_uploader(
        "Upload Daily Feed Status (CSV)",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully")
    else:
        df = pd.read_csv("data/sample_daily_feed.csv")
        st.info("Using sample data")
    # Load client historical data for CRI
client_history_df = pd.read_csv("data/client_weekly_history.csv")

# Compute CRI
client_cri_df = compute_cri(client_history_df)

    st.subheader("Daily Feed Snapshot")
    st.dataframe(df)

    st.markdown("---")
    st.subheader("Executive Summary")

    total_clients = len(df)
    late_pct = (len(df[df["received_day"] > 1]) / total_clients) * 100
    dqi = 1 - (df["records_invalid"].sum() / df["records_total"].sum())
    avg_latency = df["latency_minutes"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Clients", total_clients)
    c2.metric("Late Submission %", f"{late_pct:.2f}%")
    c3.metric("DQI", f"{dqi:.3f}")
    c4.metric("Avg Latency (min)", f"{avg_latency:.1f}")

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("🚨 Risk Alerts & Early Warnings")

    alerts = []

    if late_pct > 10:
        alerts.append("Late Submission Risk: Clients missing T+1 deadline")
    if dqi < 0.95:
        alerts.append("Data Quality Risk: Schema drift detected")
    if avg_latency > 15:
        alerts.append("Technology Risk: High ingestion latency")

    if alerts:
        for a in alerts:
            st.error(a)
    else:
        st.success("All KRIs within acceptable limits")

# ---------------- TAB 3 ----------------
with tab3:
    st.subheader("📊 FMEA Risk Scoring")

    severity = st.slider("Severity", 1, 10, 8)
    occurrence = st.slider("Occurrence", 1, 10, 7)
    detection = st.slider("Detection", 1, 10, 6)

    rpn = severity * occurrence * detection
    st.metric("Risk Priority Number (RPN)", rpn)

    if rpn >= 400:
        st.error("CRITICAL RISK")
    elif rpn >= 200:
        st.warning("HIGH RISK")
    elif rpn >= 100:
        st.info("MEDIUM RISK")
    else:
        st.success("LOW RISK")
    st.markdown("---")
    st.subheader("🔮 Client Reliability Index (CRI) Simulator")

    # Client selector
    selected_client = st.selectbox(
        "Select Client ID",
        sorted(client_cri_df["client_id"].unique())
    )

    # Filter selected client data
    client_data = client_cri_df[
        client_cri_df["client_id"] == selected_client
    ].sort_values(["year", "month", "week_of_month"])

    # Display weekly CRI table
    st.write("Weekly Client Reliability Overview")
    st.dataframe(
        client_data[
            [
                "year",
                "month",
                "week_of_month",
                "CRI",
                "Risk_Category"
            ]
        ]
    )

    # Highlight high-risk weeks
    high_risk_weeks = client_data[
        client_data["Risk_Category"] == "High Risk"
    ]

    if not high_risk_weeks.empty:
        st.warning(
            f"⚠️ High Risk Weeks Detected: "
            f"{len(high_risk_weeks)} out of "
            f"{len(client_data)} weeks"
        )
    else:
        st.success("No high-risk weeks detected for this client")

    
# ---------------- TAB 4 ----------------
with tab4:
    st.subheader("🧪 Quarantine Pattern – Data Flow Protection")

    quarantine_rate = df["records_invalid"].sum() / df["records_total"].sum()
    processed_rate = 1 - quarantine_rate

    c1, c2 = st.columns(2)
    c1.metric("Quarantined Records %", f"{quarantine_rate*100:.2f}%")
    c2.metric("Safely Processed %", f"{processed_rate*100:.2f}%")

    st.progress(processed_rate)

# ---------------- TAB 5 ----------------
with tab5:
    st.subheader("📑 Governance & Compliance Mapping")

    gov_df = pd.DataFrame({
        "KRI": ["Late Submission %", "DQI", "Latency"],
        "Threshold": [">10%", "<95%", ">15 min"],
        "Status": [
            "BREACH" if late_pct > 10 else "OK",
            "BREACH" if dqi < 0.95 else "OK",
            "BREACH" if avg_latency > 15 else "OK"
        ]
    })

    st.table(gov_df)
