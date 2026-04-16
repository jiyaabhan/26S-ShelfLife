import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'analyst':
    st.switch_page('Home.py')

st.title("Seller Activity Report")
st.write("Analyze how efficiently sellers are connecting with buyers.")
st.divider()

# TODO: replace with GET request when API is ready
# import requests
# response = requests.get('http://api:4000/analytics/seller-activity')
# data = response.json()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg Time to Sale", "4.2 days")
with col2:
    st.metric("Listing Turnover Rate", "66%")
with col3:
    st.metric("Total Active Sellers", "312")

st.divider()

seller_data = {
    "Seller": ["Maya T.", "Priya N.", "Alex M.", "Jordan K.", "Sam R.", "Dana L."],
    "Total Listings": [7, 4, 9, 3, 6, 2],
    "Completed Sales": [4, 3, 7, 1, 4, 2],
    "Avg Days to Sale": [3.2, 5.1, 2.8, 9.4, 4.7, 1.5],
    "Avg Rating": [4.8, 4.5, 4.2, 3.9, 4.6, 5.0],
    "Turnover Rate": ["57%", "75%", "78%", "33%", "67%", "100%"]
}

df = pd.DataFrame(seller_data)

st.subheader("Seller Performance Table")

col1, col2 = st.columns(2)
with col1:
    dept_filter = st.selectbox("Filter by College", ["All", "Khoury College", "College of Engineering", "College of Science"])
with col2:
    sort_col = st.selectbox("Sort by", ["Total Listings", "Completed Sales", "Avg Days to Sale", "Avg Rating"])

df = df.sort_values(by=sort_col, ascending=False)
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
    # TODO: POST request to generate report when API is ready
    # requests.post('http://api:4000/reports', json={
    #     "analyst_id": st.session_state['user_id'],
    #     "filter_params": "report_type=seller_activity",
    #     "export_format": "CSV"
    # })
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="seller_activity_report.csv",
        mime="text/csv"
    )