import pandas as pd
import json

jsonStr = open('data/Historical.json')
# returns JSON object as a dictionary
jsonStr = json.load(jsonStr)

Usersl = []
Users = 0
for el in jsonStr.keys():
    Users +=1
Usersl.append(Users)

times_1 = []
times_2 = []
times_3 = []

for el in jsonStr.keys():
    if (jsonStr[el]["Level3"][0]) != 1000:
        jsonStr[el]["Level3"][0] = jsonStr[el]["Level3"][0] - jsonStr[el]["Level2"][0]

    if (jsonStr[el]["Level2"][0]) != 1000:
        jsonStr[el]["Level2"][0] = jsonStr[el]["Level2"][0] - jsonStr[el]["Level1"][0]

for el in jsonStr.keys():
    if jsonStr[el]["Level1"][0] != 1000:
        times_1.append(jsonStr[el]["Level1"][0])

for el in jsonStr.keys():
    if jsonStr[el]["Level2"][0] != 1000:
        times_2.append(jsonStr[el]["Level2"][0])

for el in jsonStr.keys():
    if jsonStr[el]["Level3"][0] != 1000:
        times_3.append(jsonStr[el]["Level3"][0])

times_1_l = []
times_2_l = []
times_3_l = []

times_1_l.append(sum(times_1) / len(times_1))
times_2_l.append(sum(times_2) / len(times_2))
times_3_l.append(sum(times_3) / len(times_3))




df_Levels = pd.DataFrame()
df_Levels["Number_Users"] = Usersl
df_Levels["Level1"] = times_1_l
df_Levels["Level2"] = times_2_l
df_Levels["Level3"] = times_3_l

attempt_1 = []
attempt_2 = []
attempt_3 = []

for el in jsonStr.keys():
    if jsonStr[el]["Level1"][0] != 1000:
        attempt_1.append(jsonStr[el]["Level1"][2])

for el in jsonStr.keys():
    if jsonStr[el]["Level2"][0] != 1000:
        attempt_2.append(jsonStr[el]["Level2"][2])

for el in jsonStr.keys():
    if jsonStr[el]["Level3"][0] != 1000:
        attempt_3.append(jsonStr[el]["Level3"][2])

attempt_1l = []
attempt_2l = []
attempt_3l = []

attempt_1l.append(sum(attempt_1) / len(attempt_1))
attempt_2l.append(sum(attempt_2) / len(attempt_2))
attempt_3l.append(sum(attempt_3) / len(attempt_3))

df_att = pd.DataFrame()
df_att["Level1"] = attempt_1l
df_att["Level2"] = attempt_2l
df_att["Level3"] = attempt_3l

