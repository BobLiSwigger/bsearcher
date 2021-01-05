# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 21:21:11 2020

@author: BobLi
"""

from nkaiIndex import *

myIndex = nkaiIndex()
# myIndex.index_dir("../data/zfxy/")


results = myIndex.search("六级","content")


for result in results:
    print(result["title"], end=" ")
    print(result["URL"])