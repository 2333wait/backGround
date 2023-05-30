import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt



def PC_algorithm(data, alpha=0.05):
    """
    实现Peter and Clark算法
    data：pandas.DataFrame类型，包含所有变量的时间序列数据
    alpha：显著性水平，默认为0.05
    """
    n, k = data.shape
    corr = np.abs(np.corrcoef(data, rowvar=False))
    S = set(range(k))
    G = np.zeros((k, k))

    # 初始化所有节点之间的边
    for i in range(k):
        for j in range(i + 1, k):
            if i != j:
                G[i, j] = 1
                G[j, i] = 1

    while len(S) > 0:
        # 找到当前分数最高的一组变量对
        max_score, max_pair = -np.inf, None
        for i, j in [(i, j) for i in S for j in S if i != j]:
            Sij = list(set(range(k)).difference({i, j}))
            score = corr[i, j] - np.sum([corr[i, m] * corr[j, m] * cond_corr(i, j, m, G) for m in Sij])
            if score > max_score:
                max_score = score
                max_pair = [i, j]

        # 将分数不显著的边删除
        if max_score > 0 and max_score > chi2.ppf(1 - alpha, df=1):
            G[max_pair[0], max_pair[1]] = 0
            G[max_pair[1], max_pair[0]] = 0

        S = set(np.nonzero(G)[0])

    return G.astype(int)
data = pd.read_csv('E:/Projects/dataFromMysql/fromscl.csv', index_col=0)

# 运行PC算法
adj_matrix = PC_algorithm(data.values, alpha=0.05)

# 构建有向图
G = nx.DiGraph(adj_matrix)

# 可视化有向图
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='lightblue')
nx.draw_networkx_labels(G, pos, font_size=16, font_family='Arial')
nx.draw_networkx_edges(G, pos, width=1, edge_color='gray')
plt.axis('off')

# 显示有向图
plt.show()