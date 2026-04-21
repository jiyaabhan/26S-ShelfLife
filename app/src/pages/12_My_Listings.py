import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'seller':
    st.switch_page('Home.py')

st.title("My Listings")
st.divider()

try:
    r = requests.get(f'http://api:4000/users/{st.session_state["user_id"]}/listings')
    listings = r.json().get("listings", []) if r.status_code == 200 else []
except Exception as e:
    st.error(f"Could not load listings: {e}")
    listings = []

tab1, tab2, tab3 = st.tabs(["Active", "Reserved", "Sold"])

def render_listing_card(listing):
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"**{listing.get('title', 'N/A')}**")
            st.caption(f"{listing.get('course_number', '')} · {listing.get('condition_desc', '')}")
            st.caption(f"Search count: {listing.get('search_count', 0)}")
        with col2:
            st.metric("Price", f"${float(listing.get('price', 0)):.2f}")
        with col3:
            st.caption(f"Status: {listing.get('status', 'N/A')}")

        edit_col, sold_col, reserve_col = st.columns(3)
        with edit_col:
            if st.button("Edit Price", key=f"edit_{listing.get('listing_id')}"):
                st.session_state[f"editing_{listing.get('listing_id')}"] = True
        with sold_col:
            if st.button("Mark as Sold", key=f"sold_{listing.get('listing_id')}"):
                try:
                    requests.put(
                        f'http://api:4000/listings/{listing.get("listing_id")}',
                        json={
                            "status": "Sold",
                            "price": float(listing.get("price", 0)),
                            "condition_desc": listing.get("condition_desc", "")
                        }
                    )
                    st.success("Marked as sold!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        with reserve_col:
            if st.button("Mark Reserved", key=f"reserve_{listing.get('listing_id')}"):
                try:
                    requests.put(
                        f'http://api:4000/listings/{listing.get("listing_id")}',
                        json={
                            "status": "Reserved",
                            "price": float(listing.get("price", 0)),
                            "condition_desc": listing.get("condition_desc", "")
                        }
                    )
                    st.success("Marked as reserved!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        if st.session_state.get(f"editing_{listing.get('listing_id')}"):
            new_price = st.number_input(
                "New Price ($)",
                value=float(listing.get('price', 0)),
                key=f"price_{listing.get('listing_id')}"
            )
            if st.button("Save Price", key=f"save_{listing.get('listing_id')}"):
                try:
                    requests.put(
                        f'http://api:4000/listings/{listing.get("listing_id")}',
                        json={
                            "price": new_price,
                            "status": listing.get("status", "Active"),
                            "condition_desc": listing.get("condition_desc", "")
                        }
                    )
                    st.success("Price updated!")
                    st.session_state[f"editing_{listing.get('listing_id')}"] = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

with tab1:
    active = [l for l in listings if l.get('status') == 'Active']
    if active:
        for listing in active:
            render_listing_card(listing)
    else:
        st.info("No active listings.")

with tab2:
    reserved = [l for l in listings if l.get('status') == 'Reserved']
    if reserved:
        for listing in reserved:
            render_listing_card(listing)
    else:
        st.info("No reserved listings.")

with tab3:
    sold = [l for l in listings if l.get('status') == 'Sold']
    if sold:
        for listing in sold:
            render_listing_card(listing)
    else:
        st.info("No sold listings yet.")