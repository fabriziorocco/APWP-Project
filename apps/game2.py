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

        st.title(f"Sentence n°{page_id-4}")

        self.sentence = st.text_input("Write here the sentence")


def app():



    placeholder = st.empty()
    placeholder2 = st.empty()

    t0 = time.time()




    while True:

        num = st.session_state.num

        if st.session_state.num ==10:
            st.markdown('<h1 style="color: #5b61f9;">Level 2</h1>',
                        unsafe_allow_html=True)
            placeholder2.empty()
            df = pd.DataFrame(st.session_state.sentenceinput)
            df["speed"] = (df["time"].iloc[-1] - df["time"].iloc[0])

            userWindow = Window(user=st.session_state.Name, level=2)
            df["true_sentence"] = (st.session_state.truesentence[0::2])  #QUESTO PERCHE SFACIOLA LE PAGINE

            a = userWindow.getAccuracy(list(df["sentence"].iloc[-4:]), list(df["true_sentence"].iloc[-4:]))
            df["accuracy"] = str(a)

            Historical = open('data/Historical.json')


            # returns JSON object as a dictionary
            Historical_data = json.load(Historical)


            Historical_data[st.session_state.Name]["Level2"][0] = df["speed"][0]
            Historical_data[st.session_state.Name]["Level2"][1] = df["accuracy"][0]
            Historical_data[st.session_state.Name]["Level2"][2] += 1



            with open("data/Historical.json", "w") as fp:
                json.dump(Historical_data, fp)


            if "light" in st.session_state:
                if int(Historical_data[st.session_state.Name]["Level2"][1]) < 3:
                    st.markdown('<h3 style="color: #ff0000;">You did not pass the level! Please click repeat!</h3>',
                                unsafe_allow_html=True)
                    st.session_state.light = "red"
                    df = pd.DataFrame()


                else:
                    st.session_state.light = "green"
                    st.markdown('<h3 style="color: #006400;">Congratulations! Click next to go to the next level!</h3>',
                                unsafe_allow_html=True)










            break
        else:
            char2int = pickle.load(open(f"data/wonderland.txt-char2int.pickle", "rb"))
            int2char = pickle.load(open(f"data/wonderland.txt-int2char.pickle", "rb"))
            model = keras.models.load_model(f"data/wonderland.txt-100.h5")
            data = sen_generator(2,2,int2char,char2int,model)
            #f = open('data/levels.json')
            #data = json.load(f)
            userWindow = Window(user=st.session_state.Name, level=2)


            with placeholder.form(key=str(num)):

                random_sentence = userWindow.get_sentence(list(data))
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