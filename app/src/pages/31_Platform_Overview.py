import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'analyst':
    st.switch_page('Home.py')

st.title("Platform Overview")
st.caption("ShelfLife Marketplace Health")
st.divider()

try:
    r = requests.get('http://api:4000/analytics/metrics/latest')
    data = r.json() if r.status_code == 200 else []
    metrics = {}
    if isinstance(data, list) and len(data) > 0:
        keys = ["metric_id", "active_users", "total_listings", "total_transactions", "recorded_at"]
        metrics = dict(zip(keys, data))
except Exception:
    metrics = {}

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Active Listings", metrics.get("total_listings", "N/A"))
with col2:
    st.metric("Completed Transactions", metrics.get("total_transactions", "N/A"))
with col3:
    st.metric("Active Users This Week", metrics.get("active_users", "N/A"))

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Transaction Volume Over Time")
    try:
        r2 = requests.get('http://api:4000/analytics/transactions/volume')
        vol_data = r2.json() if r2.status_code == 200 else {}
        vol = vol_data.get("volume", []) if isinstance(vol_data, dict) else []
        if vol:
            df_vol = pd.DataFrame(vol)
            st.bar_chart(df_vol.set_index("month"))
        else:
            st.info("No transaction data available.")
    except Exception:
        st.info("No transaction data available.")

with col2:
    st.subheader("Most Active Departments")
    try:
        r3 = requests.get('http://api:4000/analytics/departments/activity')
        dept_data = r3.json() if r3.status_code == 200 else {}
        depts = dept_data.get("departments", []) if isinstance(dept_data, dict) else []
        if depts:
            df_dept = pd.DataFrame(depts)
            st.bar_chart(df_dept.set_index("dept_name"))
        else:
            st.info("No department data available.")
    except Exception:
        st.info("No department data available.")

st.divider()
st.subheader("Top-Searched Items with Low Supply")
st.caption("Items where search demand significantly exceeds available listings")

try:
    r4 = requests.get('http://api:4000/analytics/demand-gaps')
    gaps_data = r4.json() if r4.status_code == 200 else {}
    gaps = gaps_data.get("gaps", []) if isinstance(gaps_data, dict) else []
    if gaps:
        df = pd.DataFrame(gaps)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No demand gap data available.")
except Exception:
    st.info("No demand gap data available.")

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.subheader("Filter by Semester")
    st.selectbox("Semester", ["Fall 2025", "Spring 2025", "Fall 2024", "Spring 2024"])
with col2:
    st.subheader("Filter by College")
    st.selectbox("College", ["All", "Khoury College", "College of Engineering", "College of Science"])