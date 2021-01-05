# -*- coding: utf-8 -*-

import jieba
from jieba import posseg

class textParser:
    # 从文本中解析句子（标记的token流）
    def __init__(self):
        jieba.load_userdict("../data/mydict.txt")
        pass
        
    def parse(self, text):
        # 将非结构化文本解析成由token组成的句子
        tokens = self.tokenize(text)
        sents = self.sentencize(tokens)
        return sents
    
    def tokenize(self, text):
        # 词法分析，返回标记词性的token列表
        tokens = posseg.cut(text)
        result = []
        for word, flag in tokens:
            result.append((str(word), str(flag)))
        return result
    
    def sentencize(self, tokens):
        # 切分句子，将一篇文档的token流分割成句子
        sents = []
        sentence = []
        for token in tokens:
            sentence.append((token[0], token[1]))
            if self.isSentEnd(token):
                if len(sentence) > 3:
                    sents.append(sentence)
                sentence = []    
        return sents
    
    def isSentEnd(self, token):
        # 判断token是否为句子结尾
        if "x" not in token[1]:
            return False
        if token[0] == "，" or token[0] == "（" or token[0] == "）":
            return False
        if token[0] == " " or token[0] == "《" or token[0] == "》":
            return False
        if token[0] == "-" or token[0] == "、" or token[0] == "：":
            return False
        return True
    
    def __del__(self):
        pass