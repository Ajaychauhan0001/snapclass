# src/screens/student_screen.py
import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard


def Student_screen():
    style_background_dashboard()
    style_base_layout()

    if 'show_student_login' not in st.session_state:
        st.session_state.show_student_login = False
    if 'show_student_register' not in st.session_state:
        st.session_state.show_student_register = False

    # ── Top bar ──────────────────────────────────────────────────────
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to Home", type='secondary', key='student_back_main',
                    shortcut="control+backspace"):
            st.session_state.show_student_login = False
            st.session_state.show_student_register = False
            st.rerun()

    st.header('Register your student profile')

    # ── Trigger buttons ───────────────────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        if st.button(" Login", key='student_open_login'):
            st.session_state.show_student_login = True
            st.session_state.show_student_register = False
            st.rerun()
    with col2:
        if st.button(" Register Instead", key='student_open_register'):
            st.session_state.show_student_register = True
            st.session_state.show_student_login = False
            st.rerun()

    if st.session_state.show_student_login:
        _student_login()

    if st.session_state.show_student_register:
        _student_register()


def _student_login():
    st.markdown("""
        <style>
        .student-box {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.18);
            margin: 1.5rem 0;
        }
        </style>
        <div class="student-box">
            <h3 style="text-align:center; font-weight:800;">Login using password</h3>
        </div>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        # ── Back to home ──
        if st.button("Go back to Home", type='secondary', key='student_login_back_home',
                    shortcut="control+backspace"):
            st.session_state.show_student_login = False
            st.rerun()

        student_username = st.text_input(
            "Enter username", placeholder='@abhishek', key='student_login_username'
        )
        student_pass = st.text_input(
            "Enter password", placeholder='Enter your password',
            type='password', key='student_login_pass'
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button(" Login", key='student_submit_login',
                        shortcut="control+Return", type='primary'):
                if student_username and student_pass:
                    st.success(f"Welcome, {student_username}!")
                    # TODO: auth logic here
                else:
                    st.error("Please fill in both fields.")
        with col2:
            if st.button(" Register Instead", key='student_switch_to_register'):
                st.session_state.show_student_login = False
                st.session_state.show_student_register = True
                st.rerun()

        st.divider()
        st.markdown(
            "<p style='text-align:center; font-size:0.8rem;'>Created with ❤️ by AJAY CHAUHAN</p>",
            unsafe_allow_html=True
        )


def _student_register():
    with st.container(border=True):
        st.markdown(
            "<h3 style='text-align:center; font-weight:800;'>Register your student profile</h3>",
            unsafe_allow_html=True
        )

        # ── Back to home ──
        if st.button("Go back to Home", type='secondary', key='student_register_back_home',
                    shortcut="control+backspace"):
            st.session_state.show_student_register = False
            st.rerun()

        full_name = st.text_input("Full name", placeholder='Abhishek Roy', key='student_reg_name')
        username  = st.text_input("Username",  placeholder='@abhishek',    key='student_reg_username')
        password  = st.text_input("Password",  type='password',            key='student_reg_pass')
        confirm   = st.text_input("Confirm password", type='password',     key='student_reg_confirm')

        col1, col2 = st.columns(2)
        with col1:
            if st.button(" Register", key='student_submit_register', type='primary'):
                if password != confirm:
                    st.error("Passwords don't match.")
                elif full_name and username and password:
                    st.success(f"Registered as {username}!")
                    # TODO: save to DB here
                else:
                    st.error("Please fill in all fields.")
        with col2:
            if st.button("← Back to Login", key='student_switch_to_login'):
                st.session_state.show_student_register = False
                st.session_state.show_student_login = True
                st.rerun()

        st.divider()
        st.markdown(
            "<p style='text-align:center; font-size:0.8rem;'>Created with ❤️ by AJAY CHAUHAN</p>",
            unsafe_allow_html=True
        )