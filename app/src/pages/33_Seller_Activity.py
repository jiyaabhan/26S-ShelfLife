import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'analyst':
    st.switch_page('Home.py')

st.title("Seller Activity Report")
st.write("Analyze how efficiently sellers are connecting with buyers.")
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Time to Sale", "4.2 days")
with col2:
    st.metric("Listing Turnover Rate", "66%")
with col3:
    st.metric("Total Active Sellers", "312")

st.divider()

r = requests.get('http://api:4000/analytics/seller-activity')
sellers = r.json().get("sellers", []) if r.status_code == 200 else []
df = pd.DataFrame(sellers) if sellers else pd.DataFrame()

st.subheader("Seller Performance Table")

col1, col2 = st.columns(2)
with col1:
    dept_filter = st.selectbox(
        "Filter by College",
        ["All", "Khoury College", "College of Engineering", "College of Science"]
    )
with col2:
    sort_col = st.selectbox(
        "Sort by",
        ["Total Listings", "Completed Sales", "Avg Days to Sale", "Avg Rating"]
    )

if not df.empty:
    if dept_filter != "All":
        df = df[df["college"] == dept_filter]

    sort_map = {
        "Total Listings": "total_listings",
        "Completed Sales": "completed_sales",
        "Avg Days to Sale": "avg_days_to_sale",
        "Avg Rating": "avg_rating"
    }
    df = df.sort_values(by=sort_map[sort_col], ascending=False)

st.dataframe(df, use_container_width=True)

st.divider()
st.subheader("Days to Sale Distribution")
days_data = pd.DataFrame({
    "Days to Sale": ["1-2 days", "3-5 days", "6-10 days", "11-20 days", "20+ days"],
    "Number of Listings": [124, 310, 248, 112, 53]
})
st.bar_chart(days_data.set_index("Days to Sale"))

st.divider()
if st.button("Export Seller Report", type="primary"):
    requests.post('http://api:4000/analytics/reports', json={
        "analyst_id": st.session_state['user_id'],
        "filter_params": "report_type=seller_activity",
        "format": "CSV"
    })
    csv = df.to_csv(index=False)
    st.download_button(
        "Download CSV",
        data=csv,
        file_name="seller_activity.csv",
        mime="text/csv"
    )