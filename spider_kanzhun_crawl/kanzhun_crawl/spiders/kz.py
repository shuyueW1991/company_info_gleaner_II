# -*- coding: utf-8 -*-
import scrapy
from kanzhun_crawl.items import KanzhunCrawlItem
from kanzhun_crawl.items import KanzhunCrawlLoader
from scrapy.selector import Selector
# from scrapy.linkextractors import LinkExtractor
# from scrapy.contrib.spiders import Rule

import random
import time
import datetime


class KanzhunSpider(scrapy.Spider):
    name = "kzspider"
    allowed_domains = ["www.kanzhun.com"]
    # url = -1


    def start_requests(self):
        starttime = time.time()

        for i in range(0,50000):
            start_urls=['https://www.kanzhun.com/gso'+str(i)+'.html?ka=com1-title']
            # self.url = i
            for url in start_urls:
                yield scrapy.Request(url, self.parse_ext)

        endtime = time.time()
        deltatime = endtime-starttime
        print('time duration:')
        print(deltatime)

    def parse_ext(self,response):
        # sell = Selector(response)

        load = KanzhunCrawlLoader(item=KanzhunCrawlItem(), response=response)
        load.add_xpath('co_short_nm','//div[@class="banner_word"]/div[@class="bw_company"]/h1/text()')

        co_container = load.nested_xpath('//div[@class="banner_word"]/div[@class="bw_explain"]')
        co_container.add_xpath('co_type', 'span[1]/text()')
        co_container.add_xpath('co_city', 'span[2]/text()')
        co_container.add_xpath('co_staff_num', 'span[3]/text()')

        load.add_xpath('co_short_desc','//div[@class="banner_word"]/div[@class="bw_brief"]/text()')
        load.add_xpath('co_goodcommnt_rate','//div[@class="ci_left"]/span[@class="cil_perc"]/text()')
        load.add_xpath('co_goodcommnt_rate_emply_num','//div[@class="ci_left"]/span[@class="cil_num"]/text()')
        load.add_xpath('co_avg_pay','//div[@class="ci_right"]/span[@class="cir_perc"]/text()')
        load.add_xpath('co_avg_pay_emply_num','//div[@class="ci_right"]/span[@class="cir_num"]/text()')

        # load.add_value('lg_update_time', repr(date))


        yield load.load_item()
