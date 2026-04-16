##################################################
# This is the main/entry-point file for the
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports regular and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout='wide')

# If a user is at this page, we assume they are not
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false.
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel.
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

logger.info("Loading the Home page of the app")
st.title('📚 ShelfLife')
st.write('#### Northeastern\'s campus course materials marketplace')
st.write('Select your role below to get started.')

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user
# can click to MIMIC logging in as that mock user.

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.write('**Student Seller**')
    seller = st.selectbox(
        'Select seller account:',
        ['Maya Thomas'],
        key='seller_select'
    )
    if st.button('Log in as Seller', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'seller'
        st.session_state['first_name'] = seller.split()[0]
        st.session_state['user_id'] = 1 if seller == 'Maya Thomas' else 3
        st.switch_page('pages/10_Seller_Home.py')

with col2:
    st.write('**Student Buyer**')
    buyer = st.selectbox(
        'Select buyer account:',
        ['Ethan Park'],
        key='buyer_select'
    )
    if st.button('Log in as Buyer', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'buyer'
        st.session_state['first_name'] = buyer.split()[0]
        st.session_state['user_id'] = 2
        st.switch_page('pages/20_Buyer_Home.py')

col3, col4 = st.columns(2)

with col3:
    st.write('**Data Analyst**')
    analyst = st.selectbox(
        'Select analyst account:',
        ['Ricky Spiffy', 'Dana Cross'],
        key='analyst_select'
    )
    if st.button('Log in as Analyst', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'analyst'
        st.session_state['first_name'] = analyst.split()[0]
        st.session_state['user_id'] = 1 if analyst == 'Ricky Spiffy' else 2
        st.switch_page('pages/30_Analyst_Home.py')

with col4:
    st.write('**Platform Admin**')
    admin = st.selectbox(
        'Select admin account:',
        ['Jordan Kanpa', 'Sarah Mitchell'],
        key='admin_select'
    )
    if st.button('Log in as Admin', type='primary', use_container_width=True):
        st.session_state['authenticated'] = True
        st.session_state['role'] = 'admin'
        st.session_state['first_name'] = admin.split()[0]
        st.session_state['user_id'] = 1 if admin == 'Jordan Kanpa' else 2
        st.switch_page('pages/40_Admin_Home.py')