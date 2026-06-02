import streamlit as st
import base64
from pathlib import Path

def footer_home():
    logo_path = r"C:\Users\pc\Downloads\Gemini_Generated_Image_e2zkzfe2zkzfe2zk.png"
    
    with open(logo_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; 
                    justify-content:center; margin-bottom:30px; margin-top:30px;">
            <p style="font-weight:bold; color:white;">Created by</p>
            <img src="data:image/png;base64,{encoded}" style="height:150px;"/>
        </div>
    """, unsafe_allow_html=True)