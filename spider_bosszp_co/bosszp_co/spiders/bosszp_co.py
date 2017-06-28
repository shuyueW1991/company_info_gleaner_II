# -*- coding: utf-8 -*-
import scrapy
from bosszp_co.items import BosszpCoItem
from bosszp_co.items import BosszpCoLoader
from scrapy.selector import Selector
# from scrapy.linkextractors import LinkExtractor
# from scrapy.contrib.spiders import Rule

import random
import time
import datetime


class BosszpCoSpider(scrapy.Spider):
    name = "bosszpcospider"
    allowed_domains = ["www.zhipin.com"]

    def start_requests(self):
        for i in range(1,999999):
            start_urls=['https://www.zhipin.com/gongsi/'+str(i)+'.html?ka=company-intro']
            for url in start_urls:
                yield scrapy.Request(url, self.parse_page)


    def parse_page(self,response):

        load = BosszpCoLoader(item=BosszpCoItem(), response=response)

        link_container = load.nested_xpath('//div[@class="job-primary"]/div[@class="company-stat"]')
        link_container.add_xpath('bosszp_co_web_id', 'span[1]/a/@href')
        link_container.add_xpath('co_emply_blank', 'span[1]/a/b/text()')
        link_container.add_xpath('co_boss_num', 'span[2]/b/text()')

        co_container = load.nested_xpath('//div[@class="job-primary"]/div[@class="info-primary"]')
        co_container.add_xpath('co_short_nm', 'h3[@class="name"]/text()')
        co_container.add_xpath('co_financing_round', 'p[1]')
        co_container.add_xpath('co_staff_num', 'p[1]')
        co_container.add_xpath('co_type', 'p[1]')
        co_container.add_xpath('co_link', 'p[2]')
        co_container.add_xpath('co_staff_num', 'span[3]/text()')

        co_containerother = load.nested_xpath('//div[@class="job-sec"]')

        co_containerother.add_xpath('co_short_desc','div[@class="text fold-text"]/text()')


        # load.add_value('lg_update_time', repr(date))


        yield load.load_item()
