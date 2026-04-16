import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'analyst':
    st.switch_page('Home.py')

st.title(f"Welcome, {st.session_state['first_name']}! 👋")
st.write("Monitor platform health and marketplace trends.")
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🌐 Platform Overview", use_container_width=True):
        st.switch_page('pages/31_Platform_Overview.py')
with col2:
    if st.button("📈 Price Trends", use_container_width=True):
        st.switch_page('pages/32_Price_Trends.py')
with col3:
    if st.button("🏪 Seller Activity", use_container_width=True):
        st.switch_page('pages/33_Seller_Activity.py')