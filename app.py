import streamlit as st
from multiapp import MultiApp
<<<<<<< HEAD
from apps import login,game,utils # import your app modules here
from src.movements import next_page, previous_page, get_to_login
=======
from apps import login,game,utils,game2,game3 # import your app modules here
from src.movements import next_page,retry
>>>>>>> f358277d (Interface bulding with most of the functionalities of the game. Also comments added per page.)
import base64


#This is the "core" of the app. In this file we initialize all the variables we need in the game. We call the multiapp function to initialize
#and we add all the pages of the app.
#The latest lines define some costraints derived by the movements. If we are in the last page(last level) the next button won't be present.
#Also, the button repeat won't be present in the login page.
#For the rest, every page will have the next and repeat button. The next button is regulated by the variable light(green,red). Repeat is always avaliable.




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

if 'num' not in st.session_state:
    st.session_state.num = 1

if 'sentenceinput' not in st.session_state:
    st.session_state.sentenceinput = []

if "truesentence" not in st.session_state:
    st.session_state.truesentence = []

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
app.add_app("Game2",game2.app)
app.add_app("Game3",game3.app)
#app.add_app("Train Prediction Selection",train_pred_selection.app)
# The main app
app.run()

#Move through the pages


if st.session_state.page_name!= "Game3":
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            next = st.button('Next',on_click= next_page)


if st.session_state.page_name != "Login":
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            repeat = st.button('Repeat', on_click=retry, key=2)


