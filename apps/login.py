import streamlit as st
import json
from apps.utils import Authtentication,Sign_up

"""
This is the page that is displayed when the application is started. It contains the form for both login and sign up.
Like every page,it contains the check for variables in the session state.
The functions used in backend are in utils, here is just the form in streamlit.
"""


if 'Name' not in st.session_state:  #This has been used for testing without doing the authentication.
    st.session_state.Name = "User1"



def app():


    st.session_state.warning= "Please Imput E-mail and Password"
    st.markdown('<h1 style="color: #5b61f9;">Welcome to our typing service!</h1>',
                unsafe_allow_html=True)
    type= st.radio("New User?",options=["Log-in","Sign-up"], index=0)


    if type == "Log-in":
        user= st.text_input("Username")
        password= st.text_input("Password", type="password")

        a = st.button("Log-in")
        if a:
            Authtentication(user, password)

    elif type == "Sign-up":
        user= st.text_input("Username")
        password= st.text_input("Password", type="password")
        password2 = st.text_input("Write again the Password", type="password")
        a = st.button("Sign-up")
        if a:
            Sign_up(user,password)







