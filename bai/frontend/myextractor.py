# -*- coding: utf-8 -*-
import nltk

class sentExtractor:
    # 从分割好的句子中提取triples
    def __init__(self):
        Grammar = """SUBJECT:{<n..*><n.*|x.*|m.*|t.*|p.*|b.*>*}
                     RELATION:{<v.*><x.*|v.*>*}
                     OBJECT:{<n.*><n.*|x.*|m.*|t.*|p.*|b.*>*}
                     ERE:{<SUBJECT><RELATION><OBJECT>}
                     """
        QUESTION = """SUBJECT:{<n..*><n.*|x.*|m.*|t.*|p.*|b.*>*}
                      RELATION:{<v.*><x.*|v.*>*}
                      QUESTION:{<SUBJECT><RELATION>?}
                      """
        self.ERErule = nltk.RegexpParser(Grammar)
        self.Qrule = nltk.RegexpParser(QUESTION)
    
    def getObject(self, E):
        # 从Entity（nltk.tree.Tree）提取宾语
        o = ""
        for node in E:
            if isinstance(node, tuple):
                o = o + node[0]
        return o
    
    def getSubjects(self, E):
        # 从ENTITY（nltk.tree.Tree）提取主语
        subjects = []
        for node in E:
            if isinstance(node, tuple):
                if "nt" in node[1] or "nr" in node[1] or "ns" in node[1] or "nw" in node[1]:
                    subjects.append(node[0])
        return subjects
    
    def getRelation(self, R):
        # 从RELATION（nltk.tree.Tree）提取关系信息
        for node in R:
            if isinstance(node, tuple):
                if "v" in node[1]:
                    return node[0]
    
    def ERE2Graph(self, tree):
        # 抽取ERE，返回ERE列表
        subjects = []
        relation = ""
        o = ""
        EREs = []
        if not isinstance(tree, nltk.tree.Tree):
            return
        for node in tree:
            if isinstance(node, nltk.tree.Tree):
                if node.label() == "SUBJECT":
                    subjects = self.getSubjects(node)
                elif node.label() == "RELATION":
                    relation = self.getRelation(node)
                elif node.label() == "OBJECT":
                    o = self.getObject(node)
        for subject in subjects:
            EREs.append([subject, relation, o])
        return EREs
    
    def extract(self, sentence):
        # 抽取知识信息
        parseTree = self.ERErule.parse(sentence)
        result = []
        for node in parseTree:
            if isinstance(node, nltk.tree.Tree):
                if node.label() == "ERE":
                    for ERE in self.ERE2Graph(node):
                        result.append(ERE)
        return result
    
    def Q2Graph(self, tree):
        # 返回ER列表
        ERs = []
        for n in tree:
            if isinstance(n, nltk.tree.Tree):
                if n.label() == "SUBJECT":
                    for subject in self.getSubjects(n):
                        ERs.append([subject, ""])
                elif n.label() == "RELATION":
                    edge = self.getRelation(n)
                    for ER in ERs:
                        ER[1] = edge
        return ERs
    
    def extractQuestion(self, sentence):
        # 抽取问题实体和关系
        defaultNode = ""
        count = 0
        parseTree = self.Qrule.parse(sentence)
        for node in parseTree:
            if isinstance(node, nltk.tree.Tree):
                if node.label() == "QUESTION":
                    return self.Q2Graph(node)
            elif isinstance(node, tuple):
                if count == 0:
                    defaultNode = node[0]
                count = count + 1
        return [defaultNode, ""]
    
    def __del__(self):
        pass