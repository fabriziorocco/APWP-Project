import unittest
import json
from window import Window


class TestWindow(unittest.TestCase):

    def __init__(self) -> None:
        super().__init__(Window.__init__)

    def test_getCurrentLevelData(self):
        for key, value in self.levelsData.items():
            if key == self.level:
                self.levelData = value
                return self.levelData
        self.assertIs(self.levelData, list, "Should be a list")
    
    


if __name__ == '__main__':
    unittest.main()