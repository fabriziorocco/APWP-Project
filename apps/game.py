from requests import session
import streamlit as st
import pandas as pd
import json
from apps.window import Window
import time


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


if 'num' not in st.session_state:  #This takes track of the pages.Streamlit is a stateless library, you can just memorize variables among pages.
    st.session_state.num = 1

if 'sentenceinput' not in st.session_state: #variable sentence input to remember
    st.session_state.sentenceinput = []

if "truesentence" not in st.session_state:  #random sentences
    st.session_state.truesentence = []







class NewSentence:  #this create the pages
    def __init__(self, page_id):

        st.title(f"Sentence n°{page_id}")

        self.sentence = st.text_input("Write here the sentence")


def app():
    st.session_state.warning = "You must pass the level to go ahead!"


    placeholder = st.empty()
    placeholder2 = st.empty()

    t0 = time.time()




    while True:

        num = st.session_state.num

        if st.session_state.num ==5:

            st.header("Level 1")
            placeholder2.empty()
            df = pd.DataFrame(st.session_state.sentenceinput)
            df["speed"] = (df["time"].iloc[-1] - df["time"].iloc[0])

            userWindow = Window(user=st.session_state.Name, level=1)
            df["true_sentence"] = (st.session_state.truesentence[0::2])  #This is because of a bug. The sentences are registered twice.

            a = userWindow.getAccuracy(df["sentence"], df["true_sentence"])
            df["accuracy"] = a

            Historical = open('data/Historical.json')


            # returns JSON object as a dictionary
            Historical_data = json.load(Historical)



            Historical_data[st.session_state.Name]["Level1"][0] = df["speed"][0]
            Historical_data[st.session_state.Name]["Level1"][1] = df["accuracy"][0]
            Historical_data[st.session_state.Name]["Level1"][2] += 1






            with open("data/Historical.json", "w") as fp:
                json.dump(Historical_data, fp)





            if "light" in st.session_state:
                if float(Historical_data[st.session_state.Name]["Level1"][1].split()[1][:-1]) < 75:
                    st.write("You didn't pass the level. Click repeat to try again!")
                    st.session_state.light = "red"
                    df = pd.DataFrame()

                else:
                    st.session_state.light = "green"
                    st.write("Congratulations! Click next to go to the next level!")






            break
        else:

            f = open('data/levels.json')
            data = json.load(f)
            userWindow = Window(user=st.session_state.Name, level=1)


            with placeholder.form(key=str(num)):

                random_sentence = userWindow.get_sentence(data[str(1)])
                st.header(random_sentence)

                st.session_state.truesentence.append(random_sentence)



                new_sentence = NewSentence(page_id=num)


                if st.form_submit_button('submit'):

                    st.session_state.sentenceinput.append({
                        'id': num, 'sentence': new_sentence.sentence, "true_sentence": random_sentence, "time":t0})
                    st.session_state.num += 1
                    placeholder.empty()
                    placeholder2.empty()
                else:
                    st.stop()