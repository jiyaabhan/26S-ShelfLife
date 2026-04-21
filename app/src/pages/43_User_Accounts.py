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
    data = r.json() if r.status_code == 200 else {}
    users = data.get("users", []) if isinstance(data, dict) else []
except Exception as e:
    st.error(f"Could not load users: {e}")
    users = []

col1, col2, col3 = st.columns(3)
with col1:
    search = st.text_input("Search by name or email", placeholder="e.g. Maya")
with col2:
    status_filter = st.selectbox("Status", ["All", "Active", "Inactive"])
with col3:
    st.metric("Total Users", len(users))

st.divider()

filtered = users
if search:
    filtered = [u for u in filtered if
                search.lower() in u.get('name', '').lower() or
                search.lower() in u.get('email', '').lower()]
if status_filter == "Active":
    filtered = [u for u in filtered if u.get('is_active') == 1]
elif status_filter == "Inactive":
    filtered = [u for u in filtered if u.get('is_active') == 0]

st.write(f"**{len(filtered)} user(s) found**")

for user in filtered:
    with st.container(border=True):
        col1, col2, col3 = st.columns([3, 1, 2])
        with col1:
            st.write(f"**{user.get('name', 'N/A')}**")
            st.caption(f"{user.get('email', 'N/A')}")
            if user.get('avg_rating'):
                st.caption(f"⭐ {user.get('avg_rating')}")
        with col2:
            if user.get('is_active') == 1:
                st.success("Active")
            else:
                st.error("Inactive")
        with col3:
            if user.get('is_active') == 1:
                if st.button("View History", key=f"history_{user.get('user_id')}"):
                    st.session_state[f"show_history_{user.get('user_id')}"] = True
                if st.button("Deactivate", key=f"deactivate_{user.get('user_id')}"):
                    try:
                        requests.put(
                            f'http://api:4000/users/{user.get("user_id")}/deactivate',
                            json={"reason": "admin_action"}
                        )
                        st.error(f"{user.get('name')} deactivated.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                if st.button("Reactivate", key=f"reactivate_{user.get('user_id')}"):
                    try:
                        requests.put(
                            f'http://api:4000/users/{user.get("user_id")}/reactivate'
                        )
                        st.success(f"{user.get('name')} reactivated.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

        if st.session_state.get(f"show_history_{user.get('user_id')}"):
            try:
                r2 = requests.get(f'http://api:4000/users/{user.get("user_id")}/listings')
                listing_data = r2.json().get("listings", []) if r2.status_code == 200 else []
                if listing_data:
                    df = pd.DataFrame(listing_data)
                    st.dataframe(df[['title', 'course_number', 'price', 'status', 'created_at']],
                                use_container_width=True)
                else:
                    st.info("No listings found for this user.")
            except Exception as e:
                st.error(f"Could not load history: {e}")
            if st.button("Hide", key=f"hide_{user.get('user_id')}"):
                st.session_state[f"show_history_{user.get('user_id')}"] = False