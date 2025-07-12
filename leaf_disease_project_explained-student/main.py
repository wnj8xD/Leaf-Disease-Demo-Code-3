import streamlit as st
from modules.auth import login_user, create_user
from modules.db import init_db
from modules.home import show_home
from modules.feedback import save_feedback
from modules.history import show_user_history, show_area_statistics

# App config
st.set_page_config(page_title="Leaf Disease Detection App", layout="centered")
init_db()

# Session states
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "registered" not in st.session_state:
    st.session_state.registered = False
if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# THEME SWITCHER
if st.session_state.theme == "Dark":
    background_color = "#121212"
    foreground_color = "#f1f1f1"
    container_bg = "rgba(30, 30, 30, 0.95)"
    button_bg = "#43A047"
    button_hover = "#2E7D32"
    tab_text_color = "white"
    alert_text_color = "#ffffff"
    radio_label_color = "#43A047"
    radio_option_color = "#43A047"
    info_bg = "#2c2c2c"
    info_text_color = "#e0e0e0"
    warning_bg = "#453C1E"
    warning_text_color = "#fff3cd"
else:
    background_color = "#ffffff url('https://res.cloudinary.com/dtjjgiitl/image/upload/q_auto:good,f_auto,fl_progressive/v1751949019/pm8nqffbgjmemdhdnszh.jpg') no-repeat center center fixed"
    foreground_color = "#1A1A1A"
    container_bg = "rgba(255, 255, 255, 0.9)"
    button_bg = "#2E7D32"
    button_hover = "#1B5E20"
    tab_text_color = "black"
    alert_text_color = "#000000"
    radio_label_color = "#2E7D32"
    radio_option_color = "#2E7D32"
    info_bg = "#e8f4ff"
    info_text_color = "#000000"
    warning_bg = "#fff3cd"
    warning_text_color = "#000000"

# Custom CSS injection
st.markdown(f"""
    <style>
    .stApp {{
        background: {background_color};
        background-size: cover;
    }}
    .block-container {{
        background-color: {container_bg};
        padding: 2rem;
        border-radius: 16px;
        max-width: 700px;
        margin: auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        color: {foreground_color};
    }}
    h1, h2, h3 {{
        color: {foreground_color};
        text-align: center;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.4);
    }}
    .stButton>button {{
        background-color: {button_bg};
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }}
    .stButton>button:hover {{
        background-color: {button_hover};
        transform: scale(1.03);
    }}
    .stTabs [role="tab"] > div {{
        color: {tab_text_color} !important;
        font-weight: 600;
    }}
    .stAlert > div {{
        color: {alert_text_color} !important;
        font-weight: 600;
    }}
    .stRadio > label {{
        color: {radio_label_color} !important;
        font-weight: 600;
    }}
    .stRadio div[role="radiogroup"] > label span {{
        color: {radio_option_color} !important;
        font-weight: 600;
    }}
    .stAlert[data-baseweb="notification"] > div:first-child {{
        background-color: {info_bg} !important;
        color: {info_text_color} !important;
    }}
    .stAlert[data-baseweb="warning"] > div:first-child {{
        background-color: {warning_bg} !important;
        color: {warning_text_color} !important;
    }}
    </style>
""", unsafe_allow_html=True)

# Tabs
tabs = st.tabs(["🌿 Main Page", "📝 Sign Up", "🔐 Sign In", "📊 History", "⚙️ Settings"])

# -------- Main Page --------
with tabs[0]:
    st.title("🌿 Plant Disease Checker 🌳")

    if not st.session_state.logged_in:
        st.warning("Please log in to use the application")
        st.info("Use the '🔐 Sign In' or '📝 Sign Up' tab above.")
    else:
        st.write(f"👋 Welcome back, **{st.session_state.username}**")
        show_home(st.session_state.username)

# -------- Sign Up --------
with tabs[1]:
    st.title("📝 Register Account")
    username = st.text_input("Username", key="signup_user")
    password = st.text_input("Password", type="password", key="signup_pass")
    confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

    if st.button("Register"):
        if not username or not password:
            st.warning("Please enter all information")
        elif password != confirm:
            st.error("Passwords do not match")
        else:
            success, msg = create_user(username, password)
            if success:
                st.success(msg)
                st.session_state.registered = True
            else:
                st.error(msg)

# -------- Sign In --------
with tabs[2]:
    st.title("🔐 Sign In")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Sign In"):
        if login_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Login successful! Welcome {username}.")
            st.rerun()
        else:
            st.error("Incorrect username or password")

# -------- History --------
with tabs[3]:
    st.title("📊 Diagnosis History")
    if not st.session_state.logged_in:
        st.warning("Please log in to view your history.")
    else:
        show_user_history(st.session_state.username)
        show_area_statistics()

# -------- Settings --------
with tabs[4]:
    st.title("⚙️ Settings")
    theme = st.radio("Choose theme mode:", ["Light", "Dark"], index=["Light", "Dark"].index(st.session_state.theme))
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.rerun()