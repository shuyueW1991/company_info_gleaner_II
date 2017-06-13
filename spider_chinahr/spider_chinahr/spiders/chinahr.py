# -*- coding: utf-8 -*-
import scrapy
import json
import time
from lxml import html
import requests
from spider_chinahr.items import SpiderChinahrItem
from spider_chinahr.items import SpiderChinahrLoader
from bs4 import BeautifulSoup as bs

date=time.strftime("%Y%m%d",time.localtime(time.time()))

class ChinahrSpider(scrapy.Spider):
    name = "chinahr"
    search_start_url = "http://www.chinahr.com/sou/"
    c_num = 0

    def start_requests(self):
        yield scrapy.Request(self.search_start_url, callback=self.parse_seed)

    def parse_seed(self, response):
        print('parsing seed started')
        links = response.xpath('//span[@class="e3 cutWord"]/a/@data-url').extract()
        if links:
            for link in links:
                if str(link).startswith('http://www.chinahr.com/company/'):
                    yield scrapy.Request(str(link), callback=self.parse_page)
        else:
            print('parsing seed page failed')

    def parse_page(self, response):
        print('parsing co page {} started'.format(self.c_num))

        self.c_num+=1
        print(response.url)
        links = response.xpath('//div[@class="same-jobs jpadding mt15"]//@href').extract()
        if links:
            for link in links:
                if str(link).startswith('http://www.chinahr.com/company/'):
                    yield scrapy.Request(str(link), callback=self.parse_page)
        else:
            print('no relate co info for this company')

