# Creation of a leaderboard table taking into account the speed
#This function create the ranking table. If a user is at level 3 then it's register only in the level 3, and same for level 2 and level 1 consequently.
def ranking():  #Ranking function
    jsonStr = open('data/Historical.json') #open and load data
    # returns JSON object as a dictionary
    jsonStr = json.load(jsonStr)

    for el in jsonStr.keys():  #iterate over users
        if (jsonStr[el]["Level3"][0]) != 1000:  #check if the user has played this level
            jsonStr[el]["Level3"][0] = jsonStr[el]["Level3"][0] - jsonStr[el]["Level2"][0]  #The speed is registered together for all levels. Then the speed of level x is the the speed of level x - speed of level x-1.

        #same for level 2
        if (jsonStr[el]["Level2"][0]) != 1000:
            jsonStr[el]["Level2"][0] = jsonStr[el]["Level2"][0] - jsonStr[el]["Level1"][0]


    #register all the data of the speed. If the user played level 3, then is registered level 3 and its speed, and then for all the levels to create a rank.
    levels3 = []
    for el in jsonStr.keys():
        if (jsonStr[el]["Level3"][0]) != 1000:  # take the peolpe that did the level 3
            levels3.append([el, jsonStr[el]["Level3"][0], 3])

    levels2 = []
    for el in jsonStr.keys():
        if (jsonStr[el]["Level3"][0]) == 1000:
            if (jsonStr[el]["Level2"][0]) != 1000:
                levels2.append([el, jsonStr[el]["Level2"][0], 2])

    levels1 = []

    for el in jsonStr.keys():
        if (jsonStr[el]["Level3"][0]) == 1000:
            if (jsonStr[el]["Level2"][0]) == 1000:
                if (jsonStr[el]["Level1"][0]) != 1000:
                    levels1.append([el, jsonStr[el]["Level1"][0], 1])

    #Create a dataframe
    df = pd.DataFrame(columns=["Name", "Level", "Time"])

    #update the dataframe with all the levels
    for el in levels3:
        dict = {"Name": el[0], "Level": el[2], "Time": el[1]}
        df = df.append(dict, ignore_index=True)

    for el in levels2:
        dict = {"Name": el[0], "Level": el[2], "Time": el[1]}
        df = df.append(dict, ignore_index=True)

    for el in levels1:
        dict = {"Name": el[0], "Level": el[2], "Time": el[1]}
        df = df.append(dict, ignore_index=True)

    return df
