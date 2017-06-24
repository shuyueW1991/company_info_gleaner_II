# -*- coding: utf-8 -*-
import scrapy
from liepin.items import LiepinItem

# from scrapy_splash import SplashRequest
from scrapy.selector import Selector
# from scrapy.linkextractors import LinkExtractor
# from scrapy.contrib.spiders import Rule

import random
import time
import datetime


class LpSpider(scrapy.Spider):
    name = "lp190_3"
    allowed_domains = ["www.liepin.com"]

    def start_requests(self):
        for i in range(190000000,194000000):
        # for i in range(198013900,198014000): # pour test
            start_urls=['https://www.liepin.com/job/'+str(i)+'.shtml']
            for url in start_urls:
#               if i % 20 == 0:
#                    time.sleep(5)
                yield scrapy.Request(url, self.parse_ext)

    def parse_ext(self,response):
        sell = Selector(response)

        item = LiepinItem()
        item['lp_exist'] = sell.xpath('//div[@id="error404_box"]/div/dl/dd[last()-1]/h1/text()').extract()

        item['lp_job_id'] = sell.xpath('//head/link[@rel="canonical"]/@href').extract()

        item['lp_co_nm'] = sell.xpath('//div[@class="company-infor"]/h4/a[last()-1]/text()').extract()
        item['lp_co_lk'] = sell.xpath('//div[@class="company-infor"]/h4/a/@href').extract()
        item['lp_co_tag']= sell.xpath('//div[@class="company-infor"]/ul/li[last()-2]/a/@title').extract()
        item['lp_co_stf_num'] = sell.xpath('//div[@class="company-infor"]/ul/li[last()-1]/text()').extract()
        item['lp_co_ownership'] = sell.xpath('//div[@class="company-infor"]/ul/li[last()]/text()').extract()
        item['lp_co_add'] = sell.xpath('//div[@class="company-infor"]/p/text()').extract()
        item['lp_co_intro'] = sell.xpath('//div[@class="job-item main-message noborder"]/div[@class="content content-word"]/text()').extract()

        item['lp_job_pub_nm'] = sell.xpath('//p[@class="publisher-name"]/span/text()').extract()
        item['lp_job_pub_pos'] = sell.xpath('//p[@class="publisher-name"]/em/text()').extract()
        item['lp_job_apply_check_rate'] = sell.xpath('//div[@class="apply-check"]/span[last()-1]/em/text()').extract()
        item['lp_job_apply_check_dur'] = sell.xpath('//div[@class="apply-check"]/span[last()]/em/text()').extract()

        item['lp_job_nm'] = sell.xpath('//div[@class="about-position"]/div[@class="title-info"]/h1/@title').extract()
        item['lp_job_salary'] = sell.xpath('//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="job-item-title"]/text()').extract()
        item['lp_job_apply_fdbk'] = sell.xpath('//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="job-item-title"]/span/text()').extract()
        item['lp_job_add'] = sell.xpath('//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="basic-infor"]/span[last()-1]/a/text()').extract()
        item['lp_job_pub_time'] = sell.xpath('//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="basic-infor"]/span[last()]/text()').extract()
        item['lp_job_quals'] = sell.xpath('//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/div[@class="job-qualifications"]/span/text()').extract()
        item['lp_job_descr'] = sell.xpath('//div[@class="job-item main-message"]/div[@class="content content-word"]/text()').extract()
        item['lp_job_dept'] = sell.xpath('//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()-3]/label/text()').extract()
        item['lp_job_major'] = sell.xpath('//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()-2]/label/text()').extract()
        item['lp_job_boss'] = sell.xpath('//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()-1]/label/text()').extract()
        item['lp_job_subordinate'] = sell.xpath('//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()]/label/text()').extract()
        item['lp_update_datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield item
