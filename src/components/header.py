# src/components/header.py
import streamlit as st
import base64
import os

LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "logo.png")

def _get_encoded_logo():
    with open(LOGO_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode()


def header_home():
    encoded = _get_encoded_logo()
    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center;
                    justify-content:center; margin-bottom:30px; margin-top:30px;">
            <img src="data:image/png;base64,{encoded}" style="height:100px;"/>
            <h1 style="text-align:center; color:#E0E3FF;">SNAP<br/>CLASS</h1>
        </div>
    """, unsafe_allow_html=True)


def header_dashboard():
    encoded = _get_encoded_logo()
    st.markdown(f"""
        <div style="display:flex; flex-direction:row; align-items:center;
                    gap:12px; justify-content:flex-start; margin-bottom:10px;">
            <img src="data:image/png;base64,{encoded}" style="height:65px; border-radius:12px;"/>
            <h2 style="color:#5865F2; margin:0;">SNAP<br/>CLASS</h2>
        </div>
    """, unsafe_allow_html=True)