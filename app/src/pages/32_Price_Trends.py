import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'analyst':
    st.switch_page('Home.py')

st.title("Price Trend Explorer")
st.write("View historical pricing trends for items across semesters.")
st.divider()

# TODO: replace with GET request when API is ready
# import requests
# response = requests.get('http://api:4000/price-history', params={'item': selected_item})
# history = response.json()

col1, col2, col3 = st.columns(3)
with col1:
    selected_item = st.selectbox(
    "Item / Category",
    ["Engineering Mechanics: Dynamics", "Organic Chemistry", "TI-84 Plus Graphing Calculator"]
)
with col2:
    time_range = st.selectbox("Time Range", ["Last 2 semesters", "Last 4 semesters", "All time"])
with col3:
    condition_filter = st.selectbox("Condition", ["All conditions", "Unused", "Lightly Used", "Used"])

import requests

r = requests.get(
    'http://api:4000/analytics/price-trends',
    params={'course_id': selected_item}
)
history = r.json().get("points", []) if r.status_code == 200 else []
df = pd.DataFrame(history) if history else pd.DataFrame()

if time_range == "Last 2 semesters":
    df = df.tail(2)
elif time_range == "Last 4 semesters":
    df = df.tail(4)

st.divider()

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Avg Sale Price", f"${df['Avg Sale Price'].mean():.0f}")
with m2:
    st.metric("Price Low", f"${df['Avg Sale Price'].min():.0f}")
with m3:
    st.metric("Price High", f"${df['Avg Sale Price'].max():.0f}")
with m4:
    st.metric("Total Semesters", len(df))

st.divider()
st.subheader("Sale Price by Semester")
st.line_chart(df.set_index("Semester"))

st.divider()
st.subheader("Recent Sales Data")
st.dataframe(df, use_container_width=True)

if st.button("Export as CSV", type="primary"):
    r = requests.post('http://api:4000/analytics/reports', json={
        "analyst_id": st.session_state['user_id'],
        "filter_params": f"item={selected_item}",
        "format": "CSV"
    })
    if r.status_code == 202:
        csv = df.to_csv(index=False)
        st.download_button(
            "Download CSV",
            data=csv,
            file_name="price_trends.csv",
            mime="text/csv"
        )