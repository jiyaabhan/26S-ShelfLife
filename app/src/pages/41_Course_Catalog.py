import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'admin':
    st.switch_page('Home.py')

st.title("Course Catalog Manager")
st.caption("Spring 2026")
st.divider()

r = requests.get('http://api:4000/courses/')
courses = r.json().get("courses", []) if r.status_code == 200 else []

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    search = st.text_input("Search by course number or name", placeholder="e.g. CS 3200")
with col2:
    dept_filter = st.selectbox("Department", ["All", "CS", "MECH", "CHEM", "ARTD", "ECON", "PHYS"])
with col3:
    status_filter = st.selectbox("Status", ["All", "Active", "Inactive", "Pending Review"])

st.divider()

filtered = courses
if search:
    filtered = [
        c for c in filtered
        if search.upper() in c['course_number'].upper() or search.lower() in c['course_name'].lower()
    ]
if dept_filter != "All":
    filtered = [c for c in filtered if c['dept'] == dept_filter]
if status_filter == "Active":
    filtered = [c for c in filtered if c['is_active'] == 1]
elif status_filter == "Inactive":
    filtered = [c for c in filtered if c['is_active'] == 0]

st.write(f"**{len(filtered)} course(s) found**")

for course in filtered:
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        with col1:
            st.write(f"**{course['course_number']}** — {course['course_name']}")
            st.caption(f"Dept: {course['dept']} · Materials: {course['materials']}")
        with col2:
            st.metric("Active Listings", course['active_listings'])
        with col3:
            if course['is_active'] == 1:
                st.success("Active")
            else:
                st.error("Inactive")
        with col4:
            ecol, dcol = st.columns(2)
            with ecol:
                if st.button("Edit", key=f"edit_{course['course_id']}"):
                    st.session_state[f"editing_course_{course['course_id']}"] = True
            with dcol:
                if st.button("Deactivate", key=f"deactivate_{course['course_id']}"):
                    requests.put(f'http://api:4000/courses/{course["course_id"]}/deactivate')
                    st.warning(f"{course['course_number']} deactivated.")
                    st.rerun()

        if st.session_state.get(f"editing_course_{course['course_id']}"):
            with st.form(key=f"form_{course['course_id']}"):
                new_name = st.text_input("Course Name", value=course['course_name'])
                new_materials = st.text_input("Associated Materials", value=course['materials'])
                new_status = st.selectbox(
                    "Status",
                    ["Active", "Inactive"],
                    index=["Inactive", "Active"].index("Active" if course['is_active'] == 1 else "Inactive")
                )
                submitted = st.form_submit_button("Save Changes")
                if submitted:
                    requests.put(f'http://api:4000/courses/{course["course_id"]}', json={
                        "course_name": new_name,
                        "is_active": new_status == "Active"
                    })
                    st.success("Updated!")
                    st.session_state[f"editing_course_{course['course_id']}"] = False
                    st.rerun()

st.divider()
st.subheader("Add a New Course")
with st.form("add_course_form"):
    ncol1, ncol2 = st.columns(2)
    with ncol1:
        new_number = st.text_input("Course Number", placeholder="e.g. CS 4500")
        new_course_name = st.text_input("Course Name", placeholder="e.g. Software Development")
    with ncol2:
        new_dept = st.selectbox("Department", ["CS", "MECH", "CHEM", "ARTD", "ECON", "PHYS", "MATH", "BIOL"])
        new_materials = st.text_input("Associated Materials", placeholder="e.g. Textbook, Lab Kit")
    submitted = st.form_submit_button("Add Course", type="primary")
    if submitted:
        if not new_number or not new_course_name:
            st.error("Please fill in course number and name.")
        else:
            r = requests.post('http://api:4000/courses/', json={
                "course_number": new_number,
                "course_name": new_course_name,
                "dept_id": 1
            })
            if r.status_code == 201:
                st.success(f"Course {new_number} added!")
                st.rerun()