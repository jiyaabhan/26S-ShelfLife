import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'buyer':
    st.switch_page('Home.py')

if st.button("← Back to Search Results"):
    st.switch_page('pages/21_Course_Search.py')


import requests
listing_id = st.session_state.get('selected_listing', {}).get('listing_id', 1)
r = requests.get(f'http://api:4000/listings/{listing_id}')
listing = r.json() if r.status_code == 200 else {}

r2 = requests.get(f'http://api:4000/listings/{listing_id}/reviews')
reviews = r2.json().get("reviews", []) if r2.status_code == 200 else []

st.title(listing['title'])
st.caption(f"{listing['course']} · {listing['type']}")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.write(f"**Condition:** {listing['condition']}")
    st.write(f"**Listed by:** {listing['seller']} (⭐ {listing['rating']})")
    st.write(f"**Condition Notes:** {listing['condition_notes']}")
    st.divider()

    if st.button("❤️ Save to Wishlist", type="primary", use_container_width=True):
        r = requests.post(
        f'http://api:4000/users/{st.session_state["user_id"]}/wishlist',
        json={"listing_id": listing_id})
        if r.status_code == 201:
            st.success("Added to your wishlist!")
        else:
            st.error("Could not add to wishlist.")

    st.divider()
    st.subheader("Seller Reviews")
    for review in reviews:
        with st.container(border=True):
            stars = "⭐" * review['rating']
            st.write(f"{stars} — **{review['reviewer']}** · {review['semester']}")
            st.write(review['comment'])

with col2:
    st.metric("Asking Price", f"${listing['price']:.2f}")
    st.divider()
    st.write("**Price History**")
    st.caption("Historical sales for this item:")
    st.table(price_history)
    st.info("Avg: $193 | Low: $165 | High: $215")