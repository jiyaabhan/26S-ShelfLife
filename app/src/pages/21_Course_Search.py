import streamlit as st
import pandas as pd
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

import requests
response = requests.get(f'http://api:4000/listings', params={'course': course_query})
listings = response.json()

filtered = listings

if course_query:
    filtered = [l for l in filtered if course_query.upper() in l['course_number'].upper()]
if condition_filter:
    filtered = [l for l in filtered if l['condition'] in condition_filter]
if type_filter:
    filtered = [l for l in filtered if l['type'] in type_filter]
filtered = [l for l in filtered if float(l['price']) <= max_price]

if sort_by == "Price: Low to High":
    filtered = sorted(filtered, key=lambda x: x['price'])
elif sort_by == "Price: High to Low":
    filtered = sorted(filtered, key=lambda x: x['price'], reverse=True)
elif sort_by == "Rating":
    filtered = sorted(filtered, key=lambda x: x['rating'], reverse=True)

st.write(f"**{len(filtered)} listing(s) found**")

if filtered:
    for listing in filtered:
        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"**{listing['title']}**")
                st.caption(f"{listing['course']} · {listing['condition_desc']} · {listing['type']}")
                st.caption(f"Listed by: {listing['seller']} (⭐ {listing['avg_rating']})")
            with col2:
                st.metric("Price", f"${listing['price']:.2f}")
            with col3:
                if st.button("View Details", key=f"view_{listing['listing_id']}"):
                    st.session_state['selected_listing'] = listing
                    st.switch_page('pages/22_Item_Detail.py')
else:
    st.info("No listings found. Try adjusting your filters.")

