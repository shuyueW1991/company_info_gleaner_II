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
    search_start_url = "http://www.chinahr.com/sou/?city=0?orderField=relate&city=0?orderField=relate&page="
    c_num = 0

    def start_requests(self):
        ## industry number for chinahr is 1100 to 1113
        for k in range(1100,1114):
            for i in range(1, 176):
                search_url = self.search_start_url + str(i) + "&industrys=" + str(k)
                print('the search seed url is {}'.format(search_url))
                yield scrapy.Request(search_url, callback=self.parse_seed)

    ## The parse seed function analyzes search page to find seed web pages for crawling
    def parse_seed(self, response):
        print('parsing seed started')
        links = response.xpath('//span[@class="e3 cutWord"]/a/@data-url').extract()
        if links:
            for link in links:
                if str(link).startswith('http://www.chinahr.com/company/'):
                    yield scrapy.Request(str(link), callback=self.parse_page)
        else:
            print('parsing seed page failed')

    ## The parse page function extracts data from company pages and generates 'similar companies' url
    def parse_page(self, response):
        print('parsing co page {} started'.format(self.c_num))
        load = SpiderChinahrLoader(SpiderChinahrItem(), response)
        ## need to think about how to get position related information, besides only company information, and add to this part
        # load.add_xpath('chr_co_name', '')
        # load.add_xpath('chr_co_city', '')
        # load.add_xpath('chr_co_industry', '')
        # load.add_xpath('chr_co_type', '')
        # load.add_xpath('chr_co_estab', '')
        # load.add_xpath('chr_co_regcap', '')
        # load.add_xpath('chr_contact_name', '')
        # load.add_xpath('chr_mobile_num', '')
        # load.add_xpath('chr_fixline_num', '')
        # load.add_xpath('chr_email_addr', '')
        # load.add_xpath('chr_co_address', '')
        # load.add_xpath('chr_co_desc', '')
        load.add_value('chr_co_url', response.url)
        yield load.load_item()

        ## c_num counts the number of pages visited
        self.c_num+=1
        print(response.url)
        links = response.xpath('//div[@class="same-jobs jpadding mt15"]//@href').extract()
        ## if links exists, that means similar companies exist, then crawl similar companies' webpage
        if links:
            for link in links:
                if str(link).startswith('http://www.chinahr.com/company/'):
                    yield scrapy.Request(str(link), callback=self.parse_page)
        else:
            print('no similar companies')

