
#File that control the main window
from cmath import e
from typing_extensions import Self
import json
from  pynput import keyboard
#from src.keylogger import check_key, on_release
import time
import random
import streamlit as st

"""
Here is it class window. Fabrizio comments better. I modified get accuracy. I dont use Userinput, but i use get sentence.

"""



class Window ():
    def __init__(self, user, level) -> None:
        self.user = user
        self.level = level
        with open('data/levels.json') as json_file:
            levelsData = json.load(json_file)
        self.levelsData = levelsData

    def getCurrentLevelData(self) -> list:
        for key, value in self.levelsData.items():
            if key == self.level:
                self.levelData = value
                return self.levelData

    def get_sentence(self, listOfSentence):
        sentence = random.choice(listOfSentence)
        return sentence

    def getCurrentSentence(self):
        # The event listener will be running in this block
            # with keyboard.Events() as events:
            #     for event in events:
            #         if event.key == keyboard.Key.space:
            #             self.counter += 1
            #             print(self.counter)
            #             print(self.levelData[self.counter])
            #         else:
            #             print('Received event {}'.format(event))
        with keyboard.Listener(
            on_press=check_key(lst=self.levelData),
            on_release=on_release) as listener:
            listener.join()

    def userInput(self,random_sentence):
        self.userInputtedSentences = []
        a = False
        try:
            t0 = time.time()
            counter = random.randint(0,10000000)
                #sentence = random.choice(self.levelData)
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
        j = 0
        counter = 0
        while j < len(userInputtedSentences):
            if userInputtedSentences[j] == Truesentences[j]:
                counter +=1

            j +=1

        st.write(counter)
        return counter


    def getSpeed(self):
        self.wpm = round(len(self.userInputtedSentences)*60/(5*self.finalTime),2)
        print("WPM: {}".format(self.wpm))
        return self.wpm



    def progressLevel(self):
        if self.accuracy >= 75:
            self.level += 1
            print("Congratulation, you can move to level {} ".format(self.level))
        elif self.accuracy < 75 and self.accuracy > 50:
            print("Don't give up! Keep practicing to progress to the next level")
        else:
            print("Keep practicing! You still have to work")


                
    


if __name__ == "__main__":
    
    a = Window("fabrizio", "test")
    print(a.getCurrentLevelData())
    #print(a.getCurrentSentence())
    print(a.userInput())
    print(a.getAccuracy())
    print(a.getSpeed())