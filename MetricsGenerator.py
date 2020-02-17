import pandas as pd
import sys
import os
import networkx as nx
import matplotlib.pylab as plt
import numpy as np


from sklearn import preprocessing
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from mtools import *

# process data
data = pd.read_csv("./data/passdata.csv")
sdata = pd.read_csv("./data/fullevents.csv")
res = pd.read_csv("./data/matches.csv")

# create metrics matrix (38 * 10), the last col is performance
metrics = np.zeros((38, 10))

dir = {}

dir['Huskies_G1'] = 0
for i in range (6):
    dir['Huskies_F' + str(i + 1)] = i + 1
for i in range(13):
    dir['Huskies_M' + str(i + 1)] = i + 7
for i in range(10):
    dir['Huskies_D' + str(i + 1)] = i + 20



# calcualte metrics for each game

for i in range(38):
    # cal score for this game:
    # generate another digraph based on shooting data
    G = generate_digraph_from_data(data, i + 1)
    G_ = nx.DiGraph(G)
    G_.add_node("Gate")
    sd = sdata[sdata.EventType == 'Shot']
    sd = sd[sd.MatchID == (i + 1)]
    sd.index = [i for i in range(sd.shape[0])]
    for k in range(sd.shape[0]):
        op = sd['OriginPlayerID'][k]
        if (op, "Gate") not in G_.edges:
            G_.add_edge(op, "Gate", weight=0)
        G_[op]['Gate']['weight'] += 1
    d = data[data.MatchID == (i + 1)]
    d = d[d.OriginPlayerID < 'Opponent']
    pass_number = d.shape[0]
    metrics[i][8] = pass_number
    metrics[i][0] = np.array(list(nx.closeness_centrality(G).values())).mean()
    metrics[i][1] = np.array(list(nx.betweenness_centrality(G).values())).mean()
    metrics[i][2] = np.array(list(nx.pagerank(G).values())).var()
    metrics[i][3] = nx.average_clustering(G)
    metrics[i][7] = len(nx.minimum_edge_cut(G))
    G__ = nx.DiGraph()
    mat = [[0 for i in range(30)] for i in range(30)]
    avg_pos_dir = process_data(data, mat, i + 1)
    edg = G.edges

    for nodes in G_.nodes:
        G__.add_node(nodes)
    for edge in G_.edges:
        G__.add_edge(edge[0], edge[1], capacity=1 / G_[edge[0]][edge[1]]['weight'])

    metrics[i][6], _ = nx.maximum_flow(G__, 'Huskies_G1', 'Gate')

    min_attack_path = 10000
    for node in list(G.nodes):
        if node[8] == 'F':
            if not nx.has_path(G, 'Huskies_G1', node):
                continue
            min_attack_path = min(min_attack_path, nx.shortest_path_length(G, 'Huskies_G1', node, weight='weight'))
    metrics[i][5] = min_attack_path


    tot = 0.0
    totd = 0.0
    for node in list(G.nodes):
        tot += avg_pos_dir[dir[node]][0] * G.degree(node)
        totd += G.degree(node)

    metrics[i][4] = tot / totd


# normalize each col

x = metrics[:, :-1]
metrics[:, 2] = 1 / metrics[:, 2]
metrics[:, 5] = 1 / metrics[:, 5]
scaler= preprocessing.MinMaxScaler(feature_range=(0, 1)).fit(x)
newX = scaler.transform(x)



# use PCA

pca = PCA(n_components=3)
pca.fit(newX)
newX = pca.transform(newX)



# draw pca figure

fig = plt.figure()
ax = Axes3D(fig)

#ax.scatter(newX[:, 0], newX[:, 1], newX[:, 2])


# linear regression part

reg = linear_model.LinearRegression()
reg.fit(newX, np.array(score))
print("mean square error:", mean_squared_error(score, reg.predict(newX)))
print("Coefficient:", reg.coef_)
print("Intercept", reg.intercept_)
print("the model is: y = ", reg.coef_, "* X + ",  reg.intercept_)


for i in range(38):
    if res['Outcome'][i] == 'loss':
        p1 = ax.scatter(newX[i][0], newX[i][1], newX[i][2],  c='blue', s=20)
    else:
        p2 = ax.scatter(newX[i][0], newX[i][1], newX[i][2], c='red', s=15)

ax.legend(handles=[p1, p2], labels=['lose', 'not lose'])
plt.savefig("./lose_or_not_lose.png")

ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('score')

ax.scatter(newX[:, 0], newX[:, 1], score, marker="x")
x0, x1 = np.meshgrid(newX[:, 0], newX[:, 1])
ax.plot_surface(x0, x1, x0 * reg.coef_[0] + x1 * reg.coef_[1] + reg.intercept_, shade=False, alpha=0.8,cmap=plt.get_cmap('rainbow'))

plt.savefig("./PCA2.png")








