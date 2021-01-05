# -*- coding: utf-8 -*-
from nkai import Nkai

# neo4j数据库配置
# uri = "neo4j://localhost:7687"
# driver = GraphDatabase.driver(uri, auth=("neo4j", "l18740122759"))
# driver.close()

ai = Nkai()
# ai.printGraph()
# print(ai.search("汉英获得过什么奖项？"))
# print(ai.search("郭士桐任？"))
# print(ai.search("文化周展播时间是？"))
# print(ai.search("李波答辩的时间是"))
# print(ai.search("姜立夫兼任"))

print("------------------------\n欢迎使用智能检索系统")

while True:
    query = input()
    if query == "quit":
        break
    else:
        print(ai.search(query))