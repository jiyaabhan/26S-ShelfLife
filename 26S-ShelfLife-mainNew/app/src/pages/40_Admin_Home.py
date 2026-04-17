import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'admin':
    st.switch_page('Home.py')

st.title(f"Welcome, {st.session_state['first_name']}! 👋")
st.write("Manage the ShelfLife platform.")
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📚 Course Catalog", use_container_width=True):
        st.switch_page('pages/41_Course_Catalog.py')
with col2:
    if st.button("🚩 Flagged Listings", use_container_width=True):
        st.switch_page('pages/42_Flagged_Listings.py')
with col3:
    if st.button("👥 User Accounts", use_container_width=True):
        st.switch_page('pages/43_User_Accounts.py')