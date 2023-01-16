#python 
## 教程地址

[教程 — NetworkX 3.0rc2.dev0 文档](https://networkx.org/documentation/latest/tutorial.html)

## 主要内容

### 创建图表

- `nx.Graph()`来创建一个无向图
创建一个没有节点和边的空图形。

```python
import networkx as nx
G = nx.Graph()
```

- `nx.DiGraph()`创建一个有向图
[`DiGraph`](https://networkx.org/documentation/latest/reference/classes/digraph.html#networkx.DiGraph "networkx.DiGraph") 类提供了特定于的其他方法和属性 到有向边缘，例如[`DiGraph.out_edges`](https://networkx.org/documentation/latest/reference/classes/generated/networkx.DiGraph.out_edges.html#networkx.DiGraph.out_edges "networkx.DiGraph.out_edges")、[`DiGraph.in_degree`](https://networkx.org/documentation/latest/reference/classes/generated/networkx.DiGraph.in_degree.html#networkx.DiGraph.in_degree "networkx.DiGraph.in_degree") 

```python
import networkx as nx
G = nx.DiGraph()
```

### 添加节点

图形可以通过多种方式增长。NetworkX 包括许多图形[生成器函数](https://networkx.org/documentation/latest/reference/generators.html)和[工具，用于读取和写入多种格式的图形](https://networkx.org/documentation/latest/reference/readwrite/index.html)。

```python
'''1'''
G.add_node(1)
'''2'''
G.add_nodes_from([2, 3])
'''3'''
G.add_nodes_from([
     (4, {"color": "red"}),
     (5, {"color": "green"}),
 ])
```

### 添加边

`G`也可以通过一次添加一个边
```python
'''1'''
G.add_edge(1, 2)
'''2'''
>>> e = (2, 3)
>>> G.add_edge(*e)  # unpack edge tuple*
'''3'''
G.add_edges_from([(1, 2), (1, 3)])
```

### 绘图

NetworkX 主要不是一个图形绘图包，而是具有基本绘图 Matplotlib以及使用开源Graphviz软件的界面。

首先导入 Matplotlib 的绘图界面（pylab 也可以）

```python
import matplotlib.pyplot as plt
```

调用下面的方法：

	1. nx.draw
	2. nx.draw_cycle
	3. nx.draw_networkx_edge_labels
	4. nx.draw_random
	5. nx.draw_spectral
	6. nx.draw_shell

使用`plt.subplot(x)` 将各个图形分开
使用`plt.savefig("path.png")` 保存为图片

