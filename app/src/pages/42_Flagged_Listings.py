import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'admin':
    st.switch_page('Home.py')

st.title("Flagged Listings Review Queue")
st.divider()

try:
    r = requests.get('http://api:4000/analytics/flags')
    data = r.json() if r.status_code == 200 else {}
    flags = data.get("flags", []) if isinstance(data, dict) else []
except Exception as e:
    st.error(f"Could not load flags: {e}")
    flags = []

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Flagged", len(flags))
with col2:
    st.metric("Pending Review", len([f for f in flags if f.get('flag_status') == 'Pending']))
with col3:
    st.metric("Unique Sellers", len(set([f.get('seller_id') for f in flags])))

st.divider()

for flag in flags:
    with st.container(border=True):
        st.warning(f"Flag #{flag.get('flag_id')} · Flagged {flag.get('flagged_at', '')}")

        lcol, scol = st.columns(2)
        with lcol:
            st.write("**Listing**")
            st.write(f"**{flag.get('title')}**")
            st.caption(f"${float(flag.get('price', 0)):.2f} · {flag.get('condition_desc')}")
            st.write("Report reason:")
            st.warning(flag.get('reason', ''))

        with scol:
            st.write("**Seller**")
            st.write(f"{flag.get('seller')}")
            st.caption(f"Rating: ⭐ {flag.get('avg_rating')}")

        acol1, acol2, acol3 = st.columns(3)
        with acol1:
            if st.button("Approve", key=f"approve_{flag.get('flag_id')}"):
                try:
                    requests.put(f'http://api:4000/analytics/flags/{flag.get("flag_id")}',
                                json={"flag_status": "Resolved"})
                    st.success("Approved!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        with acol2:
            if st.button("Remove Listing", key=f"remove_{flag.get('flag_id')}"):
                try:
                    requests.delete(f'http://api:4000/listings/{flag.get("listing_id")}')
                    st.success("Listing removed.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
        with acol3:
            if st.button("Deactivate User", key=f"deactivate_{flag.get('flag_id')}"):
                try:
                    requests.put(f'http://api:4000/users/{flag.get("seller_id")}/deactivate',
                                json={"reason": "admin_action"})
                    st.error("User deactivated.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")