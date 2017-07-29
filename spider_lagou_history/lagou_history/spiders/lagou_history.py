# -*- coding: utf-8 -*-
import re
import scrapy
import datetime
import time
from lagou_history.items import LagouHistoryItem
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lagou_history.items import LagouHistroyLoader
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector


date=time.strftime("%Y%m%d",time.localtime(time.time()))


class LagouHistorySpider(scrapy.Spider):
    name = "lagou_history"
    # start_urls = 'https://www.lagou.com/gongsi/43743.html'
    # start_urls = 'https://www.lagou.com/gongsi/13712.html'

    # def start_requests(self, url=start_urls):
    def start_requests(self):
        # yield scrapy.Request(url, callback=self.parse_co)
        for i in range(0,300000):
            start_urls = ["https://www.lagou.com/gongsi/"+str(i)+".html"]
            for url in start_urls:
                yield scrapy.Request(url, callback=self.parse_co)

    def parse_co(self, response, date=date):
        load = LagouHistroyLoader(LagouHistoryItem(), response)

        upper_container = load.nested_xpath('//div[@class="company_main"]/h1/a')
        upper_container.add_xpath('lg_co_name', '@title')
        upper_container.add_xpath('lg_co_website', '@href')

        right_container = load.nested_xpath('//div[@id="basic_container"]/div[@class="item_content"]/ul')
        right_container.add_xpath('lg_co_tags', 'li[1]')
        right_container.add_xpath('lg_co_rounds', 'li[2]')
        right_container.add_xpath('lg_co_ee_size', 'li[3]')
        right_container.add_xpath('lg_co_city', 'li[4]')

        load.add_xpath('lg_mgmt_name','//script[@id="companyInfoData"]')
        load.add_xpath('lg_mgmt_title','//script[@id="companyInfoData"]')
        load.add_xpath('lg_mgmt_desc','//script[@id="companyInfoData"]')

        load.add_xpath('lg_prd_name','//script[@id="companyInfoData"]')
        load.add_xpath('lg_prd_desc','//script[@id="companyInfoData"]')
        load.add_xpath('lg_co_desc','//script[@id="companyInfoData"]')

        load.add_xpath('lg_num_position','//script[@id="companyInfoData"]')
        load.add_xpath('lg_handle_rate','//script[@id="companyInfoData"]')
        load.add_xpath('lg_handle_time','//script[@id="companyInfoData"]')
        load.add_xpath('lg_num_review','//script[@id="companyInfoData"]')
        load.add_xpath('lg_co_id', '//script[@id="companyInfoData"]')

        load.add_value('lg_update_time', repr(date))

        yield load.load_item()


    def parse_hiring(self,response):
        pass

    def parse_pos(self, response):
        pass