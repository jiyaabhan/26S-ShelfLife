import streamlit as st


def home_nav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")


# ---- Role: seller -----------------------------------------------------------

def seller_home_nav():
    st.sidebar.page_link("pages/10_Seller_Home.py", label="Seller Dashboard", icon="👤")

def create_listing_nav():
    st.sidebar.page_link("pages/11_Create_Listing.py", label="Create Listing", icon="➕")

def my_listings_nav():
    st.sidebar.page_link("pages/12_My_Listings.py", label="My Listings", icon="📋")

def seller_profile_nav():
    st.sidebar.page_link("pages/13_Seller_Profile.py", label="My Profile & Reviews", icon="⭐")


# ---- Role: buyer ------------------------------------------------------------

def buyer_home_nav():
    st.sidebar.page_link("pages/20_Buyer_Home.py", label="Browse", icon="🔍")

def course_search_nav():
    st.sidebar.page_link("pages/21_Course_Search.py", label="Search by Course", icon="📖")

def item_detail_nav():
    st.sidebar.page_link("pages/22_Item_Detail.py", label="Item Detail", icon="🏷️")

def wishlist_nav():
    st.sidebar.page_link("pages/23_Wishlist.py", label="My Wishlist", icon="❤️")


# ---- Role: analyst ----------------------------------------------------------

def analyst_home_nav():
    st.sidebar.page_link("pages/30_Analyst_Home.py", label="Analyst Dashboard", icon="📊")

def platform_overview_nav():
    st.sidebar.page_link("pages/31_Platform_Overview.py", label="Platform Overview", icon="🌐")

def price_trends_nav():
    st.sidebar.page_link("pages/32_Price_Trends.py", label="Price Trends", icon="📈")

def seller_activity_nav():
    st.sidebar.page_link("pages/33_Seller_Activity.py", label="Seller Activity", icon="🏪")


# ---- Role: admin ------------------------------------------------------------

def admin_home_nav():
    st.sidebar.page_link("pages/40_Admin_Home.py", label="Admin Dashboard", icon="🖥️")

def course_catalog_nav():
    st.sidebar.page_link("pages/41_Course_Catalog.py", label="Course Catalog", icon="📚")

def flagged_listings_nav():
    st.sidebar.page_link("pages/42_Flagged_Listings.py", label="Flagged Listings", icon="🚩")

def user_accounts_nav():
    st.sidebar.page_link("pages/43_User_Accounts.py", label="User Accounts", icon="👥")


# ---- Sidebar assembly -------------------------------------------------------

def SideBarLinks(show_home=False):
    st.sidebar.image("assets/logo.png", width=150)

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        home_nav()

    if st.session_state["authenticated"]:

        if st.session_state["role"] == "seller":
            seller_home_nav()
            create_listing_nav()
            my_listings_nav()
            seller_profile_nav()

        elif st.session_state["role"] == "buyer":
            buyer_home_nav()
            course_search_nav()
            item_detail_nav()
            wishlist_nav()

        elif st.session_state["role"] == "analyst":
            analyst_home_nav()
            platform_overview_nav()
            price_trends_nav()
            seller_activity_nav()

        elif st.session_state["role"] == "admin":
            admin_home_nav()
            course_catalog_nav()
            flagged_listings_nav()
            user_accounts_nav()

    if st.session_state["authenticated"]:
        if st.sidebar.button("Logout", key="logout_btn"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")