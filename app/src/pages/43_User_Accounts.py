import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'admin':
    st.switch_page('Home.py')

st.title("User Account Management")
st.divider()

# TODO: replace with GET request when API is ready
# import requests
# response = requests.get('http://api:4000/users')
# users = response.json()

if 'users' not in st.session_state:
    st.session_state['users'] = [
        {"id": 1, "name": "Maya Thomas", "email": "thomas.ma@northeastern.edu", "role": "Seller", "listings": 7, "sales": 4, "rating": 4.8, "reports": 0, "is_active": True, "joined": "Fall 2023"},
        {"id": 2, "name": "Ethan Park", "email": "park.et@northeastern.edu", "role": "Buyer", "listings": 0, "sales": 0, "rating": None, "reports": 0, "is_active": True, "joined": "Fall 2025"},
        {"id": 3, "name": "Priya Nair", "email": "nair.pr@northeastern.edu", "role": "Seller", "listings": 4, "sales": 3, "rating": 4.5, "reports": 0, "is_active": True, "joined": "Spring 2024"},
        {"id": 4, "name": "Odessa Franklin", "email": "franklin.od@northeastern.edu", "role": "Seller", "listings": 6, "sales": 2, "rating": 2.8, "reports": 2, "is_active": True, "joined": "Fall 2025"},
        {"id": 5, "name": "Alex Martinez", "email": "martinez.al@northeastern.edu", "role": "Seller", "listings": 9, "sales": 7, "rating": 4.2, "reports": 0, "is_active": True, "joined": "Spring 2023"},
        {"id": 6, "name": "Sam Kim", "email": "kim.sa@northeastern.edu", "role": "Buyer", "listings": 0, "sales": 0, "rating": None, "reports": 0, "is_active": False, "joined": "Fall 2024"},
    ]

col1, col2, col3 = st.columns(3)
with col1:
    search = st.text_input("Search by name or email", placeholder="e.g. Maya")
with col2:
    role_filter = st.selectbox("Role", ["All", "Seller", "Buyer"])
with col3:
    status_filter = st.selectbox("Status", ["All", "Active", "Inactive"])

st.divider()

filtered = st.session_state['users']
if search:
    filtered = [u for u in filtered if search.lower() in u['name'].lower() or search.lower() in u['email'].lower()]
if role_filter != "All":
    filtered = [u for u in filtered if u['role'] == role_filter]
if status_filter == "Active":
    filtered = [u for u in filtered if u['is_active']]
elif status_filter == "Inactive":
    filtered = [u for u in filtered if not u['is_active']]

st.write(f"**{len(filtered)} user(s) found**")

for user in filtered:
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            st.write(f"**{user['name']}**")
            st.caption(f"{user['email']} · {user['role']} · Joined {user['joined']}")
            if user['reports'] > 0:
                st.warning(f"⚠️ {user['reports']} prior report(s) on file")
        with col2:
            st.write(f"Listings: {user['listings']}")
            st.write(f"Sales: {user['sales']}")
            st.write(f"Rating: {'⭐ ' + str(user['rating']) if user['rating'] else 'N/A'}")
        with col3:
            if user['is_active']:
                st.success("Active")
                if st.button("View Full History", key=f"history_{user['id']}"):
                    st.session_state[f"show_history_{user['id']}"] = True
                if st.button("Deactivate Account", key=f"deactivate_{user['id']}"):
                    # TODO: PUT request when API is ready
                    # requests.put(f'http://api:4000/users/{user["id"]}', json={"is_active": False})
                    # requests.put(f'http://api:4000/listings/user/{user["id"]}/deactivate-all')
                    st.error(f"{user['name']}'s account deactivated and listings removed.")
            else:
                st.error("Inactive")
                if st.button("Reactivate Account", key=f"reactivate_{user['id']}"):
                    # TODO: PUT request when API is ready
                    # requests.put(f'http://api:4000/users/{user["id"]}', json={"is_active": True})
                    st.success(f"{user['name']}'s account reactivated.")

        if st.session_state.get(f"show_history_{user['id']}"):
            st.write("**Listing & Transaction History**")
            history_data = {
                "Item": ["Engineering Mechanics: Dynamics", "TI-84 Calculator", "CS 2500 Lab Kit"],
                "Course": ["MECH 2350", "MATH 1341", "CS 2500"],
                "Price": ["$215", "$65", "$40"],
                "Status": ["Active", "Active", "Sold"],
                "Date Listed": ["Apr 10, 2026", "Apr 3, 2026", "Mar 15, 2026"]
            }
            st.dataframe(pd.DataFrame(history_data), use_container_width=True)
            if st.button("Hide History", key=f"hide_{user['id']}"):
                st.session_state[f"show_history_{user['id']}"] = False