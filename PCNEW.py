import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pgmpy.estimators import PC
import networkx as nx


data = pd.read_csv('E:/Projects/dataFromMysql/data2.csv', index_col=0)

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['SimHei'] # 设置使用SimHei字体

# 运行PC算法
est = PC(data)
skeleton = est.estimate_skeleton(indegree_outdegree_treshold=(0.2, 0.2))
model = est.estimate(return_type='dag')
print(model.edges()) # 输出因果关系图的边集

G = nx.DiGraph(model.edges()) # 将边集转换成有向图
pos = nx.spring_layout(G) # 使用Spring布局算法生成节点坐标
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos, arrows=True)
nx.draw_networkx_labels(G, pos)
plt.show()