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



#load data

data = pd.read_csv("./data/passdata.csv")
group_match = data.groupby("MatchID")
senlist = [[[], [], [], [], []] for i in range(4)]


# randomly delete data from the each match to test the
# sensitivities of the metrics

for name, group in group_match:
    group.index = [i for i in range(group.shape[0])]
    group_95 = group.sample(frac=0.95)
    group_90 = group.sample(frac=0.95)
    group_85 = group.sample(frac=0.85)
    group_80 = group.sample(frac=0.85)
    G = generate_digraph_from_data(group, name)
    G_95 = generate_digraph_from_data(group_95, name)
    G_90 = generate_digraph_from_data(group_90, name)
    G_85 = generate_digraph_from_data(group_85, name)
    G_80 = generate_digraph_from_data(group_80, name)
    G_list = [G, G_95, G_90, G_85, G_80]
    for i, Gi in enumerate(G_list):
        clos = np.array(list(nx.closeness_centrality(Gi).values())).mean()
        betw = np.array(list(nx.betweenness_centrality(Gi).values())).mean()
        pgrk = np.array(list(nx.pagerank(Gi).values())).var()
        clus = nx.average_clustering(Gi)
        senlist[0][i].append(clos)
        senlist[1][i].append(betw)
        senlist[2][i].append(pgrk)
        senlist[3][i].append(clus)

plt.rcParams['savefig.dpi'] = 200
plt.rcParams['figure.dpi'] = 200
colorlist = ['red', 'blue', 'yellow', 'green', 'seagreen']
titlelist = ['Closeness', 'Betweenness', 'PagerankVar', 'Clustering']


for i in range(4):
    for j in range(5):
        plt.plot(senlist[i][j], c=colorlist[j])
    plt.legend(["Origin", "95%", "90%", "85%", "80%"])
    plt.savefig("{}.png".format(titlelist[i]))
    plt.cla()



