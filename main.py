import streamlit as st
from modules.check_password import check_password_strength
from modules.generate_password import generate_strong_password
import hashlib
from datetime import datetime

st.set_page_config(page_title="PassGuard: Password Strength Meter", page_icon="🔐")

# Inject custom CSS
st.markdown("""
    <style>
    :root {
        --primary-color-rgb: 145, 123, 193;
        --shadow-color: 0,0,0;
        --strong-color: #28a745;
        --moderate-color: #ffc107;
        --weak-color: #dc3545;
    }
    [data-theme="dark"] {
        --shadow-color: 255,255,255;
        --primary-color-rgb: 161, 138, 214;
    }
    [data-theme="light"] {
        --shadow-color: 0,0,0;
    }
    .stButton > button {
        background-color: #917bc1;
        width: 100%;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #FF4B4B;
    }
    .stButton > button,
    .stButton > button:hover,
    .stButton > button:active,
    .stButton > button:focus {
        color: #ffffff !important;
    }
    .stTextInput > div > div > input {
        border: 2px solid #917bc1;
        border-radius: 5px;
        padding: 10px;
    }
    .result-container {
        margin-top: 20px;
        margin-bottom: 15px;
        padding: 10px;
        background: rgba(var(--primary-color-rgb), 0.08);
        border-radius: 12px;
        text-align: center;
        box-shadow: 
            0 4px 12px rgba(var(--shadow-color), 0.15),
            0 0 0 2px rgba(var(--primary-color-rgb), 0.15);
        border: 3px solid rgba(var(--primary-color-rgb), 0.3);
        transition: all 0.3s ease;
    }
    .strong {
        border-color: var(--strong-color);
        background: rgba(40, 167, 69, 0.1);
    }
    .moderate {
        border-color: var(--moderate-color);
        background: rgba(255, 193, 7, 0.1);
    }
    .weak {
        border-color: var(--weak-color);
        background: rgba(220, 53, 69, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Heading and description
st.markdown(
    "<h1 style='text-align: center;'>🔐 PassGuard: Password Strength Meter</h1>",
    unsafe_allow_html=True
    )
st.markdown(
    "<p style='text-align: center;'>A sleek, secure tool to evaluate password strength, generate strong passwords.</p>",
    unsafe_allow_html=True
    )
password = st.text_input("Enter your password", type="default")

if 'password_history' not in st.session_state:
    st.session_state.password_history = []

col1, col2 = st.columns(2)
with col1:
    check_button = st.button("Check Password")
with col2:
    generate_button = st.button("Generate Strong Password")

# Progress bar
progress = st.progress(0)

# Check Password logic
if check_button:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if password == "":
        st.error("Please type your password to check.")
    else:
        if any(hashed_password == hp for hp, _ in st.session_state.password_history):
            st.error("You cannot reuse a recent password.")
        else:
            strength, feedback, strength_bar = check_password_strength(password)
            if strength == "Strong":
                st.markdown('''
                    <div class="result-container strong">
                        <strong>Password Strength:</strong> ✅ Strong
                    </div>
                ''', unsafe_allow_html=True)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.session_state.password_history.append((hashed_password, timestamp))
                if len(st.session_state.password_history) > 10:
                    st.session_state.password_history.pop(0)
                progress.progress(strength_bar)
            elif strength == "Moderate":
                st.markdown('''
                    <div class="result-container moderate">
                        <strong>Password Strength:</strong> ⚠️ Moderate - Consider improvements.
                    </div>
                ''', unsafe_allow_html=True)
                progress.progress(strength_bar)
                if feedback:
                    st.write("Suggestions:")
                    for msg in feedback:
                        st.write(f"- {msg}")
            else:
                st.markdown('''
                    <div class="result-container weak">
                        <strong>Password Strength:</strong> ❌ Weak
                    </div>
                ''', unsafe_allow_html=True)
                progress.progress(strength_bar)
                if feedback:
                    st.write("Suggestions:")
                    for msg in feedback:
                        st.write(f"- {msg}")

# Generate Strong Password
if generate_button:
    new_password = generate_strong_password()
    st.write("Suggested Password:")
    st.code(new_password)

# Sidebar
st.sidebar.title("📜 Password History")
if st.session_state.password_history:
    for i, entry in enumerate(st.session_state.password_history, 1):
        ts = entry[1]
        st.sidebar.write(f"**Password {i}:** Set on {ts}")
else:
    st.sidebar.write("No passwords in history yet.")

# Clear Password History
st.sidebar.markdown("---")
st.sidebar.subheader("🗑️ Clear History")
confirm_clear = st.sidebar.checkbox("Check to confirm clear")
if st.sidebar.button("Clear Password History"):
    if confirm_clear:
        st.session_state.password_history = []
        st.sidebar.success("Password history cleared!")
        st.rerun()
    else:
        st.sidebar.warning("Please check the box to confirm.")

st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ By Owais Abdullah")