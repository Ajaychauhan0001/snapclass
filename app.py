import streamlit as st

from src.screen.home_screen import Home_screen
from src.screen.Student_screen import Student_screen
from src.screen.Teachers_screen import Teacher_screen

def main():
    if 'login_type' not in st.session_state:
        st.session_state['login_type'] = None
        
    match st.session_state['login_type']:
        case 'Teacher':
            Teacher_screen()
            
        case 'Student':
            Student_screen()
            
        case None:
            Home_screen()        
            
main()