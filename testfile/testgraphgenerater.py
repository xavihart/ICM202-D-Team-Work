import pandas as pd
import sys
import os
import networkx as nx
import matplotlib.pylab as plt
o = os.getcwd()
sys.path.append(o)
from mtools import *

print("*" * 70)
data = pd.read_csv("./data/passdata.csv")
res = pd.read_csv("./data/matches.csv")

G = generate_digraph_from_data(data, 1)

lis = []
relist = []
for i in range(38):
    G = generate_digraph_from_data(data, i + 1)
    lis.append(nx.average_clustering(G))
for i in range (38):
    if res.iloc[i][3] == res.iloc[i][4]:
        k = 1
    elif res.iloc[i][3] > res.iloc[i][4]:
        k = 3
    else:
        k = 0
    if res.iloc[i][5] == 'home':
        a = 0.9
    else:
        a = 1
    relist.append(np.exp(a*((res['OwnScore'][i] - res['OpponentScore'][i]) * 0.3 + 0.7 * k)))



plt.scatter(lis, relist)
plt.savefig("./pic/task2/test.png")


print(nx.betweenness_centrality(G))
print(nx.closeness_centrality(G))
print(nx.pagerank(G))
print(nx.minimum_edge_cut(G))
print(nx.center(G))
print(nx.shortest_path_length(G, source='Huskies_G1', target='Huskies_F4'))

""""
result = pd.read_csv("./metrics.csv")
for i in range(38):
    G = generate_digraph_from_data(data, i + 1)
    result['closeness'][i] = np.array(list((nx.closeness_centrality(G).values()))).mean()
    result['betweenness'][i] = np.array(list(nx.betweenness_centrality(G).values())).mean()
    result['pagerank'][i] = np.array(list(nx.pagerank(G).values())).mean()
    result['clustering_degree'][i] = nx.average_clustering(G)
result.to_csv("./metrics2.csv", index=False)
"""

ans = [[] for i in range(30)]

dir = {}

dir['Huskies_G1'] = 0
for i in range(6):
    dir['Huskies_F' + str(i + 1)] = i + 1
for i in range(13):
    dir['Huskies_M' + str(i + 1)] = i + 7
for i in range(10):
    dir['Huskies_D' + str(i + 1)] = i + 20

dir2 = {}

dir2[0] = 'G1'

ans_dir = {}

for i in range(6):
       dir['Huskies_F' + str(i + 1)] = i + 1
       dir2[i + 1] = 'F'+ str(i + 1)
for i in range(13):
       dir['Huskies_M' + str(i + 1)] = i + 7
       dir2[i + 7] = 'M'+ str(i + 1)
for i in range(10):
       dir['Huskies_D' + str(i + 1)] = i + 20
       dir2[i + 20] = 'D'+ str(i + 1)


for i in range(37, 38):
    data = pd.read_csv("./data/passdata.csv")
    data = data[data.OriginPlayerID > 'Opponent']
    data = data[data.MatchID == (i + 1)]
    g = data.groupby("OriginPlayerID")
    for name, group in g:
        group.index = [i for i in range(group.shape[0])]
        g_1h = group[group.MatchPeriod == '1H']
        g_2h = group[group.MatchPeriod == '2H']
        g_1h.index = [i for i in range(g_1h.shape[0])]
        g_2h.index = [i for i in range(g_2h.shape[0])]
        #print(g_1h['EventTime'])
        if g_1h.shape[0] == 0:
            player_time_1h = 0
        else:
            player_time_1h = g_1h['EventTime'][g_1h.shape[0] - 1] - g_1h['EventTime'][0]
        if g_2h.shape[0] == 0:
            player_time_2h = 0
        else:
            player_time_2h = g_2h['EventTime'][g_2h.shape[0] - 1] - g_2h['EventTime'][0]
        ans_dir[name] = (player_time_1h + player_time_2h) / 3600




print(ans_dir)












