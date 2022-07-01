import json
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

"""
Plotting of the number of attempts per level per user
"""

def progressPlot(name):

    n = input('Enter 0 for accuracy, 1 for speed or 2 for number of attempts')
    n = int(n)
    f = open('data/Historical.json')
    # returns JSON object as a dictionary
    data = json.load(f)


    objects = ('Level 1', 'Level 2', 'Level 3')
    yPos = np.arange(len(objects))
    performance = [data[name]['Level1'][n],data[name]['Level2'][n],data[name]['Level3'][n]]

    if n == 0:
        ylabel = 'Accuracy per level'
    elif n == 1:
        ylabel = 'Speed per level'
    elif n == 2:
        ylabel = 'Attempts per level'

    plt.bar(yPos, performance, align='center', alpha=0.5)
    plt.xticks(yPos, objects)
    plt.ylabel(ylabel)
    plt.title(f"{name}'s progress")

    plt.show()

progressPlot('Giorgio')