# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from multiprocessing import Lock
from bs4 import BeautifulSoup
import json
import codecs
import os

class ExampleSpider(scrapy.Spider):
    htmlNo = 1
    mutex = Lock()
    name = 'nkcrawler'
    allowed_domains = ['nankai.edu.cn']
    start_urls = ['https://www.nankai.edu.cn/']
    crawled_urls = {} # {url:[title, []anchor]}
    allowpattern = r'^(http|https)://.+\.nankai\.edu\.cn/(info.*|.*list|.*page|index\.php.*)\.(htm|html)$'
    linkextrator = LinkExtractor(allow=allowpattern)
        
    def parse(self, response):
        self.mutex.acquire()
        if response.url not in self.crawled_urls:
            self.crawled_urls[response.url]=["", []]
        self.mutex.release()
        # 合法网页且非乱码
        if response.status == 200:
            try:
                _body_ = codecs.decode(response.body, "utf_8_sig")
            except BaseException:
                pass
            else:
                soup = BeautifulSoup(codecs.decode(response.body), 'lxml')
                self.crawled_urls[response.url][0] = (soup.title.string)
                # self._save_(_body_, response.url)
                yield {response.url:soup.get_text()}
        # 跟踪锚文本
        links = self.linkextrator.extract_links(response)
        for _link_ in links:
            self.crawled_urls[response.url][1].append([_link_.url, _link_.text])
            if _link_.url not in self.crawled_urls:
                yield scrapy.Request(url=_link_.url, callback=self.parse)

    def __del__(self):
        with open('crawled_urls.json', "w", encoding="utf-8") as f:
            json.dump(self.crawled_urls, f, ensure_ascii=False)

