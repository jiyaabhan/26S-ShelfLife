import streamlit as st
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'admin':
    st.switch_page('Home.py')

st.title("Course Catalog Manager")
st.divider()

try:
    r = requests.get('http://api:4000/courses/')
    data = r.json() if r.status_code == 200 else {}
    courses = data.get("courses", []) if isinstance(data, dict) else []
except Exception as e:
    st.error(f"Could not load courses: {e}")
    courses = []

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    search = st.text_input("Search by course number or name", placeholder="e.g. CS 3200")
with col2:
    dept_filter = st.selectbox("Department", ["All"] + sorted(list(set([c.get('dept_name', '') for c in courses]))))
with col3:
    status_filter = st.selectbox("Status", ["All", "Active", "Inactive"])

st.divider()

filtered = courses
if search:
    filtered = [c for c in filtered if search.upper() in c.get('course_number', '').upper() or search.lower() in c.get('course_name', '').lower()]
if dept_filter != "All":
    filtered = [c for c in filtered if c.get('dept_name') == dept_filter]
if status_filter == "Active":
    filtered = [c for c in filtered if c.get('is_active') == 1]
elif status_filter == "Inactive":
    filtered = [c for c in filtered if c.get('is_active') == 0]

st.write(f"**{len(filtered)} course(s) found**")

for course in filtered:
    with st.container(border=True):
        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
        with col1:
            st.write(f"**{course.get('course_number')}** — {course.get('course_name')}")
            st.caption(f"Dept: {course.get('dept_name')} · College: {course.get('college')}")
        with col2:
            st.write(f"ID: {course.get('course_id')}")
        with col3:
            if course.get('is_active') == 1:
                st.success("Active")
            else:
                st.error("Inactive")
        with col4:
            ecol, dcol = st.columns(2)
            with ecol:
                if st.button("Edit", key=f"edit_{course.get('course_id')}"):
                    st.session_state[f"editing_course_{course.get('course_id')}"] = True
            with dcol:
                if st.button("Deactivate", key=f"deactivate_{course.get('course_id')}"):
                    try:
                        requests.put(f'http://api:4000/courses/{course.get("course_id")}/deactivate')
                        st.warning(f"{course.get('course_number')} deactivated.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

        if st.session_state.get(f"editing_course_{course.get('course_id')}"):
            with st.form(key=f"form_{course.get('course_id')}"):
                new_name = st.text_input("Course Name", value=course.get('course_name', ''))
                new_status = st.selectbox("Status", ["Active", "Inactive"],
                                          index=0 if course.get('is_active') == 1 else 1)
                submitted = st.form_submit_button("Save Changes")
                if submitted:
                    try:
                        requests.put(f'http://api:4000/courses/{course.get("course_id")}', json={
                            "course_name": new_name,
                            "is_active": new_status == "Active"
                        })
                        st.success("Updated!")
                        st.session_state[f"editing_course_{course.get('course_id')}"] = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

st.divider()
st.subheader("Add a New Course")
with st.form("add_course_form"):
    ncol1, ncol2 = st.columns(2)
    with ncol1:
        new_number = st.text_input("Course Number", placeholder="e.g. CS 4500")
        new_course_name = st.text_input("Course Name", placeholder="e.g. Software Development")
    with ncol2:
        new_dept_id = st.number_input("Department ID", min_value=1, value=1)
    submitted = st.form_submit_button("Add Course", type="primary")
    if submitted:
        if not new_number or not new_course_name:
            st.error("Please fill in course number and name.")
        else:
            try:
                r = requests.post('http://api:4000/courses/', json={
                    "course_number": new_number,
                    "course_name": new_course_name,
                    "dept_id": new_dept_id
                })
                if r.status_code == 201:
                    st.success(f"Course {new_number} added!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")