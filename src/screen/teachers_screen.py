import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard

def Teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if 'show_teacher_login' not in st.session_state:
        st.session_state.show_teacher_login = False
    if 'show_teacher_register' not in st.session_state:
        st.session_state.show_teacher_register = False

    # ── Top bar ──────────────────────────────────────────────────────
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='teacher_back_main',
                    shortcut="control+backspace"):
            st.session_state.show_teacher_login = False
            st.session_state.show_teacher_register = False
            st.rerun()

    st.header('Register your teacher profile')

    # ── Trigger buttons ───────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Login", key='teacher_open_login'):
            st.session_state.show_teacher_login = True
            st.session_state.show_teacher_register = False
            st.rerun()
    with col2:
        if st.button(" Register Instead", key='teacher_open_register'):
            st.session_state.show_teacher_register = True
            st.session_state.show_teacher_login = False
            st.rerun()

    if st.session_state.show_teacher_login:
        _teacher_login()

    if st.session_state.show_teacher_register:
        _teacher_register()


def _teacher_login():
    st.markdown("""
        <style>
        .teacher-box {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.18);
            margin: 1.5rem 0;
        }
        </style>
        <div class="teacher-box">
            <h3 style="text-align:center; font-weight:800;">Login using password</h3>
        </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        # ── Back to home ──
        if st.button("Go back to Home", type='secondary', key='teacher_login_back_home',
                    shortcut="control+backspace"):
            st.session_state.show_teacher_login = False
            st.rerun()

        teacher_username = st.text_input(
            "Enter username", placeholder='@abhishek', key='teacher_login_username'
        )
        teacher_pass = st.text_input(
            "Enter password", placeholder='Enter your password',
            type='password', key='teacher_login_pass'
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧑‍🏫 Login", key='teacher_submit_login',
                        shortcut="control+Return", type='primary'):
                if teacher_username and teacher_pass:
                    st.success(f"Welcome, {teacher_username}!")
                    # TODO: auth logic here
                else:
                    st.error("Please fill in both fields.")
        with col2:
            if st.button("🧑‍🏫 Register Instead", key='teacher_switch_to_register'):
                st.session_state.show_teacher_login = False
                st.session_state.show_teacher_register = True
                st.rerun()

        st.divider()
        st.markdown(
            "<p style='text-align:center; font-size:0.8rem;'>Created with ❤️ by AJAY CHAUHAN</p>",
            unsafe_allow_html=True
        )

    footer_dashboard()


def _teacher_register():
    with st.container(border=True):
        st.markdown(
            "<h3 style='text-align:center; font-weight:800;'>Register your teacher profile</h3>",
            unsafe_allow_html=True
        )

        # ── Back to home ──
        if st.button("Go back to Home", type='secondary', key='teacher_register_back_home',
                    shortcut="control+backspace"):
            st.session_state.show_teacher_register = False
            st.rerun()

        full_name = st.text_input("Full name", placeholder='Abhishek Roy', key='teacher_reg_name')
        username  = st.text_input("Username",  placeholder='@abhishek',    key='teacher_reg_username')
        password  = st.text_input("Password",  type='password',            key='teacher_reg_pass')
        confirm   = st.text_input("Confirm password", type='password',     key='teacher_reg_confirm')

        col1, col2 = st.columns(2)
        with col1:
            if st.button(" Register", key='teacher_submit_register', type='primary'):
                if password != confirm:
                    st.error("Passwords don't match.")
                elif full_name and username and password:
                    st.success(f"Registered as {username}!")
                    # TODO: save to DB here
                else:
                    st.error("Please fill in all fields.")
        with col2:
            if st.button("← Back to Login", key='teacher_switch_to_login'):
                st.session_state.show_teacher_register = False
                st.session_state.show_teacher_login = True
                st.rerun()

        st.divider()
        st.markdown(
            "<p style='text-align:center; font-size:0.8rem;'>Created with ❤️ by AJAY CHAUHAN </p>",
            unsafe_allow_html=True
        )