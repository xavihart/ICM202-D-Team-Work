import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import random
import os
import math

from matplotlib.patches import Arc
from mtools import *

# set canvas
plt.figure(figsize=(7.5, 5.5))
plt.rcParams['savefig.dpi'] = 500
plt.rcParams['figure.dpi'] = 500
fig=plt.figure()
fig.set_size_inches(7, 5)
ax=fig.add_subplot(1,1,1)
alphax = 1.0
alphay = 1.0
matchid = 30
plt.style.use('fivethirtyeight')

# create 2 dirs for players to facilitate future work
dir = {}
dir['Huskies_G1'] = 0
dir2 = {}
dir2[0] = 'G1'
for i in range(6):
       dir['Huskies_F' + str(i + 1)] = i + 1
       dir2[i + 1] = 'F'+ str(i + 1)
for i in range(13):
       dir['Huskies_M' + str(i + 1)] = i + 7
       dir2[i + 7] = 'M'+ str(i + 1)
for i in range(10):
       dir['Huskies_D' + str(i + 1)] = i + 20
       dir2[i + 20] = 'D'+ str(i + 1)


pass_data = pd.read_csv("./data/passdata.csv")  # load data
player_number = 30
mat = [[0 for i in range(player_number + 1)] \
       for j in range(player_number + 1)]

# get position infor and add shooting data
pos_dir = process_data(pass_data, mat, matchid)
add_shooting_data(mat, "./data/fullevents.csv", matchid)

# create graph G:forward net //  G2: backword net
G = nx.DiGraph()
G2 = nx.DiGraph()

G.add_node("Gate", pos=(100 * alphax, 50 * alphay))
G2.add_node("Gate", pos=(100 * alphax, 50 * alphay))

# add nodes
for k in pos_dir.keys():
       G.add_node(dir2[k], pos=(pos_dir[k][0] * alphax, pos_dir[k][1] * alphay))
       G2.add_node(dir2[k], pos=(pos_dir[k][0] * alphax, pos_dir[k][1] * alphay))

# create edges
for j in range(30):
    for i in range(0, 30):
        if(mat[i][j] == 0):
            continue
        else:
            if pos_dir[i][0] > pos_dir[j][0]:
                G.add_edge(dir2[i], dir2[j], weight=mat[i][j])
            else:
                G2.add_edge(dir2[i], dir2[j], weight=mat[i][j])

for i in range(30):
    if mat[i][30] == 0:
        continue
    G.add_edge(dir2[i], "Gate", weight=mat[i][30])


pos = nx.get_node_attributes(G, 'pos')
weight_list = nx.get_edge_attributes(G, 'weight_list')

# set color and size list for each nodes and edges
colors = []
node_size = [int(d['weight']*200) for (u, v, d) in G.edges(data=True)]
node_size[0] = 1000
node_number = G.number_of_nodes()


# set various param for nx.draw G

nx.draw(G, pos=pos, with_labels=True, edge_color=[float(d['weight']) \
        for (u, v, d) in G.edges(data=True)], node_size=node_size,\
        node_color=["#2E8B57"] + ["#DC143C" for i in range(node_number-1)],  \
        cmap=plt.cm.Dark2, edge_cmap=plt.cm.Blues, fontweight='bold', \
        font_color='white', width=[float(d['weight'] / 3) for (u,v,d) in G.edges(data=True)], \
        font_size=7, arrowstyle="->")


plt.savefig("./pic/passpic/nn_mathid_dir_forward{}.png".format(matchid))


plt.cla()

# set various param for nx.draw and draw G2

node_size = [int(d['weight']*200) for (u, v, d) in G2.edges(data=True)]
node_size[0] = 1000
node_number = G2.number_of_nodes()
nx.draw(G2, pos=pos, with_labels=True, edge_color=[float(math.pow(d['weight'], 1/8)) for (u, v, d) in G2.edges(data=True)],\
         node_size=node_size,\
        node_color=["#2E8B57"] + ["#DC143C" for i in range(node_number-1)], cmap=plt.cm.Dark2, edge_cmap=plt.cm.Blues, fontweight='bold', \
        font_color='white', width=[float(d['weight'] / 3) for (u,v,d) in G2.edges(data=True)], font_size=7,\
        arrowstyle="->")

plt.savefig("./pic/passpic/nn_mathid_dir_backward{}.png".format(matchid))



