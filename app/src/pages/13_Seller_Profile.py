import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'seller':
    st.switch_page('Home.py')

st.title("My Profile & Reviews")
st.divider()

try:
    r = requests.get(f'http://api:4000/users/{st.session_state["user_id"]}')
    user = r.json() if r.status_code == 200 else {}
except Exception as e:
    st.error(f"Could not load profile: {e}")
    user = {}

try:
    r2 = requests.get(f'http://api:4000/users/{st.session_state["user_id"]}/reviews')
    reviews = r2.json().get("reviews", []) if r2.status_code == 200 else []
except Exception as e:
    reviews = []

try:
    r3 = requests.get(f'http://api:4000/users/{st.session_state["user_id"]}/listings')
    listings_data = r3.json().get("listings", []) if r3.status_code == 200 else []
except Exception:
    listings_data = []

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(user.get('name', 'N/A'))
    st.caption(f"📧 {user.get('email', 'N/A')}")
    st.divider()
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Avg Rating", f"⭐ {user.get('avg_rating', 'N/A')}")
        st.metric("Total Listings", len(listings_data))
    with m2:
        st.metric("Reviews", len(reviews))
        completed = [l for l in listings_data if l.get('status') == 'Sold']
        st.metric("Sales", len(completed))

with col2:
    st.subheader("Buyer Reviews")
    if reviews:
        for review in reviews:
            with st.container(border=True):
                stars = "⭐" * review.get('rating', 0)
                st.write(f"{stars} — **{review.get('reviewer', 'Anonymous')}**")
                st.write(review.get('comment', ''))
    else:
        st.info("No reviews yet.")