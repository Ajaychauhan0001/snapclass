# src/ui/base_layout.py
import streamlit as st

def style_background_home():
    st.markdown("""
        <style>
            .stApp {
                background-color: #5865F2 !important;
            }
            .stApp div[data-testid="stColumn"] {
                background-color: #E0E3FF !important;
                padding: 2rem !important;
                border-radius: 5rem !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    st.markdown("""
        <style>
            .stApp {
                background-color: #E0E3FF !important;
            }
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');

        #MainMenu, footer, header { visibility: hidden; }

        .block-container { padding-top: 1.5rem !important; }
        
        h1 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 3.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
            color: #1A1A2E !important; /* Optional: Keep h1 dark too if needed */
        }
        h2 {
            font-family: 'Climate Crisis', sans-serif !important;
            font-size: 2rem !important;
            line-height: 0.9 !important;
            margin-bottom: 0rem !important;
            color: #1A1A2E !important; 
        }
        h3, h4, p {
            font-family: 'Outfit', sans-serif !important;
            color: #1A1A2E !important; /* <-- This fixes the "Welcome" text and footer paragraph */
        }

        /* ── Fixes Select Subject and other input labels ── */
        div[data-testid="stWidgetLabel"] p {
            color: #1A1A2E !important; /* Forces dropdown label to be dark charcoal */
            font-weight: 600 !important;
        }

        # h1 {
        #     font-family: 'Climate Crisis', sans-serif !important;
        #     font-size: 3.5rem !important;
        #     line-height: 1.1 !important;
        #     margin-bottom: 0rem !important;
        # }
        # h2 {
        #     font-family: 'Climate Crisis', sans-serif !important;
        #     font-size: 2rem !important;
        #     line-height: 0.9 !important;
        #     margin-bottom: 0rem !important;
        #     color: #1A1A2E !important;
        # }
        # h3, h4, p {
        #     font-family: 'Outfit', sans-serif !important;
        # }

        /* ── Buttons (correct CSS selectors) ── */
        
        /* ── Buttons (correct CSS selectors) ── */
        div.stButton > button {
            border-radius: 1.5rem !important;
            background-color: #5865F2 !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            font-family: 'Outfit', sans-serif !important;
            transition: transform 0.25s ease-in-out !important;
        }
        
        /* ── ADD THIS NEW BLOCK TO FORCE BUTTON TEXT TO BE WHITE ── */
        div.stButton > button p {
            color: white !important;
        }
        
        div.stButton > button[kind="secondary"] {
            background-color: #EB459E !important;
            color: white !important;
        }
        div.stButton > button[kind="tertiary"] {
            background-color: black !important;
            color: white !important;
        }
        
        
        
        # div.stButton > button {
        #     border-radius: 1.5rem !important;
        #     background-color: #5865F2 !important;
        #     color: white !important;
        #     padding: 10px 20px !important;
        #     border: none !important;
        #     font-family: 'Outfit', sans-serif !important;
        #     transition: transform 0.25s ease-in-out !important;
        # }
        # div.stButton > button[kind="secondary"] {
        #     background-color: #EB459E !important;
        #     color: white !important;
        # }
        # div.stButton > button[kind="tertiary"] {
        #     background-color: black !important;
        #     color: white !important;
        # }
        # div.stButton > button:hover {
        #     transform: scale(1.05) !important;
        # }
        # </style>
    """, unsafe_allow_html=True)