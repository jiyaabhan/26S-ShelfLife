import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'buyer':
    st.switch_page('Home.py')

if st.button("← Back to Search Results"):
    st.switch_page('pages/21_Course_Search.py')

# TODO: replace with GET request when API is ready
# import requests
# listing_id = st.session_state.get('selected_listing_id')
# response = requests.get(f'http://api:4000/listings/{listing_id}')
# listing = response.json()

listing = st.session_state.get('selected_listing', {
    "id": 1,
    "title": "Engineering Mechanics: Dynamics",
    "course": "MECH 2350",
    "condition": "Lightly Used",
    "price": 215.00,
    "seller": "Maya T.",
    "rating": 4.8,
    "type": "Textbook",
    "condition_notes": "Minor highlighting in chapters 1-3. Binding intact. All pages present. ISBN sticker on back cover.",
    "status": "Active"
})

price_history = [
    {"Semester": "S'23", "Avg Sale Price": "$165"},
    {"Semester": "F'23", "Avg Sale Price": "$183"},
    {"Semester": "S'24", "Avg Sale Price": "$193"},
    {"Semester": "F'24", "Avg Sale Price": "$210"},
    {"Semester": "S'25", "Avg Sale Price": "$215"},
]

reviews = [
    {"reviewer": "Ethan P.", "semester": "Fall 2025", "rating": 5, "comment": "Fast response, item exactly as described."},
    {"reviewer": "Priya N.", "semester": "Spring 2025", "rating": 4, "comment": "Great seller, easy pickup on campus."},
]

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
        # TODO: POST request when API is ready
        # requests.post('http://api:4000/wishlist', json={
        #     "user_id": st.session_state['user_id'],
        #     "listing_id": listing['id']
        # })
        st.success("Added to your wishlist!")

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