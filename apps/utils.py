import json
import streamlit as st
from datetime import datetime
import pandas as pd

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

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

#<<<<<<< HEAD
        #data["{}".format(name)]["Registration date"] = datetime.today().strftime('%Y-%m-%d')
#=======
#>>>>>>> f358277d (Interface bulding with most of the functionalities of the game. Also comments added per page.)
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




def ranking():
    jsonStr = open('data/Historical.json')
    # returns JSON object as a dictionary
    jsonStr = json.load(jsonStr)

    for el in jsonStr.keys():
        if (jsonStr[el]["Level3"][0]) != 1000:
            jsonStr[el]["Level3"][0] = jsonStr[el]["Level3"][0] - jsonStr[el]["Level2"][0]

        if (jsonStr[el]["Level2"][0]) != 1000:
            jsonStr[el]["Level2"][0] = jsonStr[el]["Level2"][0] - jsonStr[el]["Level1"][0]


    levels3 = []
    for el in jsonStr.keys():
        if (jsonStr[el]["Level3"][0]) != 1000:  # take the peolpe that did the level 3
            levels3.append([el, jsonStr[el]["Level3"][0], 3])

    levels2 = []
    for el in jsonStr.keys():
        if (jsonStr[el]["Level3"][0]) == 1000:
            if (jsonStr[el]["Level2"][0]) != 1000:
                levels2.append([el, jsonStr[el]["Level2"][0], 2])

    levels1 = []

    for el in jsonStr.keys():
        if (jsonStr[el]["Level3"][0]) == 1000:
            if (jsonStr[el]["Level2"][0]) == 1000:
                if (jsonStr[el]["Level1"][0]) != 1000:
                    levels1.append([el, jsonStr[el]["Level1"][0], 1])

    df = pd.DataFrame(columns=["Name", "Level", "Time"])

    for el in levels3:
        dict = {"Name": el[0], "Level": el[2], "Time": el[1]}
        df = df.append(dict, ignore_index=True)

    for el in levels2:
        dict = {"Name": el[0], "Level": el[2], "Time": el[1]}
        df = df.append(dict, ignore_index=True)

    for el in levels1:
        dict = {"Name": el[0], "Level": el[2], "Time": el[1]}
        df = df.append(dict, ignore_index=True)

    return df


def stats():
    jsonStr = open('data/Historical.json')
    # returns JSON object as a dictionary
    jsonStr = json.load(jsonStr)

    Usersl = []
    Users = 0
    for el in jsonStr.keys():
        Users += 1
    Usersl.append(Users)

    times_1 = []
    times_2 = []
    times_3 = []

    for el in jsonStr.keys():
        if (jsonStr[el]["Level3"][0]) != 1000:
            jsonStr[el]["Level3"][0] = jsonStr[el]["Level3"][0] - jsonStr[el]["Level2"][0]

        if (jsonStr[el]["Level2"][0]) != 1000:
            jsonStr[el]["Level2"][0] = jsonStr[el]["Level2"][0] - jsonStr[el]["Level1"][0]

    for el in jsonStr.keys():
        if jsonStr[el]["Level1"][0] != 1000:
            times_1.append(jsonStr[el]["Level1"][0])

    for el in jsonStr.keys():
        if jsonStr[el]["Level2"][0] != 1000:
            times_2.append(jsonStr[el]["Level2"][0])

    for el in jsonStr.keys():
        if jsonStr[el]["Level3"][0] != 1000:
            times_3.append(jsonStr[el]["Level3"][0])

    times_1_l = []
    times_2_l = []
    times_3_l = []

    times_1_l.append(sum(times_1) / len(times_1))
    times_2_l.append(sum(times_2) / len(times_2))
    times_3_l.append(sum(times_3) / len(times_3))

    df_Levels = pd.DataFrame()
    df_Levels["Users"] = Usersl
    df_Levels["Level1"] = times_1_l
    df_Levels["Level2"] = times_2_l
    df_Levels["Level3"] = times_3_l

    attempt_1 = []
    attempt_2 = []
    attempt_3 = []

    for el in jsonStr.keys():
        if jsonStr[el]["Level1"][0] != 1000:
            attempt_1.append(jsonStr[el]["Level1"][2])

    for el in jsonStr.keys():
        if jsonStr[el]["Level2"][0] != 1000:
            attempt_2.append(jsonStr[el]["Level2"][2])

    for el in jsonStr.keys():
        if jsonStr[el]["Level3"][0] != 1000:
            attempt_3.append(jsonStr[el]["Level3"][2])

    attempt_1l = []
    attempt_2l = []
    attempt_3l = []

    attempt_1l.append(sum(attempt_1) / len(attempt_1))
    attempt_2l.append(sum(attempt_2) / len(attempt_2))
    attempt_3l.append(sum(attempt_3) / len(attempt_3))

    df_att = pd.DataFrame()
    df_att["Level1"] = attempt_1l
    df_att["Level2"] = attempt_2l
    df_att["Level3"] = attempt_3l

    return (df_Levels,df_att)





"""
Plotting of the number of attempts per level per user
"""

