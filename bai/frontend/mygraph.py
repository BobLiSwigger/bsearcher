# -*- coding: utf-8 -*-

import networkx
import json

class nkaiKG:
    def __init__(self):
        self.graph = networkx.DiGraph()
    
    def add(self, ERE):
        # 图的生长
        self.graph.add_node(ERE[0])
        self.graph.add_node(ERE[2])
        self.graph.add_edge(ERE[0], ERE[2], attr=ERE[1])
            
    def show(self):
        networkx.draw(self.graph)
        print("-----------------node-----------------")
        for node in self.graph.nodes():
            print(node)
        print("-----------------edge-----------------")
        for edge in self.graph.edges(data=True):
            print(edge)
            
    def load(self):
        # 从保存的文件中加载图
        try:
            with open("../data/nkaiKG_nodes.json", "r", encoding="utf-8") as f:
                nodes = json.load(f)
            with open("../data/nkaiKG_edges.json", "r", encoding="utf-8") as f:
                edges = json.load(f)
        except BaseException:
            print("no resource")
            return False
        else:
            # 构造有向图
            for node in nodes:
                self.graph.add_node(node)
            for edge in edges:
                self.graph.add_edge(edge[0], edge[1], attr=edge[2]["attr"])
            return True
            
    def save(self):
        # 保存图
        nodes = []
        edges = []
        for node in self.graph.nodes():
            nodes.append(node)
        for edge in self.graph.edges(data=True):
            edges.append(edge)
        with open("../data/nkaiKG_nodes.json", "w", encoding="utf-8") as f:
            json.dump(nodes, f, ensure_ascii=False)
        with open("../data/nkaiKG_edges.json", "w", encoding="utf-8") as f:
            json.dump(edges, f, ensure_ascii=False)
    
    def edges(self):
        # 返回图的边迭代器
        return self.graph.edges(data=True)
    
    def nodes(self):
        # 返回节点的迭代器
        return self.graph.nodes()
    
    def __del__(self):
        pass