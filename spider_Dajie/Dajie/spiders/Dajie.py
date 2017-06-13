 # -*- coding: utf-8 -*-
import scrapy
from Dajie.items import DajieItem
from Dajie.items import DajieLoader
from scrapy.selector import Selector
# from scrapy_splash import SplashRequest
import random
import time
import datetime



class Dajie(scrapy.Spider):
    name = "Dajie"
    allowed_domains = ["https://www.dajie.com"]

    def start_requests(self):
        for i in range(1000000,9999999):
            # start_urls=['http://jobs.51job.com/all/co'+str(i)+'.html']
            start_urls=["https://www.dajie.com/corp/"+str(i)]
            for url in start_urls:
                yield scrapy.Request(url, callback=self.parse_page)
                # yield SplashRequest(url, self.parse_page,args={'wait':0.5})


    def parse_page(self,response):

        link_container= DajieLoader(item=DajieItem(), response=response)

        # item=DajieLoader()
        # item["co_web_id"] = link_container.add_xpath('co_web_id', '//*[@id="J_corNav"]/li[1]/a')
        # item["co_name"] = link_container.add_xpath('co_name', '//h1/text()')
        # item["co_number"] = link_container.add_xpath('co_number', '//dl[@class="card-detail"]/dd[2]/span[2]/text()')
        # item["co_add"] = link_container.add_xpath('co_add', '//dl[@class="card-detail"]/dd[3]/span[2]/text()')
        # item["co_type"] = link_container.add_xpath('co_type', '//dl[@class="card-detail"]/dd[4]/span[2]/text()')
        # link_container.add_xpath('co_web_add', '//dl[@class="card-detail"]/dd[5]/span[2]/a/@href')
        #
        # if link_container['co_web_add']:
        #     item["co_web_add"] = link_container.add_xpath('co_web_add',
        #                                              '//dl[@class="card-detail"]/dd[5]/span[2]/a/@href')
        #     yield item.load_item()
        # else:
        #     item["co_web_add"]="unavailable"
        #     yield item.load_item()

        # link_container.add_value('Chinahr_co_web_id', 'repr(url)')
        # co_container = load.nested_xpath('//div[@class="tCompany_full"]/div[@class="tBorderTop_box bt"]/div[@class="tmsg inbox"]/div[@class="con_msg"]/div[@class="in"]')


        link_container.add_xpath('co_web_id', '//*[@id="J_corNav"]/li[1]/a')
        link_container.add_xpath('co_name', '//h1/text()')
        link_container.add_xpath('co_number', '//dl[@class="card-detail"]/dd[2]/span[2]/text()')
        link_container.add_xpath('co_add', '//dl[@class="card-detail"]/dd[3]/span[2]/text()')
        link_container.add_xpath('co_type', '//dl[@class="card-detail"]/dd[4]/span[2]/text()')
        link_container.add_xpath('co_web_add', '//dl[@class="card-detail"]/dd[5]/span[2]/text()|//dl[@class="card-detail"]/dd[5]/span[2]/a/@href')


        yield link_container.load_item()


    def parse_error(self, response):
        print("Error Occured")
        print(response.status)
