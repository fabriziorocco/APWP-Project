import json
import streamlit as st
from datetime import datetime


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
    f = open('users.json')

    # returns JSON object as a dictionary
    data = json.load(f)

    if name in data.keys():
        st.write("User is already registered!")

    else:
        data["{}".format(name)] = {}
        data["{}".format(name)]["Password"] = password
        data["{}".format(name)]["Level"] = 1
        #data["{}".format(name)]["Registration date"] = datetime.today().strftime('%Y-%m-%d')
        st.write("Welcome to our Platform!. Click Next to start playing!")
        st.session_state.light = "green"
        st.session_state.Level = data[name]["Level"]
        st.session_state.Name = name

        with open("users.json", "w") as fp:
            json.dump(data, fp)