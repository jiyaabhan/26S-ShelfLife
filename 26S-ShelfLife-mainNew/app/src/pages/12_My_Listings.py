import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'seller':
    st.switch_page('Home.py')

st.title("My Listings")
st.divider()

# TODO: replace with GET request when API is ready
# import requests
# response = requests.get(f'http://api:4000/listings/user/{st.session_state["user_id"]}')
# listings = response.json()

listings = [
    {"id": 1, "title": "Engineering Mechanics: Dynamics", "course": "MECH 2350", "condition": "Lightly Used", "price": 215.00, "views": 18, "saves": 4, "status": "Active"},
    {"id": 2, "title": "TI-84 Plus Graphing Calculator", "course": "MATH 1341", "condition": "Unused", "price": 65.00, "views": 31, "saves": 7, "status": "Active"},
    {"id": 3, "title": "CS 2500 Lab Kit (sealed)", "course": "CS 2500", "condition": "Unused", "price": 40.00, "views": 9, "saves": 2, "status": "Reserved"},
]

tab1, tab2, tab3 = st.tabs(["Active", "Reserved", "Sold"])

def render_listing_card(listing):
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{listing['title']}**")
            st.caption(f"{listing['course']} · {listing['condition']}")
            st.caption(f"Views: {listing['views']} · Saves: {listing['saves']}")
        with col2:
            st.metric("Price", f"${listing['price']:.2f}")
        with col3:
            st.caption(f"Status: {listing['status']}")

        edit_col, sold_col, reserve_col = st.columns(3)
        with edit_col:
            if st.button("Edit Price", key=f"edit_{listing['id']}"):
                st.session_state[f"editing_{listing['id']}"] = True
        with sold_col:
            if st.button("Mark as Sold", key=f"sold_{listing['id']}"):
                # TODO: PUT request to update status
                # requests.put(f'http://api:4000/listings/{listing["id"]}', json={"status": "Sold"})
                st.success("Marked as sold!")
        with reserve_col:
            if st.button("Mark Reserved", key=f"reserve_{listing['id']}"):
                # TODO: PUT request
                st.success("Marked as reserved!")

        if st.session_state.get(f"editing_{listing['id']}"):
            new_price = st.number_input("New Price ($)", value=listing['price'], key=f"price_{listing['id']}")
            if st.button("Save Price", key=f"save_{listing['id']}"):
                # TODO: PUT request
                # requests.put(f'http://api:4000/listings/{listing["id"]}', json={"price": new_price})
                st.success(f"Price updated to ${new_price:.2f}!")
                st.session_state[f"editing_{listing['id']}"] = False

with tab1:
    active = [l for l in listings if l['status'] == 'Active']
    if active:
        for listing in active:
            render_listing_card(listing)
    else:
        st.info("No active listings.")

with tab2:
    reserved = [l for l in listings if l['status'] == 'Reserved']
    if reserved:
        for listing in reserved:
            render_listing_card(listing)
    else:
        st.info("No reserved listings.")

with tab3:
    st.info("No sold listings yet.")