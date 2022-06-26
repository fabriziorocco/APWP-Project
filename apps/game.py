from requests import session
import streamlit as st
import json
from src.window import Window


def app():
    col1h, col2h, col3h = st.columns(3)
    with col1h:
        st.write("Hi {}".format(st.session_state.Name))
    with col3h:
        st.write("Level {}".format(st.session_state.Level))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        start = st.button("Start the Game")
    
    if start:
        userWindow = Window(user=st.session_state.Name, level=st.session_state.Level)
        print(userWindow.getCurrentLevelData())
        userWindow.userInput()

