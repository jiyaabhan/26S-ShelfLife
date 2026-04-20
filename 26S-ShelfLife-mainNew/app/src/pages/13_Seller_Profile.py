import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'seller':
    st.switch_page('Home.py')

st.title("My Profile & Reviews")
st.divider()

# TODO: replace with GET request when API is ready
# import requests
# response = requests.get(f'http://api:4000/users/{st.session_state["user_id"]}')
# user = response.json()

user = {
    "name": "Maya Thomas",
    "email": "thomas.ma@northeastern.edu",
    "member_since": "Fall 2023",
    "avg_rating": 4.8,
    "total_reviews": 12,
    "total_listings": 7,
    "completed_sales": 4
}

reviews = [
    {"reviewer": "Ethan P.", "semester": "Fall 2025", "rating": 5, "comment": "Fast response, item exactly as described."},
    {"reviewer": "Priya N.", "semester": "Spring 2025", "rating": 4, "comment": "Great seller, easy pickup on campus."},
    {"reviewer": "Sam K.", "semester": "Spring 2025", "rating": 5, "comment": "Item was in perfect condition. Would buy again!"},
]

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