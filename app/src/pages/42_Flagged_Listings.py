import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'admin':
    st.switch_page('Home.py')

st.title("Flagged Listings Review Queue")
st.divider()

r = requests.get('http://api:4000/analytics/flags')
flags = r.json().get("flags", []) if r.status_code == 200 else []

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Flagged", len(flags))
with col2:
    high = len([f for f in flags if f['priority'] == 'HIGH'])
    st.metric("High Priority", high)
with col3:
    med = len([f for f in flags if f['priority'] == 'MED'])
    st.metric("Med Priority", med)

st.divider()

priority_filter = st.selectbox("Filter by Priority", ["All", "HIGH", "MED", "LOW"])
filtered_flags = flags
if priority_filter != "All":
    filtered_flags = [f for f in filtered_flags if f['priority'] == priority_filter]

for flag in filtered_flags:
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            if flag['priority'] == 'HIGH':
                st.error(f"Report #{flag['flag_id']} · {flag['num_reports']} report(s) · HIGH PRIORITY")
            elif flag['priority'] == 'MED':
                st.warning(f"Report #{flag['flag_id']} · {flag['num_reports']} report(s) · MED PRIORITY")
            else:
                st.info(f"Report #{flag['flag_id']} · {flag['num_reports']} report(s) · LOW PRIORITY")

        lcol, scol = st.columns(2)
        with lcol:
            st.write("**Listing**")
            st.write(f"**{flag['listing_title']}**")
            st.caption(f"{flag['course']} · ${flag['price']:.2f} · {flag['condition']}")
            st.write("Report reason:")
            st.warning(flag['report_reason'])

        with scol:
            st.write("**Seller Account**")
            st.write(f"{flag['seller']}")
            st.caption(f"Rating: ⭐ {flag['seller_rating']} ({flag['seller_reviews']} reviews)")
            st.caption(f"Active listings: {flag['active_listings']} · Prior reports: {flag['prior_reports']}")
            st.caption(f"Joined: {flag['joined']}")

        st.write("**Actions**")
        acol1, acol2, acol3 = st.columns(3)
        with acol1:
            if st.button("Approve Listing", key=f"approve_{flag['flag_id']}"):
                requests.put(
                    f'http://api:4000/analytics/flags/{flag["flag_id"]}',
                    json={"flag_status": "Resolved"}
                )
                st.success("Approved!")
                st.rerun()
        with acol2:
            if st.button("Remove Listing", key=f"remove_{flag['flag_id']}"):
                requests.delete(f'http://api:4000/listings/{flag["listing_id"]}')
                st.success("Listing removed.")
                st.rerun()
        with acol3:
            if st.button("Deactivate User", key=f"deactivate_{flag['flag_id']}"):
                requests.put(
                    f'http://api:4000/users/{flag["seller_id"]}/deactivate',
                    json={"reason": "admin_action"}
                )
                st.error("User deactivated.")
                st.rerun()