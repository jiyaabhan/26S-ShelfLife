import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'seller':
    st.switch_page('Home.py')

st.title("Create a New Listing")
st.write("Fill in the details below to list your course material.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Item Details")
    isbn = st.text_input("ISBN (optional — auto-fills details)", placeholder="e.g. 9780131103627")
    title = st.text_input("Item Title", placeholder="e.g. Engineering Mechanics: Dynamics")
    author = st.text_input("Author", placeholder="e.g. Hibbeler")
    edition = st.text_input("Edition", placeholder="e.g. 14th")
    category = st.selectbox("Category", ["Textbook", "Calculator", "Lab Kit", "Art Supply", "Software", "Other"])

with col2:
    st.subheader("Listing Details")
    course = st.selectbox("Course Association", [
        "CS 3200 — Database Design",
        "MECH 2350 — Engineering Mechanics",
        "CHEM 2313 — Organic Chemistry I",
        "MATH 1341 — Calculus 1",
        "CS 2500 — Fundamentals of CS 1"
    ])
    condition = st.selectbox("Condition", ["Unused", "Lightly Used", "Used", "Rough"])
    price = st.number_input("Asking Price ($)", min_value=0.0, max_value=1000.0, step=0.50)
    condition_notes = st.text_area("Condition Notes", placeholder="e.g. Minor highlighting in chapters 1-3. Binding intact.")

st.divider()
if st.button("Publish Listing", type="primary", use_container_width=True):
    if not title:
        st.error("Please enter an item title.")
    elif price == 0:
        st.error("Please enter a price greater than $0.")
    else:
        item_r = requests.post('http://api:4000/items/', json={
            "title": title,
            "author": author,
            "edition": edition,
            "isbn": isbn,
            "category": category,
        })
        if item_r.status_code != 201:
            st.error(f"Failed to create item. Status: {item_r.status_code} — {item_r.text}")
        else:
            item_id = item_r.json().get("item_id")
            r = requests.post('http://api:4000/listings/', json={
                "user_id": st.session_state['user_id'],
                "item_id": item_id,
                "course_id": 1,
                "price": price,
                "condition_desc": condition,
            })
            if r.status_code == 201:
                st.success("Listing published!")
                st.balloons()
            else:
                st.error(f"Something went wrong. Status: {r.status_code} — {r.text}")