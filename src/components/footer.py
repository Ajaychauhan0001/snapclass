import streamlit as st

def footer_home():
    st.markdown(
        """
        <div style="text-align:center; margin-top:30px;">
            <p style="font-weight:bold;">Created by AJAY CHAUHAN</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def footer_dashboard():
    footer_home()