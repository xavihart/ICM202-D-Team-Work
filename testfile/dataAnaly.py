import pandas as pd
import numpy as np
import networkx as nx
from mtools import *

data = pd.read_csv("./data/passdata.csv")
data = data[data.TeamID < "Opponent"]

pass_list = []
g = data.groupby("MatchID")
for name, group in g:
    pass_list.append(group.shape[0])
print(pass_list)
print(np.array(pass_list).mean())
strl = ""
for i in range(38):
    strl+=( "'"+str(i+1)+"'")
    strl+=","
print(strl)

data_match = pd.read_csv("./data/matches.csv")
score_list = []
for i in range(data_match.shape[0]):
    if data_match.iloc[i][3] == data_match.iloc[i][4]:
        sc = 1
    elif data_match.iloc[i][3] > data_match.iloc[i][4]:
        sc = 3
    else:
        sc = 0
    if data_match.iloc[i][5] == 'home':
        k = 0.9
    else:
        k = 1
    score_list.append(k * ((data_match.iloc[i][3] - data_match.iloc[i][4]) * 0.3 + 0.7 * sc)+2)

print(score_list)
