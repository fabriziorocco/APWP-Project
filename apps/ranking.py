# Creation of a leaderboard table taking into account the speed
from itertools import groupby
import pandas as pd
import json

jsonStr = open('data/Historical.json')
# returns JSON object as a dictionary
data = json.load(jsonStr)

# Convert JSON to DataFrame using read_json()
df = pd.read_json(data, orient = 'index')
print(df)

# Create a column called Rank in the df
df['Rank'] = (
    df.groupby('User')['Level']
        .transform('max')
        .rank(method='dense', ascending=False)
        .astype(int)
)

# If two users have the same level, check the typing speed
df['Rank'] = (
    df.groupby('Level')['Speed']
        .transform('max')
        .rank(method='dense', ascending=False)
        .astype(int)
)
