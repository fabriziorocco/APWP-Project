'Importing required libraries'

import json
import streamlit as st
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from essential_generators import DocumentGenerator
from essential_generators import MarkovWordGenerator
from essential_generators import MarkovTextGenerator
import numpy as np
import tqdm
import json
import re
import pickle
import keras

"""
In this file we create the functions to log in and sign up. The users are registerd in a json composed by name and password.
The check is very easy and regulated by the variable light.
When a user signed, also his historical is initialized. Every time the user plays, its stats are updated, apart of number of trials.

Also, this file contains all the external functions called in the game. Among them, there are the rankings and stats functions and deep learning text generation part.
"""


def Authtentication(name, password):
    f = open('data/users.json')  #open and load the json

    # returns JSON object as a dictionary
    data = json.load(f)

    if name in data.keys():  #check if the user exists
        if password == data[name]["Password"]: #check if the password is correct
            session_state = "green"  #light green allows to go on on the app
            st.write("Welcome. Click Next to start playing!")
            st.session_state.light = "green"
            st.session_state.Level = data[name]["Level"]  #register the level
            st.session_state.Name = name

        else:
            st.write("Password incorrect!")  #light is still red here and the user can see the error

    else:
        st.write("Username not registered!")  #second condition error


#This function takes name and password and register them in the json if they're not already there.
def Sign_up(name, password):
    f = open('data/users.json')  #open and load the json data

    # returns JSON object as a dictionary
    data = json.load(f)




    if name in data.keys():
        st.write("User is already registered!")  #check if the user is already registered with the name

    else:
        data["{}".format(name)] = {} #create a new nested key and fill the data
        data["{}".format(name)]["Password"] = password
        data["{}".format(name)]["Level"] = 1

#<<<<<<< HEAD
        #data["{}".format(name)]["Registration date"] = datetime.today().strftime('%Y-%m-%d')
#=======
#>>>>>>> f358277d (Interface bulding with most of the functionalities of the game. Also comments added per page.)
        st.write("Welcome to our Platform!. Click Next to start playing!")
        st.session_state.light = "green"  #you can go on
        st.session_state.Level = data[name]["Level"] #register the data
        st.session_state.Name = name

        with open("data/users.json", "w") as fp:
            json.dump(data, fp)  #update the json with the new user

        Historical = open('data/Historical.json')

        # returns JSON object as a dictionary
        Hist_data = json.load(Historical)


        #Initialization of the user historical data with default values
        Hist_data["{}".format(name)] = {}
        Hist_data["{}".format(name)]["Level1"] = [1000,0,0]  #time,accuracy,attempts
        Hist_data["{}".format(name)]["Level2"] = [1000,0,0]
        Hist_data["{}".format(name)]["Level3"] = [1000, 0,0]

        with open("data/Historical.json", "w") as fp:
            json.dump(Hist_data, fp)




#This function create the ranking table. If a user is at level 3 then it's register only in the level 3, and same for level 2 and level 1 consequently.
def ranking():  #Ranking function
    jsonStr = open('data/Historical.json') #open and load data
    # returns JSON object as a dictionary
    jsonStr = json.load(jsonStr)

    for el in jsonStr.keys():  #iterate over users
        if (jsonStr[el]["Level3"][0]) != 1000:  #check if the user has played this level
            jsonStr[el]["Level3"][0] = jsonStr[el]["Level3"][0] - jsonStr[el]["Level2"][0]  #The speed is registered together for all levels. Then the speed of level x is the the speed of level x - speed of level x-1.

        #same for level 2
        if (jsonStr[el]["Level2"][0]) != 1000:
            jsonStr[el]["Level2"][0] = jsonStr[el]["Level2"][0] - jsonStr[el]["Level1"][0]


    #register all the data of the speed. If the user played level 3, then is registered level 3 and its speed, and then for all the levels to create a rank.
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

    #Create a dataframe
    df = pd.DataFrame(columns=["Name", "Level", "Time"])

    #update the dataframe with all the levels
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

#Function Stats for the search bar. This function take the input of the user in the homepage and return stats about the speed, attempts.
def stats():
    jsonStr = open('data/Historical.json') #load json data
    # returns JSON object as a dictionary
    jsonStr = json.load(jsonStr)

    #number of users in the platform
    Usersl = []
    Users = 0
    for el in jsonStr.keys():
        Users += 1
    Usersl.append(Users)

    #if the user played one level(value is not default), append the corrisponding speed and then compute the average. This for each level.
    times_1 = []
    times_2 = []
    times_3 = []

#Usual check of existence in the level by checking the default values.
    for el in jsonStr.keys():
        if (jsonStr[el]["Level3"][0]) != 1000:
            jsonStr[el]["Level3"][0] = jsonStr[el]["Level3"][0] - jsonStr[el]["Level2"][0]

        if (jsonStr[el]["Level2"][0]) != 1000:
            jsonStr[el]["Level2"][0] = jsonStr[el]["Level2"][0] - jsonStr[el]["Level1"][0]

    for el in jsonStr.keys():
        if jsonStr[el]["Level1"][0] != 1000:
            times_1.append(jsonStr[el]["Level1"][0])  #list of speed

    for el in jsonStr.keys():
        if jsonStr[el]["Level2"][0] != 1000:
            times_2.append(jsonStr[el]["Level2"][0]) #list of speed

    for el in jsonStr.keys():
        if jsonStr[el]["Level3"][0] != 1000:
            times_3.append(jsonStr[el]["Level3"][0]) #list of speed

    times_1_l = []  #average lists to put inside the df
    times_2_l = []
    times_3_l = []

    times_1_l.append(sum(times_1) / len(times_1)) #average
    times_2_l.append(sum(times_2) / len(times_2))
    times_3_l.append(sum(times_3) / len(times_3))

    #compute the dataframe for speed
    df_Levels = pd.DataFrame()
    df_Levels["Users"] = Usersl
    df_Levels["Level1"] = times_1_l
    df_Levels["Level2"] = times_2_l
    df_Levels["Level3"] = times_3_l

    #For attemps is exactly the same
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

    return (df_Levels,df_att)  #0 and 1 output in the login page



def main_generator():
    '''
    Function that generates 3 dictionaries of sentences for the app.
    Output (json):
    3 JSON files, each with 10 different sentences for the 3 levels of difficulty of the app.'''

    # Loading required data and model weights
    char2int = pickle.load(open(f"data/wonderland.txt-char2int.pickle", "rb"))
    int2char = pickle.load(open(f"data/wonderland.txt-int2char.pickle", "rb"))
    model = keras.models.load_model(f"data/wonderland.txt-100.h5")

    # Creating JSON file for the first level of difficulty of the game, with 10 sentences of 30 characters each.
    sen_level1 = sen_generator(30, 1, int2char, char2int, model)
    create_json(sen_level1, 'sen_level1')

    # Creating JSON file for the second level of difficulty of the game, with 10 sentences of 60 characters each.
    sen_level2 = sen_generator(60, 2, int2char, char2int, model)
    create_json(sen_level2, 'sen_level2')

    # Creating JSON file for the third level of difficulty of the game, with 10 sentences of 90 characters each.
    sen_level3 = sen_generator(90, 3, int2char, char2int, model)
    create_json(sen_level3, 'sen_level3')


def create_json(dict, name):
    '''
    Function to create a JSON file and save it in the data folder.
    Parameters:
    dict (dictionary): Includes the sentences generated as keys and the levels they correspond to as values.
    name (string): Name of the JSON file to be created.
    Output (json):
    JSON file generated and saved in the data folder.'''

    jsonString = json.dumps(dict)
    jsonFile = open("data/{}.json".format(name), "w")
    jsonFile.write(jsonString)
    jsonFile.close()

def seed_generator():
    '''
    Function to generate a sentence using the Markov generator, transform it to lowercase and remove any punctuation marks from it.
    Output:
    seed (string): Sentence from the Markov generator without punctuation marks and in lowercase.'''

    gen = DocumentGenerator(text_generator=MarkovTextGenerator(), word_generator=MarkovWordGenerator())
    seed = str.lower(gen.sentence())
    seed = re.sub(r'[^\w\s]', '', seed)
    return seed

def sen_generator(n_chars, l, int2char, char2int, model):
    '''
    Funtion that generates a dictionary of 10 sentences for the app.

    Parameters:
    n_chars (int): Amount of characters requires for the generation of a sentence.
    l (int): Level of difficulty from the app to which the generated sentences correspond to.
    int2char (dict pickle file): Dictionary with characters from data source (book) converted to integers.
    char2int (dict pickle file): Dictionary with integers from data source (book) converted to characters.
    model (h5 file): File that contains the saved loaded weights of the model developed in the python notebook from the repository.

    Output:
    dict_sentences (dict): Dictionary of 10 sentences generated as keys and the level of difficulty (l) from the parameters as values.'''

    vocab_size = len(char2int)
    sequence_length = 100
    seed = seed_generator()
    sentences = []
    for i in range(0, 10):
        generated = ""
        for i in tqdm.tqdm(range(n_chars), "Generating text"):
            # Creating the input sequence
            X = np.zeros((1, sequence_length, vocab_size))
            for t, char in enumerate(seed):
                X[0, (sequence_length - len(seed)) + t, char2int[char]] = 1
            # Predicting the next character.
            predicted = model.predict(X, verbose=0)[0]
            # Converting the vector to an integer.
            next_index = np.argmax(predicted)
            # Converting the integer to a character.
            next_char = int2char[next_index]
            # Adding the character to results 'generated'.
            generated += next_char
            # Shifting seed and the predicted character.
            seed = seed[1:] + next_char
        # Removing '\' symbol.
        generated = re.sub(r'\n', '', generated)
        sentences.append(generated)
    # Creating another seed for the next sentence.
    seed = seed_generator()
    # Converting list of 10 sentences into a dictionary.
    dict_sentences = {sentences[0]: 1}
    for i in sentences:
        dict_2 = {i: l}
        dict_sentences.update(dict_2)
    return dict_sentences



