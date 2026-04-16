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

price_data = {
    "Engineering Mechanics: Dynamics": [
        {"Semester": "S'23", "Avg Sale Price": 165, "List Price": 175},
        {"Semester": "F'23", "Avg Sale Price": 183, "List Price": 190},
        {"Semester": "S'24", "Avg Sale Price": 193, "List Price": 200},
        {"Semester": "F'24", "Avg Sale Price": 210, "List Price": 215},
        {"Semester": "S'25", "Avg Sale Price": 215, "List Price": 225},
    ],
    "Organic Chemistry": [
        {"Semester": "S'23", "Avg Sale Price": 70, "List Price": 80},
        {"Semester": "F'23", "Avg Sale Price": 75, "List Price": 85},
        {"Semester": "S'24", "Avg Sale Price": 80, "List Price": 90},
        {"Semester": "F'24", "Avg Sale Price": 85, "List Price": 95},
        {"Semester": "S'25", "Avg Sale Price": 90, "List Price": 100},
    ],
    "TI-84 Plus Graphing Calculator": [
        {"Semester": "S'23", "Avg Sale Price": 45, "List Price": 55},
        {"Semester": "F'23", "Avg Sale Price": 50, "List Price": 60},
        {"Semester": "S'24", "Avg Sale Price": 55, "List Price": 65},
        {"Semester": "F'24", "Avg Sale Price": 60, "List Price": 68},
        {"Semester": "S'25", "Avg Sale Price": 65, "List Price": 70},
    ],
}

col1, col2, col3 = st.columns(3)
with col1:
    selected_item = st.selectbox("Item / Category", list(price_data.keys()))
with col2:
    time_range = st.selectbox("Time Range", ["Last 2 semesters", "Last 4 semesters", "All time"])
with col3:
    condition_filter = st.selectbox("Condition", ["All conditions", "Unused", "Lightly Used", "Used"])

df = pd.DataFrame(price_data[selected_item])

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

st.divider()
if st.button("Export as CSV", type="primary"):
    # TODO: POST request to generate report when API is ready
    # requests.post('http://api:4000/reports', json={
    #     "analyst_id": st.session_state['user_id'],
    #     "filter_params": f"item={selected_item}",
    #     "export_format": "CSV"
    # })
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name=f"price_trends_{selected_item.replace(' ', '_')}.csv",
        mime="text/csv"
    )