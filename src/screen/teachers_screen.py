import streamlit as st

from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer_dashboard
from src.components.subject_card import subject_card
from src.database.db import check_teacher_exists, create_teacher, teacher_login, get_teacher_subject, get_attendance_for_teacher
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog

from src.pipelines.face_pipeline import predict_attendance
from src.components.dialog_attendance_results import attendance_result_dialog
import pandas as pd
import numpy as np
from datetime import datetime

from src.database.config import supabase

from src.components.dialog_voice_attendance import voice_attendance_dialog

# ── Entry point ───────────────────────────────────────────────────────────────

def Teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
        return

    if "show_teacher_login" not in st.session_state:
        st.session_state.show_teacher_login = False
    if "show_teacher_register" not in st.session_state:
        st.session_state.show_teacher_register = False

    teacher_screen_login()


# ── Logged-in dashboard ───────────────────────────────────────────────────────

def teacher_dashboard():
    if "teacher_data" not in st.session_state:
        st.warning("No teacher session found.")
        st.stop()

    teacher_data = st.session_state.teacher_data

    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f"Welcome, {teacher_data['name']}")
        if st.button(
            "Logout",
            key="teacher_logout",
            shortcut="control+backspace",
            type="primary",
        ):
            st.session_state.show_teacher_login = False
            st.session_state.show_teacher_register = False
            del st.session_state.teacher_data
            st.session_state.is_logged_in = False
            st.session_state.user_role = None
            st.rerun()

    st.divider()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendance" else "tertiary"
        if st.button("Take Attendance", type=type1, use_container_width=True, icon=":material/ar_on_you:"):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_students" else "tertiary"
        if st.button("Manage Students", type=type2, use_container_width=True, icon=":material/book_ribbon:"):
            st.session_state.current_teacher_tab = "manage_students"
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendance_records" else "tertiary"
        if st.button("Attendance Records", type=type3, use_container_width=True, icon=":material/cards_stack:"):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()
    elif st.session_state.current_teacher_tab == "manage_students":
        teacher_tab_manage_students()
    elif st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()

    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header("Take AI Attendance")

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return

    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3, 1])

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add photos', type='primary', icon=':material/photo_prints:', use_container_width=True):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallary_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallary_cols[idx % 4]:
                st.image(img, use_container_width=True, caption=f'photo {idx+1}')

        has_photos = bool(st.session_state.attendance_images)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button('Clear all photos', use_container_width=True, type='tertiary', icon=':material/delete:', disabled=not has_photos):
                st.session_state.attendance_images = []
                st.rerun()

        with c2:
            if st.button('Run Face Analysis', use_container_width=True, type='secondary', icon=':material/analytics:', disabled=not has_photos):
                with st.spinner('Deep scanning classroom photos...'):
                    all_detected_ids = {}

                    for idx, img in enumerate(st.session_state.attendance_images):
                        img_np = np.array(img.convert('RGB'))

                        detected, all_students, num_faces = predict_attendance(img_np)
                        st.write(f"Photo {idx+1}: faces detected = {num_faces}, matches = {detected}, known students = {all_students}")

                        if detected:
                            for sid in detected.keys():
                                student_id = int(sid)
                                all_detected_ids.setdefault(student_id, []).append(f"photo {idx+1}")

                    enrolled_res = (
                        supabase.table('subject_students')
                        .select('*, students(*)')
                        .eq('subject_id', selected_subject_id)
                        .execute()
                    )
                    enrolled_student = enrolled_res.data

                    if not enrolled_student:
                        st.warning('No students enrolled in this course')
                    else:
                        results, attendance_to_log = [], []

                        current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                        for node in enrolled_student:
                            student = node['students']
                            sources = all_detected_ids.get(int(student['student_id']), [])
                            is_present = len(sources) > 0

                            results.append({
                                "Name": student['name'],
                                "ID": student['student_id'],
                                "Source": ", ".join(sources) if is_present else "_",
                                "Status": "✅ present" if is_present else "❌ Absent"
                            })

                            attendance_to_log.append({
                                'student_id': student['student_id'],
                                'subject_id': selected_subject_id,
                                'timestamp': current_timestamp,
                                'is_present': bool(is_present)
                            })

                        attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

        with c3:
            if st.button('Use Voice Attendance', type='primary', use_container_width=True, icon=':material/mic:'):
                voice_attendance_dialog(selected_subject_id)


def teacher_tab_manage_students():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    col1, col2 = st.columns(2)
    with col1:
        st.header("Manage Students")
    with col2:
        if st.button("Create New Subject", use_container_width=True):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂", "Students", sub['total_students']),
                ("🕰️", "Classes", sub['total_classes']),
            ]

            def make_share_btn(s):
                def share_btn():
                    if st.button(f"Share Code", key=f"share_{s['subject_code']}", icon=":material/share:"):
                        share_subject_dialog(s['name'], s['subject_code'])
                    st.write('')
                return share_btn

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=make_share_btn(sub)
            )
    else:
        st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def teacher_tab_attendance_records():
    st.header("Attendance Records")

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return

    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split('.')[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N/A",
            "Subject": r['subjects']['name'],
            "Subject_Code": r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject_Code'])
        .agg(
            Present_Count=('is_present', 'sum'),
            Total_Count=('is_present', 'count')
        ).reset_index()
    )

    summary['Attendance Stats'] = (
        "✅" + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
        [['Time', 'Subject', 'Subject_Code', 'Attendance Stats']]
    )

    st.dataframe(display_df, width='stretch', hide_index=True)


# ── Auth helpers ──────────────────────────────────────────────────────────────

def login_teacher(username: str, password: str) -> bool:
    if not username or not password:
        return False
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


def register_teacher(
    teacher_username: str,
    teacher_name: str,
    teacher_pass: str,
    teacher_pass_confirm: str,
) -> tuple[bool, str]:
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All fields are required!"
    if teacher_pass != teacher_pass_confirm:
        return False, "Passwords don't match."
    if check_teacher_exists(teacher_username):
        return False, "Username already taken."
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Account created! You can now log in."
    except Exception:
        return False, "An unexpected error occurred. Please try again."


# ── Portal landing page ───────────────────────────────────────────────────────

def teacher_screen_login():
    c1, c2 = st.columns(2, vertical_alignment="center", gap="xxlarge")
    with c1:
        header_dashboard()
    with c2:
        if st.button(
            "Go back to Home",
            type="secondary",
            key="teacher_back_main",
            shortcut="control+backspace",
        ):
            st.session_state.show_teacher_login = False
            st.session_state.show_teacher_register = False
            st.rerun()

    st.header("Teacher Portal")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login", key="teacher_open_login"):
            st.session_state.show_teacher_login = True
            st.session_state.show_teacher_register = False
            st.rerun()
    with col2:
        if st.button("Register Instead", key="teacher_open_register"):
            st.session_state.show_teacher_register = True
            st.session_state.show_teacher_login = False
            st.rerun()

    if st.session_state.show_teacher_login:
        _teacher_login()

    if st.session_state.show_teacher_register:
        _teacher_register()


# ── Login form ────────────────────────────────────────────────────────────────

def _teacher_login():
    with st.container(border=True):
        st.markdown(
            "<h3 style='text-align:center; font-weight:800;'>Login using password</h3>",
            unsafe_allow_html=True,
        )

        if st.button(
            "Go back to Home",
            type="secondary",
            key="teacher_login_back_home",
            shortcut="control+backspace",
        ):
            st.session_state.show_teacher_login = False
            st.rerun()

        teacher_username = st.text_input(
            "Enter username", placeholder="@abhishek", key="teacher_login_username"
        )
        teacher_pass = st.text_input(
            "Enter password",
            placeholder="Enter your password",
            type="password",
            key="teacher_login_pass",
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "Login",
                key="teacher_submit_login",
                shortcut="control+Return",
                type="primary",
            ):
                if login_teacher(teacher_username, teacher_pass):
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with col2:
            if st.button("Register Instead", key="teacher_switch_to_register"):
                st.session_state.show_teacher_login = False
                st.session_state.show_teacher_register = True
                st.rerun()

        st.divider()
        st.markdown(
            "<p style='text-align:center; font-size:0.8rem;'>Created with ❤️ by AJAY CHAUHAN </p>",
            unsafe_allow_html=True,
        )

    footer_dashboard()


# ── Register form ─────────────────────────────────────────────────────────────

def _teacher_register():
    with st.container(border=True):
        st.markdown(
            "<h3 style='text-align:center; font-weight:800;'>Register your teacher profile</h3>",
            unsafe_allow_html=True,
        )

        if st.button(
            "Go back to Home",
            type="secondary",
            key="teacher_register_back_home",
            shortcut="control+backspace",
        ):
            st.session_state.show_teacher_register = False
            st.rerun()

        full_name = st.text_input(
            "Full name", placeholder="Abhishek Roy", key="teacher_reg_name"
        )
        username = st.text_input(
            "Username", placeholder="@abhishek", key="teacher_reg_username"
        )
        password = st.text_input("Password", type="password", key="teacher_reg_pass")
        confirm = st.text_input(
            "Confirm password", type="password", key="teacher_reg_confirm"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Register", key="teacher_submit_register", type="primary"):
                success, message = register_teacher(username, full_name, password, confirm)
                if success:
                    st.success(message)
                    st.session_state.show_teacher_register = False
                    st.session_state.show_teacher_login = True
                    st.rerun()
                else:
                    st.error(message)

        with col2:
            if st.button("← Back to Login", key="teacher_switch_to_login"):
                st.session_state.show_teacher_register = False
                st.session_state.show_teacher_login = True
                st.rerun()

        st.divider()
        st.markdown(
            "<p style='text-align:center; font-size:0.8rem;'>Created with ❤️ by AJAY CHAUHAN</p>",
            unsafe_allow_html=True,
        )