import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'analyst':
    st.switch_page('Home.py')

st.title("Platform Overview")
st.caption("Fall 2025 — ShelfLife Marketplace Health")
st.divider()

# TODO: replace with GET request when API is ready
# import requests
# response = requests.get('http://api:4000/metrics/latest')
# metrics = response.json()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Active Listings", "1,284", delta="12% vs last sem")
with col2:
    st.metric("Completed Transactions", "847", delta="8% vs last sem")
with col3:
    st.metric("Active Users This Week", "562", delta="5% vs last week")
with col4:
    st.metric("Avg Days to Sale", "4.2", delta="-0.3 vs last sem")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Transaction Volume Over Time")
    transaction_data = pd.DataFrame({
        "Month": ["Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
        "Transactions": [45, 210, 180, 95, 60, 320, 290, 188]
    })
    st.bar_chart(transaction_data.set_index("Month"))

with col2:
    st.subheader("Most Active Departments")
    dept_data = pd.DataFrame({
        "Department": ["CS", "MECH", "BIOL", "MATH", "ARTD"],
        "Listings": [310, 248, 190, 152, 97]
    })
    st.bar_chart(dept_data.set_index("Department"))

st.divider()
st.subheader("Top-Searched Items with Low Supply")
st.caption("Items where search demand significantly exceeds available listings")

demand_data = {
    "Item": ["Organic Chem Lab Manual", "Drawing Toolkit (arch)", "Microeconomics Textbook", "TI-84 Calculator"],
    "Course": ["CHEM 2313", "ARTD 1200", "ECON 1115", "MATH 1341"],
    "Searches": [88, 64, 52, 44],
    "Active Listings": [3, 4, 6, 12],
    "Ratio": ["29:1", "16:1", "8:1", "3:1"],
    "Status": ["HIGH DEMAND", "HIGH DEMAND", "FLAGGED", "OK"]
}

df = pd.DataFrame(demand_data)

def color_status(val):
    if val == "HIGH DEMAND":
        return "background-color: #ffcccc"
    elif val == "FLAGGED":
        return "background-color: #fff3cc"
    return ""

st.dataframe(df.style.applymap(color_status, subset=["Status"]), use_container_width=True)

st.divider()
col1, col2 = st.columns(2)
with col1:
    st.subheader("Filter by Semester")
    st.selectbox("Semester", ["Fall 2025", "Spring 2025", "Fall 2024", "Spring 2024"])
with col2:
    st.subheader("Filter by College")
    st.selectbox("College", ["All", "Khoury College", "College of Engineering", "College of Science"])