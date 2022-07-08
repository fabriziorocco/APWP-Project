from requests import session
import streamlit as st
import pandas as pd
import json
from apps.window import Window
import time
from utils import sen_generator

"""
This app function is used to load the game the first time from the level 1.
It takes no parameters
"""


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


"""
This is the game file, level 1. Each level has its own page, and they differ only for sentence difficulty level. The whole structure is the same.
The class New sentence creates the subpage and it s tracked by the num.
At the begin of the app, we memorize the time, that will be compared with the final time registered at the end of the level.
The if session state num define the while loop. Once you reach 5, the level is finished. Once the level is completed, a dataframe is
created with the data registered during the game. In particular, speed(time),accuracy and number of trials is registered. 
They are registered in a pre-initialized json Historical. When the user starts to play, the values are set to speed=1000,accuracy=0,trials=1.

At the end of each level, if the accuracy registered is less than 75% the light is red, so the user can't continue and must repeat the level.

While num is less than 5(or 10 or 15 depends on the level(explaination in window.py)) the platform register the data inputed by the user,
the num and the sentence randomly created in a dictionary.

"""

if 'num' not in st.session_state:  # This takes track of the pages.Streamlit is a stateless library, you can just memorize variables among pages.
    st.session_state.num = 1

if 'sentenceinput' not in st.session_state:  # variable sentence input to remember
    st.session_state.sentenceinput = []

if "truesentence" not in st.session_state:  # random sentences
    st.session_state.truesentence = []


class NewSentence:  # This class is the object that control the page creation. The init takes as parameter page id and generate a title and a input placeholder
    def __init__(self, page_id):
        st.title(f"Sentence n°{page_id}")
        self.sentence = st.text_input("Write here the sentence")


def app():
    """
    This function controls the functioning of the page.
    It doesn't take any parameters as input.
    """
    st.session_state.warning = "You must pass the level to go ahead!"
    placeholder = st.empty()  # Remove the content of the placeholder
    placeholder2 = st.empty()  # Remove the content of the placeholder
    t0 = time.time()  # This variable stores the attempts time of the user
    while True:  # This is the loop that controls the whole functioning. It continues to run and contains two main if-else branches to check if the current page number is 5 or <5
        num = st.session_state.num
        if st.session_state.num == 5:
            st.header("Level 1")  # Define a title of the page with the level
            placeholder2.empty()  # Remove the content of the placeholder
            df = pd.DataFrame(
                st.session_state.sentenceinput)  # Create a pandas dataframe to store user inputted sentences
            df["speed"] = (df["time"].iloc[-1] - df["time"].iloc[
                0])  # Create a column for the speed. This column computes the difference of the time the user finish the level
            userWindow = Window(user=st.session_state.Name,
                                level=1)  # Instantiate a Window object that we'll use later to get the accuracy
            df["true_sentence"] = (st.session_state.truesentence[
                                   0::2])  # This is because of a bug. The sentences are registered twice and so we need to slice them twice
            placeholderAccuracy = userWindow.getAccuracy(df["sentence"],
                                                         df["true_sentence"])  # Compute the accuracy in the dataframe
            df["accuracy"] = str(placeholderAccuracy)
            Historical = open(
                'data/Historical.json')  # Open the path the historical JSON. It contains all previous attempts.
            Historical_data = json.load(Historical)  # Load the JSON
            # Update user progresses in a dictionary created by copy the content of the historical JSON. This has been done to avoid problems in writing corrupted things in the JSON.
            Historical_data[st.session_state.Name]["Level1"][0] = df["speed"][0]
            Historical_data[st.session_state.Name]["Level1"][1] = df["accuracy"][0]
            Historical_data[st.session_state.Name]["Level1"][2] += 1
            # Update the real historical JSON
            with open("data/Historical.json", "w") as fp:
                json.dump(Historical_data, fp)
            if "light" in st.session_state:  # The light is the session state mechanism we use to allow users to progress. If the light is green the user can proceed, if red not
                if int(Historical_data[st.session_state.Name]["Level1"][
                           1]) < 3:  # Check the user level. If it's below 3 the user cannot proceed.
                    st.write("You didn't pass the level. Click repeat to try again!")
                    st.session_state.light = "red"  # Set the user state to red
                    df = pd.DataFrame()  # Re initialize the dataframe
                else:
                    st.session_state.light = "green"  # Set the light to green and allow the user to go on
                    st.write("Congratulations! Click next to go to the next level!")
            break
        else:
            # In this branch the user is still progressing over the sentences inside a level

            #load the DL files
            char2int = pickle.load(open(f"data/wonderland.txt-char2int.pickle", "rb"))
            int2char = pickle.load(open(f"data/wonderland.txt-int2char.pickle", "rb"))
            model = keras.models.load_model(f"data/wonderland.txt-100.h5")
            data = sen_generator(1,1,int2char,char2int,model)  #generate a dictionary for level 1 with words of length 1
            #f = open('data/levels.json')  # Open the path of the levels JSON file that contains all the levels
            #data = json.load(f)  # Load the JSON file
            userWindow = Window(user=st.session_state.Name, level=1)  # Instantiate a Window object
            with placeholder.form(key=str(num)):
                random_sentence = userWindow.get_sentence(
                    list(data))  # Generate a sentence from the dictionary created
                st.header(random_sentence)  # Set the sentence as header of the subpage
                st.session_state.truesentence.append(
                    random_sentence)  # Add the sentence to a preeviously created array to be shown at the end for the accuracy computation
                new_sentence = NewSentence(page_id=num)  # Set the placeholder with the NewSentence class
                if st.form_submit_button(
                        'submit'):  # If the user clicks on submit register the inputted sentence of the user
                    st.session_state.sentenceinput.append({
                        'id': num, 'sentence': new_sentence.sentence, "true_sentence": random_sentence,
                        "time": t0})  # Append all the sentence data in a dictionary that in the end we'll use to create the dataframe
                    st.session_state.num += 1  # Increment the counter of the num by 1. This will allow at the next iteration to go over
                    placeholder.empty()  # Remove the content of the placeholder
                    placeholder2.empty()  # Remove the content of the placeholder
                else:
                    st.stop()