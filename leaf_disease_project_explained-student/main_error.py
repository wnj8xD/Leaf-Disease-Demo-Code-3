# main.py - main entry point of the application
import streamlit as st
from modules.auth import login_user, create_user
from modules.db import init_db
from modules.home import show_home
from modules.feedback import save_feedback
from modules.history import show_user_history, show_area_statistics

st.set_page_config(page_title="Leaf Disease Detection App", layout="centered")
init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "menu" not in st.session_state:
    st.session_state.menu = "Main Page"

menu_options = ["Main Page", "Sign Up", "Sign In", "History"]
selected = st.sidebar.selectbox("Function", menu_options, index=menu_options.index(st.session_state.menu))
st.session_state.menu = selected
menu = st.session_state.menu

if menu == "Sign Up":
    st.title("Register Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm = st.text_input("Confirm Password", type="password")
    if st.button("Register"):
        if not username or not password:
            st.warning("Please enter all information")
        elif password != confirm:
            st.error("Passwords do not match")
        else:
            success, msg = create_user(username, password)
            if success:
                st.success(msg)
                if st.button("👉 Log In Now"):
                    st.session_state.menu = "Sign In"
                    st.rerun()
            else:
                st.error(msg)

elif menu == "Sign In":
    st.title("Sign In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign In"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Login successful! Welcome {username}.")
            st.session_state.menu = "Main Page"
            st.rerun()
        else:
            st.error("Incorrect username or password")

elif menu == "Main Page":
    st.write("Hello ", st.session_state.username)
    st.title("🌿 Plant Disease Checker🌳")
    st.header("With just one photo, we can identify diseases on your plants! 🤩")
    if not st.session_state.logged_in:
        st.warning("Please log in to use the application")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👉 Log In Now"):
                st.session_state.menu = "Sign In"
                st.rerun()
        with col2:
            if st.button("📝 Create New Account"):
                st.session_state.menu = "Sign Up"
                st.rerun()
    else:
        show_home(st.session_state.username)

elif menu == "History":
    show_user_history(st.session_state.username)
    show_area_statistics()
