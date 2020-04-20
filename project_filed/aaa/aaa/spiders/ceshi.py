# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from urllib.request import urljoin
from ..items import *


class CeshiSpider(scrapy.Spider):
    name = 'ceshi'
    interval = 1440
    IS_INSERT = False
    IS_INCREMENTAL = True
    table = 'caipan'
        
    def start_requests(self):
        url = 'http://www.law-lib.com/cpws/cpwsml-cx.asp?bbdw=&50=2&tm1=&tm2='
        yield scrapy.Request(url=url, callback=self.get_page)
        
    def get_page(self, response):
        s = Selector(response=response)
        for i in range(1, int(50)+1):
            url = 'http://www.law-lib.com/cpws/cpwsml-cx.asp?bbdw=&pages={page}&tm1=&tm2='.format(page=i)
            yield scrapy.Request(url=url, callback=self.get_lists)
    
    def get_lists(self, response):
        s = Selector(response=response)
        lists = s.xpath('//ul[@class="line2"]/li')
        for i in lists:
            href = urljoin(response.url, i.xpath('./span/a/@href').extract_first())
            if href:
                yield scrapy.Request(url=href, callback=self.get_contents)
    
    def get_contents(self, response):
        item = AaaItem()
        s = Selector(response=response)
        
        content = s.xpath("//div[@class='viewcontent']//text()").extract()
        item["content"] = content
        print(content)
        
        yield item