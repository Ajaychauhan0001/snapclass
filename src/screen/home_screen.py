import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.components.footer import footer_home


def Home_screen(): 
    header_home()
    style_background_home()
    style_base_layout()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("I am Student")
        st.image(r"C:\Users\pc\Downloads\Gemini_Generated_Image_wuacj4wuacj4wuac.png", width=120)
        if st.button('Student Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'Student'   # ← lowercase
            st.rerun() 
        
    with col2:
        st.header("I am Teacher")
        st.image(r"C:\Users\pc\Downloads\Gemini_Generated_Image_sdc7hxsdc7hxsdc7.png", width=130)
        if st.button('Teacher Portal', type='primary', icon=':material/arrow_outward:', icon_position='right'):
            st.session_state['login_type'] = 'Teacher'   # ← lowercase
            st.rerun()
            
    footer_home()