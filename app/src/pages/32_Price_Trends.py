import streamlit as st
import pandas as pd
import requests
from modules.nav import SideBarLinks

SideBarLinks()

if 'role' not in st.session_state or st.session_state['role'] != 'analyst':
    st.switch_page('Home.py')

st.title("Price Trend Explorer")
st.write("View historical pricing trends for items across semesters.")
st.divider()

try:
    r = requests.get('http://api:4000/courses/')
    data = r.json() if r.status_code == 200 else {}
    courses = data.get("courses", []) if isinstance(data, dict) else []
    course_options = {f"{c.get('course_number')} — {c.get('course_name')}": c.get('course_id') for c in courses}
except Exception:
    course_options = {}

col1, col2 = st.columns(2)
with col1:
    selected_course_label = st.selectbox("Select Course", list(course_options.keys()) if course_options else ["No courses available"])
with col2:
    time_range = st.selectbox("Time Range", ["All time", "Last 4 semesters", "Last 2 semesters"])

selected_course_id = course_options.get(selected_course_label)

st.divider()

try:
    r2 = requests.get(f'http://api:4000/courses/{selected_course_id}/price-history')
    hist_data = r2.json() if r2.status_code == 200 else {}
    history = hist_data.get("history", []) if isinstance(hist_data, dict) else []
except Exception:
    history = []

if history:
    df = pd.DataFrame(history)

    if time_range == "Last 2 semesters":
        df = df.tail(2)
    elif time_range == "Last 4 semesters":
        df = df.tail(4)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Avg Sale Price", f"${df['avg_price'].mean():.0f}")
    with m2:
        st.metric("Price Low", f"${df['avg_price'].min():.0f}")
    with m3:
        st.metric("Price High", f"${df['avg_price'].max():.0f}")
    with m4:
        st.metric("Total Semesters", len(df))

    st.subheader("Price by Semester")
    st.line_chart(df.set_index("semester")["avg_price"])

    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)

    if st.button("Export as CSV", type="primary"):
        try:
            requests.post('http://api:4000/analytics/reports', json={
                "analyst_id": st.session_state['user_id'],
                "filter_params": f"course_id={selected_course_id}",
                "format": "CSV"
            })
        except Exception:
            pass
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", data=csv,
                          file_name="price_trends.csv", mime="text/csv")
else:
    st.info("No price history available for this course.")