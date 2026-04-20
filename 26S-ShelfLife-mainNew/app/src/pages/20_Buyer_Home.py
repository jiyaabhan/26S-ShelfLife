import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'buyer':
    st.switch_page('Home.py')

st.title(f"Welcome, {st.session_state['first_name']}! 👋")
st.write("Find course materials for less.")
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔍 Search by Course", use_container_width=True):
        st.switch_page('pages/21_Course_Search.py')
with col2:
    if st.button("🏷️ Browse Listings", use_container_width=True):
        st.switch_page('pages/22_Item_Detail.py')
with col3:
    if st.button("❤️ My Wishlist", use_container_width=True):
        st.switch_page('pages/23_Wishlist.py')