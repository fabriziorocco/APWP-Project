import streamlit as st
import json
import numpy as np
import pandas as pd

from apps.utils import Authtentication,Sign_up,ranking,stats

"""
This is the page that is displayed when the application is started. It contains the form for both login and sign up.
Like every page,it contains the check for variables in the session state.
The functions used in backend are in utils, here is just the form in streamlit.
"""


if 'Name' not in st.session_state:  #This has been used for testing without doing the authentication.
    st.session_state.Name = "User1"


if 'Info_User' not in st.session_state:  #This has been used for testing without doing the authentication.
    st.session_state.Info_User = "User1"



def app():


    st.session_state.warning= "Please Imput E-mail and Password"
    st.markdown('<h1 style="color: #5b61f9;">Welcome to our typing service!</h1>',
                unsafe_allow_html=True)
    type = st.radio("New User?",options=["Log-in","Sign-up"], index=0)


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



    st.sidebar.title("General statistics of the game")

    st.sidebar.header("Average time per levels")

    column1,column2,column3 = st.sidebar.columns(3)


    speed = stats()[0]
    column1.metric("Level 1", round(speed["Level1"]))
    column2.metric("Level 1", round(speed["Level2"]))
    column3.metric("Level 1", round(speed["Level3"]))



    st.sidebar.header("Average attempts per levels")
    column1,column2,column3 = st.sidebar.columns(3)

    attempts = stats()[1]

    column1.metric("Level 1", round(attempts["Level1"]))
    column2.metric("Level 1", round(attempts["Level2"]))
    column3.metric("Level 1", round(attempts["Level3"]))






    st.sidebar.header("Actual Ranking by levels")
    st.sidebar.write(ranking())











    Info_User = st.sidebar.text_input("Type a name to see the stats of a User")

    a = st.sidebar.button("Go")
    if a:
        st.session_state.Info_User = Info_User
        #st.session_state.page += 4

        jsonStr = open('data/Historical.json')
        # returns JSON object as a dictionary
        jsonStr = json.load(jsonStr)


        if st.session_state.Info_User in list(jsonStr.keys()):
            level_labels = ["Level 1","Level 2","Level 3"]
            levels_speed = [jsonStr[st.session_state.Info_User]["Level1"][0],jsonStr[st.session_state.Info_User]["Level2"][0],jsonStr[st.session_state.Info_User]["Level3"][0]]
            levels_attempts= [jsonStr[st.session_state.Info_User]["Level1"][2],jsonStr[st.session_state.Info_User]["Level2"][2],jsonStr[st.session_state.Info_User]["Level3"][2]]
            levels_accuracy= [int(jsonStr[st.session_state.Info_User]["Level1"][1]),int(jsonStr[st.session_state.Info_User]["Level2"][1]),int(jsonStr[st.session_state.Info_User]["Level3"][1])]


            st.title("Stats of user " + str(st.session_state.Info_User))

            chart_data = pd.DataFrame(
                levels_speed,index=level_labels)

            chart_data1 = pd.DataFrame(
                levels_attempts,index=level_labels)


            chart_data2 = pd.DataFrame(
                levels_accuracy,index=level_labels)


            col1,col2,col3 = st.columns(3)

            col1.write("Speed")
            col1.bar_chart(chart_data)

            col2.write("Attempts")
            col2.bar_chart(chart_data1)


            col3.write("Accuracy out of 4")
            col3.bar_chart(chart_data2)



        else:
            st.sidebar.warning("User not found")












