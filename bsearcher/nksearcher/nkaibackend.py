# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:42:39 2020

@author: BobLi
"""
from nkaiIndex import nkaiIndex
import re
import json

class nkaibackend:
    def __init__(self):
        self.urlpattern = re.compile(r"^(http://|https://)?\w+\.\w+(\.\w+)*(/.*)?$")
        self.login_user = ""
        self.__load_users()
        self.myIndex = nkaiIndex()
        if not self.myIndex.exists:
            self.myIndex.index_dir("../data/nku/")
    
    def work(self):
        while True:
            print("--------------欢迎来到nku百事通--------------")
            print("[0]退出 [1]快速检索 [2]高级检索 [3]登录 [4]注册")
            print("请选择:", end="")
            try:
                choice = int(input())
                if choice == 0:
                    print("Bye.")
                    break
            except :
                print("不合法的输入")
                continue
            if choice == 1:
                self.__quick_search()
            elif choice == 2:
                self.__pro_search()
            elif choice == 3:
                self.__login()
            elif choice == 4:
                self.__register()
                
                    
    def __login(self):
        print("请输入登录用户名:", end="")
        username= input()
        if username not in self.users:
            print("用户不存在")
            return False
        else:
            self.login_user = username
            print("登录成功")
            return True
        
    def __register(self):
        print("请输入注册用户名:", end="")
        username= input()
        if username in self.users:
            print("用户名已经被使用")
            return False
        else:
            self.users[username] = []
            self.login_user = username
            print("注册成功")
            return True
    
    def __pro_search(self):
        print("请指定查询范围:[0]返回 [1]标题 [2]网址查询 [3]全文检索 [4]锚文本", end="")
        try:
            choice = int(input())
        except BaseException:
            return
        else:
            print("请输入查询短语:", end="")
            QUERY = input()
            if choice == 0:
                return
            elif choice == 1:
                self.__search(query=QUERY, y="title")
            elif choice == 2:
                self.__search(query=QUERY, y="url")
            elif choice == 3:
                self.__search(query=QUERY, y="content")
            elif choice == 4:
                self.__search(query=QUERY, y="anchors")
                    
    def __quick_search(self):
        print("请输入查询短语:", end="")
        QUERY = input()
        if self.urlpattern.match(QUERY):
            self.__search(query=QUERY, y="url")
        else:
            self.__search(query=QUERY, y="content")
        
    def __load_users(self):
        try:
            with open("./data/users.json", "r", encoding="utf-8") as f:
                self.users = json.load(f)
        except BaseException:
            self.users = {}
        else:
            pass
        
    def __search(self, query, y):
        if self.login_user != "" and self.login_user in self.users:
            results = self.__user_search(query=query, y=y)
        else:
            results = self.myIndex.search(query=query,y=y, limit=10)
        self.__print_results(results=results)
        
    def __user_search(self, query, y):
        results = self.myIndex.search(query=query,y=y, limit=10, history=self.users[self.login_user])
        if len(self.users[self.login_user]) >= 3:
            del self.users[self.login_user][0]
        self.users[self.login_user].append([query, y])
        with open("./data/users.json", "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False)
        return results
        
    def __print_results(self, results):
        i = 1
        has_print = False
        for result in results:
            if i <= 10:
                title = self.__good_str(result["title"])
                content = self.__good_str(result["content"])
                print("No.", end="")
                print(i)
                print("title: ", end="")
                print(title)
                print("url: ", end="")
                print(result["url"])
                print("content: ", end="")
                print(content[0:96])
                print("------------------------------------------------")
                i = i + 1
            else:
                if has_print == False:
                    has_print = True
                    print("以下是个性化推荐")
                title = self.__good_str(result["title"])
                print("title: ", end="")
                print(title, end="")
                print("url: ", end="")
                print(result["url"])
            
    def __good_str(self, badstr):
        goodstr = badstr.replace("\n", "")
        goodstr = goodstr.replace("\r", "")
        goodstr = goodstr.replace(",", "")
        goodstr = goodstr.replace("-", "")
        goodstr = goodstr.replace(" ", "")
        return goodstr
    
    def __del__(self):
        with open("./data/users.json", "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False)
        pass