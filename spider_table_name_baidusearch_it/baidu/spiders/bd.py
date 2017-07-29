# -*- coding: utf-8 -*-
import scrapy
from baidu.items import BaiduLeftNonbdItem
# from baidu.items import BaiduLeftBdItem

from scrapy.selector import Selector


import random
import time
import datetime


class BdSpider(scrapy.Spider):
    name = "bdsearch"
    allowed_domains = ["www.baidu.com"]

    def start_requests(self):
        yield scrapy.Request('https://www.baidu.com/s?wd=%s' %self.searchword, self.parse_keyword)
        # yield scrapy.Request('https://www.baidu.com/s?wd=baidu', self.parse_keyword)

    def parse_keyword(self,response):
        sel = Selector(response)
        title_left = sel.xpath('//div[@id="container"]/div[@id="content_left"]')
        title_left_nonbd = title_left.xpath('div[@class="result c-container "]')
        # title_left_bd = title_left.xpath('div[@class="result-op c-container xpath-log"]')

        # for title1 in title_left_nonbd:
        #     item1 = BaiduLeftNonbdItem()
        #     item1['bd_coname'] = self.searchword
        #     item1['bd_ln_head'] = title1.xpath('h3[@class="t"]').extract()
        #     item1['bd_ln_abs'] = title1.xpath('div[@class="c-abstract"]').extract()
        #     yield item1

        item1 = BaiduLeftNonbdItem()
        item1['bd_coname'] = self.searchword

        item1['bd_ln_head'] = ['']
        item1['bd_ln_abs'] = ['']
        # print('initial status type is :\n')
        # print(type(item1['bd_ln_head']))
        # print(type(item1['bd_ln_abs']))


        for title1 in title_left_nonbd:
            head = title1.xpath('h3[@class="t"]').extract()
            item1['bd_ln_head'].extend(head)
            abs = title1.xpath('div[@class="c-abstract"]').extract()
            item1['bd_ln_abs'].extend(abs)


        # print('resulting type is :\n')
        # print(type(item1['bd_ln_abs']))
        if  len(item1['bd_ln_abs']) is 1:
            print('roll it back, nigga!\n')
            scrapy.Request('https://www.baidu.com/s?wd=%s' % self.searchword, self.parse_keyword)
        else:
            yield item1






        # for title2 in title_left_bd:
        #     item2 = BaiduLeftBdItem()
        #     item2['bd_coname'] = self.searchword
        #     item2['bd_lb_txt'] = title2.extract()
        #     yield item2


