# -*- coding: utf-8 -*-
import scrapy
import json
import time
from lxml import html
import requests
from scrapy.selector import Selector
from spider_chinahr.items import SpiderChinahrItem
from spider_chinahr.items import SpiderChinahrLoader
from bs4 import BeautifulSoup as bs

date=time.strftime("%Y%m%d",time.localtime(time.time()))
# search_start_url = "http://www.chinahr.com/sou/?city=0&industrys="
def clean(x):
    return x.replace('\\r', '').replace('\\t', '').replace('\\n', '').replace('"', '').replace(" ", "").replace("\"", "").replace("|","").replace('[','').replace(']','').replace("'",'').replace(',','')

class ChinahrSpider(scrapy.Spider):
    name = "chinahr"
    search_start_url = "http://www.chinahr.com/sou/?city=0&industrys="
    c_num = 0

    def start_requests(self):
        ## industry number for chinahr is 1100 to 1113
        while True:
            for k in range(1100,1114):
                for t in [1,2,3,4,5,6,7,8,9,10,99]:
                    for s in [1,'2%2C3',4,5,6,7,8,9,10,11,12]:
                    # for d in range(1,14):
                    # for age in range(1,7):
                        for i in range(1, 176):
                            search_url = \
                                self.search_start_url +str(k)+ '&companyType=' +str(t)+ '&salary=' +str(s)+ '&degree=0&refreshTime=0&workAge=0&page=' +str(i)
                                # http://www.chinahr.com/sou/?city=0&industrys=1100&companyType=0&salary=0&degree=0&refreshTime=0&workAge=0
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

        # load = SpiderChinahrLoader(SpiderChinahrItem(), response)
        # ## need to think about how to get position related information, besides only company information, and add to this part
        # load.add_xpath('chr_co_name', '//h1/text()')
        # load.add_xpath('chr_co_city', '//div[@class="wrap-mc"]/em[1]/text()')
        # load.add_xpath('chr_co_industry', '//div[@class="wrap-mc"]/em[2]/text()')
        # load.add_xpath('chr_co_type', '//div[@class="wrap-mc"]/em[3]/text()')
        # load.add_xpath('chr_co_estab', '//div[@class="wrap-mc"]/em[4]/text()')
        # load.add_xpath('chr_co_regcap', '//div[@class="wrap-mc"]/em[5]/text()')
        # load.add_xpath('chr_contact_name', '//i[@class="icon_hf people"]/parent::p/text()')
        # load.add_xpath('chr_mobile_num', '//i[@class="icon_hf mobile"]/parent::p/text()')
        # load.add_xpath('chr_fixline_num', '//i[@class="icon_hf tel"]/parent::p/text()')
        # load.add_xpath('chr_email_addr', '//i[@class="icon_hf email"]/parent::p/text()')
        # load.add_xpath('chr_co_address', '//i[@class="icon_hf add"]/parent::p/text()')
        # load.add_xpath('chr_co_desc', '//div[@class="article"]/text()')
        # load.add_value('chr_co_url', response.url)
        tree = Selector(response)
        item = SpiderChinahrItem()
        # load.add_xpath('chr_co_name', '//h1/text()')
        # item['chr_co_id'] = clean(str(tree.xpath().extract()))
        item['chr_co_name'] = clean(str(tree.xpath('//h1/text()').extract()))
        item['chr_co_city'] = clean(str(tree.xpath( '//div[@class="wrap-mc"]/em[1]/text()').extract()))
        item['chr_co_industry'] = clean(str(tree.xpath( '//div[@class="wrap-mc"]/em[2]/text()').extract()))
        item['chr_co_ownership'] = clean(str(tree.xpath( '//div[@class="wrap-mc"]/em[3]/text()').extract()))
        item['chr_co_estab'] = clean(str(tree.xpath( '//div[@class="wrap-mc"]/em[4]/text()').extract()))
        item['chr_co_regcap'] = clean(str(tree.xpath( '//div[@class="wrap-mc"]/em[5]/text()').extract()))
        item['chr_contact_name'] = clean(str(tree.xpath( '//i[@class="icon_hf people"]/parent::p/text()').extract()))
        item['chr_mobile_num'] = clean(str(tree.xpath('//i[@class="icon_hf mobile"]/parent::p/text()').extract()))
        item['chr_fixline_num'] = clean(str(tree.xpath('//i[@class="icon_hf tel"]/parent::p/text()').extract()))
        item['chr_email_addr'] = clean(str(tree.xpath('//i[@class="icon_hf email"]/parent::p/text()').extract()))
        item['chr_co_address'] = clean(str(tree.xpath('//i[@class="icon_hf add"]/parent::p/text()').extract()))
        item['chr_co_des'] = clean(str(tree.xpath('//div[@class="article"]/text()').extract()))
        # chr_co_url = clean(str(tree.xpath('/html/head/link[6]/@href').extract()))
        # print(type(response.url))
        item['chr_co_url'] = response.url
        # item['chr_co_url'] = clean(str(tree.xpath('//*[@id="yc_seo"]/div[1]/a[3]/@href').extract()))

        yield item

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
