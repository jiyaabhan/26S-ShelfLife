import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'buyer':
    st.switch_page('Home.py')

st.title("My Wishlist")
st.write("Listings you've saved to compare.")
st.divider()

try:
    r = requests.get(f'http://api:4000/users/{st.session_state["user_id"]}/wishlist')
    wishlist = r.json().get("wishlist", []) if r.status_code == 200 else []
except Exception as e:
    st.error(f"Could not load wishlist: {e}")
    wishlist = []

if wishlist:
    st.write(f"**{len(wishlist)} saved item(s)**")
    for item in wishlist:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item.get('title', 'N/A')}**")
                st.caption(f"{item.get('course_number', '')} · {item.get('condition_desc', '')}")
                st.caption(f"Listed by: {item.get('seller', 'N/A')} (⭐ {item.get('avg_rating', 'N/A')}) · Saved {item.get('saved_at', '')}")
            with col2:
                st.metric("Price", f"${float(item.get('price', 0)):.2f}")
            with col3:
                if st.button("View", key=f"view_{item.get('wishlist_id')}"):
                    st.session_state['selected_listing'] = item
                    st.switch_page('pages/22_Item_Detail.py')
                if st.button("Remove", key=f"remove_{item.get('wishlist_id')}"):
                    try:
                        requests.delete(
                            f'http://api:4000/users/{st.session_state["user_id"]}/wishlist/{item.get("wishlist_id")}'
                        )
                        st.success("Removed!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
else:
    st.info("Your wishlist is empty. Browse listings and save items you're interested in!")
    if st.button("Browse Listings"):
        st.switch_page('pages/21_Course_Search.py')