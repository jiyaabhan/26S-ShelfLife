import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'admin':
    st.switch_page('Home.py')

st.title("User Account Management")
st.divider()

try:
    r = requests.get('http://api:4000/users/')
    st.write(r.status_code)
    st.write(r.text)
    data = r.json() if r.status_code == 200 else {}
    users = data.get("users", []) if isinstance(data, dict) else []
except Exception as e:
    st.error(f"Could not load users: {e}")
    users = []

col1, col2, col3 = st.columns(3)
with col1:
    search = st.text_input("Search by name or email", placeholder="e.g. Maya")
with col2:
    role_filter = st.selectbox("Role", ["All", "Seller", "Buyer"])
with col3:
    status_filter = st.selectbox("Status", ["All", "Active", "Inactive"])

st.divider()

filtered = users
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
                if st.button("View Full History", key=f"history_{user['user_id']}"):
                    st.session_state[f"show_history_{user['user_id']}"] = True
                if st.button("Deactivate Account", key=f"deactivate_{user['user_id']}"):
                    requests.put(
                        f'http://api:4000/users/{user["user_id"]}/deactivate',
                        json={"reason": "admin_action"}
                    )
                    st.error(f"{user['name']}'s account deactivated.")
                    st.rerun()
            else:
                st.error("Inactive")
                if st.button("Reactivate Account", key=f"reactivate_{user['user_id']}"):
                    requests.put(f'http://api:4000/users/{user["user_id"]}/reactivate')
                    st.success(f"{user['name']}'s account reactivated.")
                    st.rerun()

        if st.session_state.get(f"show_history_{user['user_id']}"):
            st.write("**Listing & Transaction History**")
            history_data = {
                "Item": ["Engineering Mechanics: Dynamics", "TI-84 Calculator", "CS 2500 Lab Kit"],
                "Course": ["MECH 2350", "MATH 1341", "CS 2500"],
                "Price": ["$215", "$65", "$40"],
                "Status": ["Active", "Active", "Sold"],
                "Date Listed": ["Apr 10, 2026", "Apr 3, 2026", "Mar 15, 2026"]
            }
            st.dataframe(pd.DataFrame(history_data), use_container_width=True)
            if st.button("Hide History", key=f"hide_{user['user_id']}"):
                st.session_state[f"show_history_{user['user_id']}"] = False