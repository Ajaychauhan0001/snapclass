import streamlit as st
import segno
import io
import socket

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

@st.dialog("Share Subject")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "snapclass-branch.streamlit.app"
    # local_ip = get_local_ip()
    # FIX 1: use local IP instead of localhost so phones can reach it
    # FIX 2: param name is 'join-code' not 'join_code'
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.header(f"Share — {subject_name}")

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind='png', scale=10, border=1)
    out.seek(0)  # FIX 3: reset buffer before reading

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('### Copy Link')
        st.code(join_url, language='text')
        st.markdown('### Subject Code')
        st.code(subject_code, language='text')
        st.info('📱 Make sure your phone is on the same WiFi network')
    with col2:
        st.markdown('### Scan to Join')
        st.image(out.getvalue(), caption='Scan with your phone camera')