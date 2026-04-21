import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'buyer':
    st.switch_page('Home.py')

if st.button("← Back to Search Results"):
    st.switch_page('pages/21_Course_Search.py')

listing_data = st.session_state.get('selected_listing', {})
listing_id = listing_data.get('listing_id', 1)

try:
    r = requests.get(f'http://api:4000/listings/{listing_id}')
    listing = r.json() if r.status_code == 200 else listing_data
except Exception:
    listing = listing_data

try:
    r2 = requests.get(f'http://api:4000/listings/{listing_id}/reviews')
    reviews = r2.json().get("reviews", []) if r2.status_code == 200 else []
except Exception:
    reviews = []

st.title(listing.get('title', 'Item Detail'))
st.caption(f"{listing.get('course_number', '')} · {listing.get('category', '')}")
st.divider()

col1, col2 = st.columns([2, 1])

with col1:
    st.write(f"**Condition:** {listing.get('condition_desc', 'N/A')}")
    st.write(f"**Listed by:** {listing.get('seller', 'N/A')} (⭐ {listing.get('avg_rating', 'N/A')})")
    if listing.get('author'):
        st.write(f"**Author:** {listing.get('author')}")
    if listing.get('edition'):
        st.write(f"**Edition:** {listing.get('edition')}")
    st.divider()

    if st.button("❤️ Save to Wishlist", type="primary", use_container_width=True):
        try:
            r = requests.post(
                f'http://api:4000/users/{st.session_state["user_id"]}/wishlist',
                json={"listing_id": listing_id}
            )
            if r.status_code == 201:
                st.success("Added to your wishlist!")
            else:
                st.error("Could not add to wishlist.")
        except Exception as e:
            st.error(f"Error: {e}")
if st.button("❤️ Save to Wishlist", type="primary", use_container_width=True, key="wishlist_btn"):
    try:
        r = requests.post(
            f'http://api:4000/users/{st.session_state["user_id"]}/wishlist',
            json={"listing_id": listing_id}
        )
        if r.status_code == 201:
            st.success("Added to your wishlist!")
        else:
            st.error("Could not add to wishlist.")
    except Exception as e:
        st.error(f"Error: {e}")

st.divider()

if st.button("🛒 Buy Now", use_container_width=True, key="buy_now_btn"):
    try:
        r = requests.post(
            'http://api:4000/transactions/',
            json={
                "listing_id": listing_id,
                "buyer_id": st.session_state['user_id'],
                "sale_price": float(listing.get('price', 0)),
                "days_to_sale": 1
            }
        )
        if r.status_code == 201:
            st.success("Purchase complete! The seller will be in touch.")
            st.balloons()
        else:
            st.error(f"Could not complete purchase: {r.text}")
    except Exception as e:
        st.error(f"Error: {e}")

    st.divider()
    st.subheader("Seller Reviews")
    if reviews:
        for review in reviews:
            with st.container(border=True):
                stars = "⭐" * review.get('rating', 0)
                st.write(f"{stars} — **{review.get('reviewer', 'Anonymous')}**")
                st.write(review.get('comment', ''))
    else:
        st.info("No reviews yet.")

with col2:
    st.metric("Asking Price", f"${float(listing.get('price', 0)):.2f}")
    st.divider()
    st.write("**Price History**")
    try:
        r3 = requests.get(f'http://api:4000/courses/price-history/{listing.get("listing_id", 1)}')
        history = r3.json().get("history", []) if r3.status_code == 200 else []
        if history:
            import pandas as pd
            df = pd.DataFrame(history)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No price history available.")
    except Exception:
        st.info("No price history available.")