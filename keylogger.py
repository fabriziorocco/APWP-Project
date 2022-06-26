from pynput import keyboard
from pynput.keyboard import Key, Listener
import json


def on_release(key):
    pass

def check_key(key, lst):
    counter = 0
    lenList = len(lst)
    try: 
        if key in [keyboard.Key.space]: 
            print(lst[counter])
            counter += 1
    except IndexError:
        print("List is finished")
