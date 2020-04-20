# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from urllib.request import urljoin

class TushuSpider(scrapy.Spider):
    name = "tushu"

    def __init__(self):
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',            'Accept-Encoding': 'gzip, deflate',            'Accept-Language': 'zh-CN,zh;q=0.9',            'Cache-Control': 'max-age=0',            'Connection': 'keep-alive',            'Cookie': 'ASPSESSIONIDQSSCBCTD=JAIJAEHCCEBBGNANNNNJBEOK; ASPSESSIONIDSQDQCRCR=NKLLEIOCIKNEHCEHOHMGBKCE; __gads=ID=56cf2aa77616cd8b:T=1585876698:S=ALNI_MayTyHVdQtWcbBmA3k0kTBxOLJEdg; ASPSESSIONIDQSASBSCQ=AMCECMEBIMJJOEEAJPAOAHGH',            'Host': 'www.law-lib.com',            'Upgrade-Insecure-Requests': '1'}
        self.pname = re.comple("(.*?)")

    def start_requests(self):
        url = 'http://www.law-lib.com/cpws/cpwsml-cm.asp?bbdw=&pages=1&tm1=&tm2='
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        s = Selector(response=response)
        wslx_lists = s.xpath('//div[@class="padding"]/div')
        for i in wslx_lists:
            wslx = i.xpath('./div/h3/text()').extract_first()
            wslx_href = urljoin(response.url, i.xpath('./div/h3//a/@href').extract_first())
            if wslx:
                print(wslx, wslx_href)