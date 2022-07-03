import streamlit as st
import pandas as pd
import json
from apps.window import Window
import time



if 'sentenceinput' in st.session_state: #variable sentence input to remember
    st.session_state.sentenceinput = []

if "truesentence" in st.session_state:  #random sentences
    st.session_state.truesentence = []


if "st.session_state.num" in st.session_state:
    st.session_state.num = 1




class NewSentence:  #this create the pages
    def __init__(self, page_id):

        st.title(f"Sentence n°{page_id-9}")

        self.sentence = st.text_input("Write here the sentence")


def app():



    placeholder = st.empty()
    placeholder2 = st.empty()

    t0 = time.time()




    while True:

        num = st.session_state.num


        if st.session_state.num ==15:
            st.header("Level 3")
            placeholder2.empty()
            df = pd.DataFrame(st.session_state.sentenceinput)
            df["speed"] = (df["time"].iloc[-1] - df["time"].iloc[0])

            userWindow = Window(user=st.session_state.Name, level=3)
            df["true_sentence"] = (st.session_state.truesentence[0::2])  #QUESTO PERCHE SFACIOLA LE PAGINE

            a = userWindow.getAccuracy(list(df["sentence"].iloc[-4:]), list(df["true_sentence"].iloc[-4:]))
            df["accuracy"] = str(a)

            Historical = open('data/Historical.json')


            # returns JSON object as a dictionary
            Historical_data = json.load(Historical)


            Historical_data[st.session_state.Name]["Level3"][0] = df["speed"][0]
            Historical_data[st.session_state.Name]["Level3"][1] = df["accuracy"][0]
            Historical_data[st.session_state.Name]["Level3"][2] += 1






            with open("data/Historical.json", "w") as fp:
                json.dump(Historical_data, fp)


            if float(Historical_data[st.session_state.Name]["Level3"][1]) < 3:
                st.write("You didn't pass the level. Click repeat to try again!")

                df = pd.DataFrame()


            else:
                st.balloons()
                st.title("Congratulations! You finished the game.")




            break
        else:


            f = open('data/levels.json')
            data = json.load(f)
            userWindow = Window(user=st.session_state.Name, level=3)


            with placeholder.form(key=str(num)):

                random_sentence = userWindow.get_sentence(data[str(3)])
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