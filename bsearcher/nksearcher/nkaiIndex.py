# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 14:16:34 2020

@author: BobLi
"""

import os
from whoosh import index
from whoosh import scoring
from whoosh import sorting
from whoosh.fields import Schema, TEXT, KEYWORD, NUMERIC
from whoosh.qparser import QueryParser
from bs4 import BeautifulSoup
from jieba.analyse import ChineseAnalyzer
from whoosh.analysis import StemmingAnalyzer
import sys
import json
import networkx

sys.setrecursionlimit(3000)

class nkaiIndex:
    def __init__(self):
        self.indexDir = "./indexfile"
        if not os.path.exists(self.indexDir):
            os.mkdir(self.indexDir)
        self.schema = Schema(url=TEXT(stored=True, analyzer=StemmingAnalyzer()),
                             title=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                             content=TEXT(stored=True, analyzer=ChineseAnalyzer()),
                             anchors=KEYWORD(stored=True, commas=True),
                             pageRank=NUMERIC(int, 32, sortable=True, stored=True)
                             )
        self.exists = index.exists_in(self.indexDir, indexname="nkai")
        if self.exists:
            self.index = index.open_dir(self.indexDir, indexname="nkai")
        else:
            self.index = index.create_in(self.indexDir, schema=self.schema, indexname="nkai")
        
    
    def index_dir(self, dir):
        writer = self.index.writer()
        try:
            with open(dir+"crawled_urls.json", "r", encoding="utf-8") as f:
                self.info = json.load(f)
            with open(dir+"nku.json", "r", encoding="utf-8") as f:
                self.pages = json.load(f)
            self.calPageRank()
            for page in self.pages:
                keys = page.keys()
                for key in keys:
                    anchors_str = self.__anchors2str(self.info[key][1])
                    pageRank = self.__getPagerank(url=key)
                    writer.add_document(url=key, 
                                        title=self.info[key][0], 
                                        content=page[key],
                                        anchors=anchors_str,
                                        pageRank=int(pageRank*100000))
        except BaseException:
            writer.cancel()
            print("index_dir error")
            pass
        else:
            writer.commit()
                
    def search(self, query, y, limit=10, history=[]):
        searcher = self.index.searcher(weighting=scoring.TF_IDF())
        pR_score = sorting.FieldFacet("pageRank", reverse=True)
        if len(history) == 0:
            qp = QueryParser(y, schema=self.index.schema)
            q = qp.parse(query)
            results = searcher.search(q, sortedby=pR_score, limit=10)
            return results
        else:
            qp = QueryParser(y, schema=self.index.schema)
            q = qp.parse(query)
            results = searcher.search(q, sortedby=pR_score, limit=10)
            for entry in history:
                qp_1 = QueryParser(entry[1], schema=self.index.schema)
                q_1 = qp_1.parse(entry[0])
                his_results = searcher.search(q_1, sortedby=pR_score, limit=5)
                results.upgrade_and_extend(his_results)
            return results
    
    def calPageRank(self):
        graph = networkx.DiGraph()
        for key in self.info.keys():
            for anchor in self.info[key][1]:
                graph.add_edge(anchor[0], key) # 从第二个参数到第一个参数的有向边
        self.pageRank = networkx.pagerank(graph,alpha=0.85)
        self.mean_pR = 1 / len(self.pageRank)
    
    def __anchors2str(self, anchors_list):
        anchors_str = ""
        for anchor in anchors_list:
            item = anchor[1].replace(" ", "")
            item = item.replace("\n", "")
            item = item.replace("\r", "")
            item = item.replace(",", "")
            if item == "":
                continue
            if anchors_str != "":
                anchors_str = anchors_str + ","
            anchors_str = anchors_str + item
        return anchors_str
    
    def __getPagerank(self, url):
        if url not in self.pageRank:
            return self.mean_pR
        else:
            return self.pageRank[url]
    
    # Package function
    def list_files(self, dir):
        files = []
        self._list_files_recursion(files, dir)
        return files
    
    # Recursion process to get all the files within the directory
    def _list_files_recursion(self, files, dir):
        if os.path.isfile(dir):
            files.append(dir)
            return
        else:
            for root, dir_list, file_list in os.walk(dir):
                for d in dir_list:
                    self._list_files_recursion(files, os.path.join(dir ,d))
                for f in file_list:
                    self._list_files_recursion(files, os.path.join(dir ,f))
                return
    def __del__(self):
        pass
    
