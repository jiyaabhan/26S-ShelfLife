import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'seller':
    st.switch_page('Home.py')

st.title("My Profile & Reviews")
st.divider()

import requests
r = requests.get(f'http://api:4000/users/{st.session_state["user_id"]}')
user = r.json() if r.status_code == 200 else {}

r2 = requests.get(f'http://api:4000/users/{st.session_state["user_id"]}/reviews')
reviews = r2.json().get("reviews", []) if r2.status_code == 200 else []


col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(user['name'])
    st.caption(f"Member since {user['member_since']}")
    st.caption(f"📧 {user['email']}")
    st.divider()
    m1, m2 = st.columns(2)
    with m1:
        st.metric("Avg Rating", f"⭐ {user['avg_rating']}")
        st.metric("Total Listings", user['total_listings'])
    with m2:
        st.metric("Reviews", user['total_reviews'])
        st.metric("Sales", user['completed_sales'])

with col2:
    st.subheader("Buyer Reviews")
    for review in reviews:
        with st.container(border=True):
            stars = "⭐" * review['rating']
            st.write(f"{stars} — **{review['reviewer']}** · {review['semester']}")
            st.write(review['comment'])