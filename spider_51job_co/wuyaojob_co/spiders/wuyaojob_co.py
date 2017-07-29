# -*- coding: utf-8 -*-
import scrapy
from wuyaojob_co.items import WuyaojobCoItem
from wuyaojob_co.items import WuyaojobCoLoader
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
import random
import time
import datetime


class BosszpCoSpider(scrapy.Spider):
    name = "wuyaojobcospider"
    allowed_domains = ["m.51job.com"]

    def start_requests(self):
        for i in range(2000000,4000000):
            # start_urls=['http://jobs.51job.com/all/co'+str(i)+'.html']
            start_urls=['http://m.51job.com/campus/search/codetail.php?coid='+str(i)]
            for url in start_urls:
                yield scrapy.Request(url, self.parse_page)
                # yield SplashRequest(url, self.parse_page,args={'wait':0.5})


    def parse_page(self,response):

        load = WuyaojobCoLoader(item=WuyaojobCoItem(), response=response)

        link_container = load.nested_xpath('//div[@class="xq qhd"]')
        link_container.add_xpath('co_nm', 'p/text()')
        link_container.add_xpath('co_ownership', 'div[@class="xqd x2"]/label[2]/text()')
        link_container.add_xpath('co_staff_num', 'div[@class="xqd x2"]/label[1]/text()')
        link_container.add_xpath('co_type', 'div[@class="xqd x2"]')

        # co_container = load.nested_xpath('//div[@class="tCompany_full"]/div[@class="tBorderTop_box bt"]/div[@class="tmsg inbox"]/div[@class="con_msg"]/div[@class="in"]')
        co_container = load.nested_xpath('//div[@class="xqp"]')
        co_container.add_xpath('co_short_desc', 'text()')

        co_container = load.nested_xpath('//form[@id="mapForm"]')
        co_container.add_xpath('co_add', 'p/text()')
        co_container.add_xpath('wuyaojob_co_web_id', 'input/@value')


        # load.add_value('lg_update_time', repr(date))


        yield load.load_item()
