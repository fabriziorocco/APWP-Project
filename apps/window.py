#File that control the main window
from cmath import e
from typing_extensions import Self
import json
import time
import random
import streamlit as st

"""
This is the Window class. It handles the backend logic of our application.
"""

class Window ():
    def __init__(self, user, level) -> None:
        """
        This construtor takes as parameters the username and the user level from the JSON data file.
        Moreover, it loads the dictionary with all the levels into a variable called levelsData
        """
        self.user = user
        self.level = level
        with open('data/levels.json') as json_file:
            levelsData = json.load(json_file)
        self.levelsData = levelsData


    def getCurrentLevelData(self) -> list:
        """
        This function iterates over the previously created dictionary and takes only the sentences from the level of the user:
        (for example if the user is at level 3, this function will return a list with only the sentences from level 3)
        It returns a list containing the sentences
        """
        for key, value in self.levelsData.items():
            if key == self.level:
                self.levelData = value
                return self.levelData


    def get_sentence(self, listOfSentence):
        """
        Get a random sentence from the list         
        """
        sentence = random.choice(listOfSentence)
        return sentence


    def userInput(self,random_sentence):
        """
        this function asks the user to continuoosly write a sentence while printing each sentence of the level.
        When it is completed, the function returns the total time to complete the level
        """
        self.userInputtedSentences = []
        a = False
        try:
            t0 = time.time()
            counter = random.randint(0,10000000)
            sentenceInputted = st.text_input(random_sentence,key=str(counter))

            #key to unique widget
            if sentenceInputted:
                self.userInputtedSentences.append(sentenceInputted.lower())


        except Exception as e :
            print(e)

        t1 = time.time()
        self.finalTime = round(t1-t0,2)
        print("{} seconds to finish the level".format(self.finalTime))
        return self.finalTime,self.userInputtedSentences


    def getAccuracy(self,userInputtedSentences,Truesentences):
        """
        This function computes the user's accuracy.
        To do so, it compares all the words of the real sentences vs the inputted sentences.
        After that, it computes and returns the proportion of correct words.
        """
        j = 0
        counter = 0
        while j < len(userInputtedSentences):
            if userInputtedSentences[j] == Truesentences[j]:
                counter +=1

            j +=1

        st.write(counter)
        return counter


    def getSpeed(self):
        """
        This function computes the user's speed.
        We assume a number of 5 characters per word.
        We multiply the user's sentences by 60 (1 hour) and we divide it by the time elapsed * 5.
        """
        self.wpm = round(len(self.userInputtedSentences)*60/(5*self.finalTime),2)
        print("WPM: {}".format(self.wpm))
        return self.wpm


    def progressLevel(self):
        """
        This function handles user's progresses. 
        It checks if the accuraacy is above 75% and if so, allows the user to move to the next level.
        Otherwise it prints some warnings.
        """
        if self.accuracy >= 75:
            self.level += 1
            print("Congratulation, you can move to level {} ".format(self.level))
        elif self.accuracy < 75 and self.accuracy > 50:
            print("Don't give up! Keep practicing to progress to the next level")
        else:
            print("Keep practicing! You still have to work")


                
