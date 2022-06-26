import streamlit as st
from multiapp import MultiApp
from apps import login,game,utils # import your app modules here
from src.movements import next_page, previous_page, get_to_login
import base64
#INITIALIZE SESSION STATE
if "selected_var" not in st.session_state:
    st.session_state.selected_var=[]
if 'page' not in st.session_state:
    st.session_state.page = 0
if "light" not in st.session_state:
    st.session_state.light= "red"
if "warning" not in st.session_state:
    st.session_state.warning= "Undefined Error"
if "user" not in st.session_state:
    st.session_state.user= "User1"
if "page_name" not in st.session_state:
    st.session_state.page_name= "login"

if "new_user_succesfully_signed_in" not in st.session_state:
    st.session_state.new_user_succesfully_signed_in="no"
######################################################################

#Multiapp Initialization

app = MultiApp()
# st.markdown("""
# # Churn Prediction App
#
# This multi-page app is automatizing the creation of Churn prediction ML models
# """)
# Add all your application here
app.add_app("Login", login.app)
app.add_app("Game",game.app)
#app.add_app("Train Prediction Selection",train_pred_selection.app)
# The main app
app.run()

#Move through the pages


if st.session_state.page_name!= "Game":
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            next = st.button('Next',on_click= next_page)


