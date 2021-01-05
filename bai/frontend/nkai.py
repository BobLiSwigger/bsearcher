# -*- coding: utf-8 -*-
import json
import time
from myparser import textParser
from myextractor import sentExtractor
from mygraph import nkaiKG

class Nkai:
    def __init__(self):
        self.psr = textParser() # 词法分析器
        self.ext = sentExtractor() # 知识抽取器
        self.kg = nkaiKG() # 图管理器
        if not self.kg.load():
            self.makeGraph()
    
    def makeGraph(self):
        with open("../data/nku.json", "r", encoding="utf-8") as f:
            pages = json.load(f)
            start = time.time()
            for page in pages:
                for sentence in self.psr.parse(page[1]):
                    for ERE in self.ext.extract(sentence):
                        self.kg.add(ERE)
            end = time.time()
            print('Spent time:', round(end - start, 2),'secs')
            self.kg.save()
    
    def printGraph(self):
        # 显示关系图
        self.kg.show()
        
    def searchByER(self, ER):
        for e in self.kg.edges():
            if (e[0] == ER[0] or e[1] == ER[0]) and e[2]["attr"] == ER[1]:
                return e[0] + e[2]["attr"] + e[1]
        return ""
        
    def search(self, text):
        sentence = self.psr.tokenize(text)
        ERs = self.ext.extractQuestion(sentence)
        results = []
        for ER in ERs:
            results.append(self.searchByER(ER))
        return results
    
    def __del__(self):
        pass