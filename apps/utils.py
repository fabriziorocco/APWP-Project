import json
import streamlit as st
from datetime import datetime


"""
In this file we create the functions to log in and sign up. The users are registerd in a json composed by name and password.
The check is very easy and regulated by the variable light.
When a user signed, also his historical is initialized. Every time the user plays, its stats are updated, apart of number of trials.
"""


def Authtentication(name, password):
    f = open('data/users.json')

    # returns JSON object as a dictionary
    data = json.load(f)

    if name in data.keys():
        if password == data[name]["Password"]:
            session_state = "green"
            st.write("Welcome. Click Next to start playing!")
            st.session_state.light = "green"
            st.session_state.Level = data[name]["Level"]
            st.session_state.Name = name

        else:
            st.write("Password incorrect!")

    else:
        st.write("Username not registered!")


def Sign_up(name, password):
    f = open('data/users.json')

    # returns JSON object as a dictionary
    data = json.load(f)




    if name in data.keys():
        st.write("User is already registered!")

    else:
        data["{}".format(name)] = {}
        data["{}".format(name)]["Password"] = password
        data["{}".format(name)]["Level"] = 1
<<<<<<< HEAD
        #data["{}".format(name)]["Registration date"] = datetime.today().strftime('%Y-%m-%d')
=======
>>>>>>> f358277d (Interface bulding with most of the functionalities of the game. Also comments added per page.)
        st.write("Welcome to our Platform!. Click Next to start playing!")
        st.session_state.light = "green"
        st.session_state.Level = data[name]["Level"]
        st.session_state.Name = name

        with open("data/users.json", "w") as fp:
            json.dump(data, fp)

        Historical = open('data/Historical.json')

        # returns JSON object as a dictionary
        Hist_data = json.load(Historical)

        Hist_data["{}".format(name)] = {}
        Hist_data["{}".format(name)]["Level1"] = [1000,0,0]  #time,accuracy,attempts
        Hist_data["{}".format(name)]["Level2"] = [1000,0,0]
        Hist_data["{}".format(name)]["Level3"] = [1000, 0,0]

        with open("data/Historical.json", "w") as fp:
            json.dump(Hist_data, fp)
