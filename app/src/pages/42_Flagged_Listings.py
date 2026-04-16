import streamlit as st
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'admin':
    st.switch_page('Home.py')

st.title("Flagged Listings Review Queue")
st.divider()

# TODO: replace with GET request when API is ready
# import requests
# response = requests.get('http://api:4000/flags')
# flags = response.json()

if 'flags' not in st.session_state:
    st.session_state['flags'] = [
        {
            "id": 1047,
            "listing_title": "TI-84 Graphing Calculator — Brand New",
            "course": "MATH 1341",
            "price": 145.00,
            "condition": "New/Unused",
            "report_reason": "Item described as new but photos show visible wear and scratches. Possible condition misrepresentation.",
            "num_reports": 3,
            "priority": "HIGH",
            "seller": "u/odessafranklinsmith",
            "seller_rating": 2.8,
            "seller_reviews": 4,
            "active_listings": 6,
            "prior_reports": 2,
            "joined": "Sep 2025",
            "flag_status": "Pending"
        },
        {
            "id": 1044,
            "listing_title": "Organic Chemistry Lab Manual (CHEM 2313)",
            "course": "CHEM 2313",
            "price": 90.00,
            "condition": "Lightly Used",
            "report_reason": "Course association appears incorrect — this manual is listed under the wrong semester edition.",
            "num_reports": 1,
            "priority": "MED",
            "seller": "u/priya_rao22",
            "seller_rating": 4.5,
            "seller_reviews": 8,
            "active_listings": 2,
            "prior_reports": 0,
            "joined": "Jan 2024",
            "flag_status": "Pending"
        },
        {
            "id": 1039,
            "listing_title": "CS 2500 Lab Kit",
            "course": "CS 2500",
            "price": 35.00,
            "condition": "Used",
            "report_reason": "Listing price is significantly above market rate for this item.",
            "num_reports": 1,
            "priority": "LOW",
            "seller": "u/alexm_neu",
            "seller_rating": 4.2,
            "seller_reviews": 6,
            "active_listings": 3,
            "prior_reports": 0,
            "joined": "Aug 2024",
            "flag_status": "Pending"
        },
    ]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Flagged", len(st.session_state['flags']))
with col2:
    high = len([f for f in st.session_state['flags'] if f['priority'] == 'HIGH'])
    st.metric("High Priority", high)
with col3:
    med = len([f for f in st.session_state['flags'] if f['priority'] == 'MED'])
    st.metric("Med Priority", med)

st.divider()

priority_filter = st.selectbox("Filter by Priority", ["All", "HIGH", "MED", "LOW"])
filtered_flags = st.session_state['flags']
if priority_filter != "All":
    filtered_flags = [f for f in filtered_flags if f['priority'] == priority_filter]

for flag in filtered_flags:
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        with col1:
            if flag['priority'] == 'HIGH':
                st.error(f"Report #{flag['id']} · {flag['num_reports']} report(s) · HIGH PRIORITY")
            elif flag['priority'] == 'MED':
                st.warning(f"Report #{flag['id']} · {flag['num_reports']} report(s) · MED PRIORITY")
            else:
                st.info(f"Report #{flag['id']} · {flag['num_reports']} report(s) · LOW PRIORITY")

        lcol, scol = st.columns(2)
        with lcol:
            st.write("**Listing**")
            st.write(f"**{flag['listing_title']}**")
            st.caption(f"{flag['course']} · ${flag['price']:.2f} · {flag['condition']}")
            st.write(f"Report reason:")
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
            if st.button("Approve Listing", key=f"approve_{flag['id']}"):
                # TODO: PUT request when API is ready
                # requests.put(f'http://api:4000/flags/{flag["id"]}', json={"flag_status": "Resolved"})
                st.success("Listing approved and flag resolved.")
        with acol2:
            if st.button("Remove Listing", key=f"remove_{flag['id']}"):
                # TODO: DELETE request when API is ready
                # requests.delete(f'http://api:4000/listings/{flag["listing_id"]}')
                st.success("Listing removed.")
        with acol3:
            if st.button("Deactivate User", key=f"deactivate_{flag['id']}"):
                # TODO: PUT request when API is ready
                # requests.put(f'http://api:4000/users/{flag["seller_id"]}', json={"is_active": False})
                st.error(f"User {flag['seller']} deactivated.")