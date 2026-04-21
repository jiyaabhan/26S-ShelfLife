import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'buyer':
    st.switch_page('Home.py')

st.title("Search by Course")
st.write("Find all available materials for your class.")
st.divider()

col1, col2 = st.columns([2, 1])
with col1:
    course_query = st.text_input("Search by course number", placeholder="e.g. MECH 2350")
with col2:
    sort_by = st.selectbox("Sort by", ["Price: Low to High", "Price: High to Low", "Rating"])

st.write("**Filters**")
fcol1, fcol2, fcol3 = st.columns(3)
with fcol1:
    condition_filter = st.multiselect("Condition", ["Unused", "Lightly Used", "Used", "Rough"])
with fcol2:
    type_filter = st.multiselect("Item Type", ["Textbook", "Equipment", "Misc"])
with fcol3:
    max_price = st.slider("Max Price ($)", 0, 500, 500)

st.divider()

try:
    r = requests.get('http://api:4000/listings/', params={'course': course_query})
    data = r.json() if r.status_code == 200 else {}
    all_listings = data.get("listings", []) if isinstance(data, dict) else []
except Exception as e:
    st.error(f"Could not connect to API: {e}")
    all_listings = []

filtered = all_listings

if condition_filter:
    filtered = [l for l in filtered if l.get('condition_desc') in condition_filter]
if type_filter:
    filtered = [l for l in filtered if l.get('category') in type_filter]
filtered = [l for l in filtered if float(l.get('price', 0)) <= max_price]

if sort_by == "Price: Low to High":
    filtered = sorted(filtered, key=lambda x: float(x.get('price', 0)))
elif sort_by == "Price: High to Low":
    filtered = sorted(filtered, key=lambda x: float(x.get('price', 0)), reverse=True)
elif sort_by == "Rating":
    filtered = sorted(filtered, key=lambda x: float(x.get('avg_rating', 0)), reverse=True)

st.write(f"**{len(filtered)} listing(s) found**")

if filtered:
    for listing in filtered:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{listing.get('title', 'N/A')}**")
                st.caption(f"{listing.get('course_number', '')} · {listing.get('condition_desc', '')} · {listing.get('category', '')}")
                st.caption(f"Listed by: {listing.get('seller', 'N/A')} (⭐ {listing.get('avg_rating', 'N/A')})")
            with col2:
                st.metric("Price", f"${float(listing.get('price', 0)):.2f}")
            with col3:
                if st.button("View Details", key=f"view_{listing.get('listing_id')}"):
                    st.session_state['selected_listing'] = listing
                    st.switch_page('pages/22_Item_Detail.py')
else:
    st.info("No listings found. Try adjusting your filters.")