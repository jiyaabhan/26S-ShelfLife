import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'admin':
    st.switch_page('Home.py')

st.title("Course Catalog Manager")
st.caption("Spring 2026")
st.divider()

# TODO: replace with GET request when API is ready
# import requests
# response = requests.get('http://api:4000/courses')
# courses = response.json()

if 'courses' not in st.session_state:
    st.session_state['courses'] = [
        {"id": 1, "course_number": "CS 2500", "course_name": "Fundamentals of CS 1", "dept": "CS", "materials": "Textbook, Lab Kit", "active_listings": 14, "status": "Active"},
        {"id": 2, "course_number": "MECH 2350", "course_name": "Engineering Mechanics", "dept": "MECH", "materials": "Textbook, Calculator", "active_listings": 9, "status": "Active"},
        {"id": 3, "course_number": "CHEM 2313", "course_name": "Organic Chemistry I", "dept": "CHEM", "materials": "Lab Manual, Safety Kit", "active_listings": 3, "status": "Active"},
        {"id": 4, "course_number": "ARTD 1200", "course_name": "Foundation Drawing", "dept": "ARTD", "materials": "Drawing Kit", "active_listings": 4, "status": "Pending Review"},
        {"id": 5, "course_number": "ECON 1115", "course_name": "Principles of Microeconomics", "dept": "ECON", "materials": "Textbook", "active_listings": 6, "status": "Active"},
        {"id": 6, "course_number": "PHYS 1145", "course_name": "Physics for Engineers I", "dept": "PHYS", "materials": "Textbook, Lab Manual", "active_listings": 0, "status": "Inactive"},
    ]

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    search = st.text_input("Search by course number or name", placeholder="e.g. CS 3200")
with col2:
    dept_filter = st.selectbox("Department", ["All", "CS", "MECH", "CHEM", "ARTD", "ECON", "PHYS"])
with col3:
    status_filter = st.selectbox("Status", ["All", "Active", "Inactive", "Pending Review"])

st.divider()

filtered = st.session_state['courses']
if search:
    filtered = [c for c in filtered if search.upper() in c['course_number'].upper() or search.lower() in c['course_name'].lower()]
if dept_filter != "All":
    filtered = [c for c in filtered if c['dept'] == dept_filter]
if status_filter != "All":
    filtered = [c for c in filtered if c['status'] == status_filter]

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
            if course['status'] == "Active":
                st.success(course['status'])
            elif course['status'] == "Inactive":
                st.error(course['status'])
            else:
                st.warning(course['status'])
        with col4:
            ecol, dcol = st.columns(2)
            with ecol:
                if st.button("Edit", key=f"edit_{course['id']}"):
                    st.session_state[f"editing_course_{course['id']}"] = True
            with dcol:
                if st.button("Deactivate", key=f"deactivate_{course['id']}"):
                    # TODO: PUT request when API is ready
                    # requests.put(f'http://api:4000/courses/{course["id"]}', json={"status": "Inactive"})
                    st.warning(f"{course['course_number']} deactivated.")

        if st.session_state.get(f"editing_course_{course['id']}"):
            with st.form(key=f"form_{course['id']}"):
                new_name = st.text_input("Course Name", value=course['course_name'])
                new_materials = st.text_input("Associated Materials", value=course['materials'])
                new_status = st.selectbox("Status", ["Active", "Inactive", "Pending Review"],
                                          index=["Active", "Inactive", "Pending Review"].index(course['status']))
                submitted = st.form_submit_button("Save Changes")
                if submitted:
                    # TODO: PUT request when API is ready
                    # requests.put(f'http://api:4000/courses/{course["id"]}', json={
                    #     "course_name": new_name,
                    #     "materials": new_materials,
                    #     "status": new_status
                    # })
                    st.success(f"Course {course['course_number']} updated!")
                    st.session_state[f"editing_course_{course['id']}"] = False

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
            # TODO: POST request when API is ready
            # requests.post('http://api:4000/courses', json={
            #     "course_number": new_number,
            #     "course_name": new_course_name,
            #     "dept": new_dept,
            #     "materials": new_materials
            # })
            st.success(f"Course {new_number} added successfully!")