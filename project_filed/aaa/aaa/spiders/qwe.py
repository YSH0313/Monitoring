# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from urllib.request import urljoin
from ..items import *


class QweSpider(scrapy.Spider):
    name = 'qwe'
    interval = 1440
    IS_INSERT = False
    IS_INCREMENTAL = True
    table = 'caipan'
        
    def start_requests(self):
        url = 'start_url'
        yield scrapy.Request(url=url, callback=self.get_page)
        
    def get_page(self, response):
        s = Selector(response=response)
        for i in range(1, int(pages)+1):
            yield scrapy.Request(url=i, callback=self.get_lists)
    
    def get_lists(self, response):
        s = Selector(response=response)
        lists = s.xpath('lists_xpath')
        for i in lists:
            href = urljoin(response.url, i.xpath('content_xpath').extract_first())
            if href:
                yield scrapy.Request(url=href, callback=self.get_contents)
    
    def get_contents(self, response):
        item = AaaItem()
        s = Selector(response=response)
        