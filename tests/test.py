import unittest
import json
from window import Window
import random


class TestWindow(unittest.TestCase):

    def __init__(self) -> None:
        super().__init__(Window.__init__)

    def test_getCurrentLevelData(self):
        for key, value in self.levelsData.items():
            if key == self.level:
                self.levelData = value
                return self.levelData
        self.assertIs(self.levelData, list, "Should be a list")
    
    def test_get_sentence(self, listOfSentence):
        sentence = random.choice(listOfSentence)
        self.assertIs(sentence, str, "Should be a string")

    def getSpeed(self):
        self.wpm = round(len(self.userInputtedSentences)*60/(5*self.finalTime),2)
        print("WPM: {}".format(self.wpm))
        self.assertIs(self.wpm, float, "Should be a float")
    
    


if __name__ == '__main__':
    unittest.main()