import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'buyer':
    st.switch_page('Home.py')

st.title("My Wishlist")
st.write("Listings you've saved to compare.")
st.divider()

# TODO: replace with GET request when API is ready
# import requests
# response = requests.get(f'http://api:4000/wishlist/{st.session_state["user_id"]}')
# wishlist = response.json()

wishlist = [
    {"id": 1, "title": "Engineering Mechanics: Dynamics", "course": "MECH 2350", "condition": "Lightly Used", "price": 215.00, "seller": "Maya T.", "rating": 4.8, "saved_at": "Apr 10, 2026"},
    {"id": 2, "title": "TI-84 Plus Graphing Calculator", "course": "MATH 1341", "condition": "Unused", "price": 65.00, "seller": "Maya T.", "rating": 4.8, "saved_at": "Apr 12, 2026"},
]

if wishlist:
    st.write(f"**{len(wishlist)} saved item(s)**")
    for item in wishlist:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{item['title']}**")
                st.caption(f"{item['course']} · {item['condition']}")
                st.caption(f"Listed by: {item['seller']} (⭐ {item['rating']}) · Saved {item['saved_at']}")
            with col2:
                st.metric("Price", f"${item['price']:.2f}")
            with col3:
                if st.button("View", key=f"view_{item['id']}"):
                    st.session_state['selected_listing'] = item
                    st.switch_page('pages/22_Item_Detail.py')
                if st.button("Remove", key=f"remove_{item['id']}"):
                    # TODO: DELETE request when API is ready
                    # requests.delete(f'http://api:4000/wishlist/{st.session_state["user_id"]}/{item["id"]}')
                    st.success("Removed from wishlist!")
else:
    st.info("Your wishlist is empty. Browse listings and save items you're interested in!")
    if st.button("Browse Listings"):
        st.switch_page('pages/21_Course_Search.py')