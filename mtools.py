import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pylab as plt



def process_data(data, mat, gameid=None):
    """
    process the raw .csv passing data, create the adjacency map
    :param data:
    :param mat: a blank adj map to be filled
    :param gameid: the MatchID
    :return: the average position of the players
    """
    dir = {}
    pos_list = [[] for i in range(30)]
    dir['Huskies_G1'] = 0
    for i in range (6):
        dir['Huskies_F' + str(i + 1)] = i + 1
    for i in range(13):
        dir['Huskies_M' + str(i + 1)] = i + 7
    for i in range(10):
        dir['Huskies_D' + str(i + 1)] = i + 20

    data = data[data.TeamID < "Opponent"]

    if gameid is not None:
        data = data[data.MatchID == gameid]

    data.index = [i for i in range(data.shape[0])]

    for i in range(data.shape[0]):
        sp = dir[data['OriginPlayerID'][i]]
        ep = dir[data['DestinationPlayerID'][i]]
        mat[sp][ep] += 1
        pos_list[sp].append((data['EventOrigin_x'][i], data['EventOrigin_y'][i]))
        pos_list[ep].append((data['EventDestination_x'][i], data['EventDestination_y'][i]))
    avg_pos_dir = {}

    for key in range(30):
        if len(pos_list[key]) == 0:
            continue
        tmp_list = np.array(pos_list[key])
        print(tmp_list.shape)
        avg_x = tmp_list[:, 0].mean()
        avg_y = tmp_list[:, 1].mean()
        avg_pos_dir[key] = (avg_x, avg_y)

    return avg_pos_dir



def add_shooting_data(mat, shoot_data_path, gameid=None):
    """
    add the data from fullevents.csv
    :param mat: adj map
    :param shoot_data_path: data path
    :param gameid: MatchID
    :return: None
    """

    dir = {}
    dir['Huskies_G1'] = 0
    for i in range(6):
        dir['Huskies_F' + str(i + 1)] = i + 1
    for i in range(13):
        dir['Huskies_M' + str(i + 1)] = i + 7
    for i in range(10):
        dir['Huskies_D' + str(i + 1)] = i + 20
    data = pd.read_csv(shoot_data_path)
    data = data[data.TeamID < "Opponent"]
    if gameid is not None:
        data = data[data.MatchID == gameid]
    data = data[data.EventType == 'Shot']
    data.index = [i for i in range(data.shape[0])]

    for i in range(data.shape[0]):
        mat[dir[data['OriginPlayerID'][i]]][30] += 1




def generate_digraph_from_data(data:pd.DataFrame, matchid:str):
    """
     generate a diGraph from dataframe
    :param data:
    :param matchid:
    :return: a nx.Digraph for match i of HUSKIES, the weight is (1/passnumber)
    """
    data = data[data.TeamID < "Opponent"]
    data = data[data.MatchID == matchid]
    data.index = [i for i in range(data.shape[0])]
    G = nx.DiGraph()
    for i in range(data.shape[0]):
        op = data['OriginPlayerID'][i]
        dp = data['DestinationPlayerID'][i]
        if op not in G.node:
            G.add_node(op)
        if dp not in G.node:
            G.add_node(dp)
        if (op, dp) not in G.edges:
            G.add_edge(op, dp, weight=0)
        if G[op][dp]['weight'] == 0:
            G[op][dp]['weight'] += 1
        else:
            G[op][dp]['weight'] = 1 / (1 / G[op][dp]['weight'] + 1)

    return G





def triadic_of_g(mat):
    """
    use naive method to m
    :param mat: adj mat representing a graph
    :return: number of triangles in the graph
    """
    num = 0
    for i in range(mat.shape[0]):
        for j in range(i + 1, mat.shape[0]):
            if mat[i][j] == 0:
                continue
            else:
                for k in range(mat.shape[0]):
                    if mat[k][i] and mat[k][j]:
                        num += 1
    return num


def cal_triadic_trend_(data):
    """
    :param data: DATAFRAME
    :return: list triangle number per 5 minutes in a game
    """
    ans = []
    dir = {}
    dir['Huskies_G1'] = 0
    for i in range(6):
        dir['Huskies_F' + str(i + 1)] = i + 1
    for i in range(13):
        dir['Huskies_M' + str(i + 1)] = i + 7
    for i in range(10):
        dir['Huskies_D' + str(i + 1)] = i + 20
    mat = np.zeros((30, 30))
    time_div = []
    si = 0
    st = data['EventTime'][si]
    for i in range(data.shape[0]):
        if data['EventTime'][i] > st + 300:
            st = data['EventTime'][i]
            time_div.append((si, i))
            si = i + 1
        else:
            continue
    if si < data.shape[0]:
        time_div.append((si, data.shape[0]-1))

    tmp_tradic = 0
    #print(time_div)
   # print(data.shape[0])
    for i in range(len(time_div)):
        mat = np.zeros((30, 30))
        for k in range(time_div[i][0], time_div[i][1] + 1):
            op = dir[data['OriginPlayerID'][k]]
            dp = dir[data['DestinationPlayerID'][k]]
            mat[op][dp] += 1
            mat[dp][op] += 1
        num = triadic_of_g(mat)
        ans.append(num)
        tmp_tradic = num
    return ans



def cal_triadic_trend(data_path, matchid):
    """
    cal the triadic trend for certain matches
    :param data_path: path
    :param matchid:  match ot be calculated
    :return: triadic trend
    """
    data = pd.read_csv("./data/passdata.csv")
    data = data[data.TeamID < "Opponent"]
    data = data[data.MatchID == matchid]
    data_1h = data[data.MatchPeriod == '1H']
    data_2h = data[data.MatchPeriod == '2H']
    ans_list = []
    data_1h.index = [i for i in range(data_1h.shape[0])]
    data_2h.index = [i for i in range(data_2h.shape[0])]
    return cal_triadic_trend_(data_1h) + cal_triadic_trend_(data_2h)











