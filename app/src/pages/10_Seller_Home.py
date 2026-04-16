import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'seller':
    st.switch_page('Home.py')

st.title(f"Welcome, {st.session_state['first_name']}! 👋")
st.write("What would you like to do today?")
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("➕ Create a Listing", use_container_width=True):
        st.switch_page('pages/11_Create_Listing.py')
with col2:
    if st.button("📋 My Listings", use_container_width=True):
        st.switch_page('pages/12_My_Listings.py')
with col3:
    if st.button("⭐ My Profile", use_container_width=True):
        st.switch_page('pages/13_Seller_Profile.py')