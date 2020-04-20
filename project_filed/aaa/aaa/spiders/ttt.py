# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from urllib.request import urljoin
from ..items import *


class TttSpider(scrapy.Spider):
    name = 'ttt'
    interval = 1440
    IS_INSERT = False
    IS_INCREMENTAL = True
    table = 'caipan'
        
    def start_requests(self):
        url = 'http://www.law-lib.com/cpws/cpwsml-cx.asp?bbdw=&pages=1&tm1=&tm2='
        yield scrapy.Request(url=url, callback=self.get_page)
        
    def get_page(self, response):
        s = Selector(response=response)
        for i in range(1, int(50)+1):
            url = 'http://www.law-lib.com/cpws/cpwsml-cx.asp?bbdw=&pages={pages}&tm1=&tm2='.format(pages=i)
            print(url)
            yield scrapy.Request(url=url, callback=self.get_lists)
    
    def get_lists(self, response):
        s = Selector(response=response)
        lists = s.xpath('//ul[@class="line2"]/li')
        if len(lists)> 0:
            for i in lists:
                href = urljoin(response.url, i.xpath('./span/a/@href').extract_first(''))
                print(href)
                if href:
                    yield scrapy.Request(url=href, callback=self.get_contents)
        else:
            print('Not Find')
    
    def get_contents(self, response):
        item = AaaItem()
        s = Selector(response=response)
        title = s.xpath("/html/body/div[3]/div/div[1]/div/div[1]/div[1]/h2/b/text()").extract_first("")
        item["title"] = title
        
        content = s.xpath('//div[@class="viewcontent"]/text()').extract_first("")
        item["content"] = content
        print(item)