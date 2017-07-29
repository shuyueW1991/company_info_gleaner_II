# -*- coding: utf-8 -*-
import scrapy
from liepin.items import LiepinItem
from liepin.items import LiepinLoader
from scrapy.selector import Selector
import random
import time
import datetime


class LpSpider(scrapy.Spider):
    name = "lpsearch"
    allowed_domains = ["www.liepin.com"]

    def start_requests(self):
        # start_urls=['https://www.liepin.com/job/'+str(i)+'.shtml']
        # start_urls=['https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key='+
        yield scrapy.Request('https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&key=%s' %self.searchword, self.parse_title)

    def parse_title(self,response):

        sel = Selector(response)
        titles = sel.xpath('//div[@class="sojob-item-main clearfix"]')
        # item = LiepinItem()

        for title in titles:
            inside_page = title.xpath('div[@class="job-info"]/h3/a/@href').extract_first()
            if inside_page is not None:
                yield scrapy.Request(inside_page, self.parse_inside)
            else:
                print('shit happens!!!nigga!\n')


            # item = LiepinItem()
            # item['lp_job'] =title.xpath('div[@class="job-info"]/h3/a/text()').extract()
            # item['lp_pay'] = title.xpath('div[@class="job-info"]/p[@class="condition clearfix"]/span[@class="text-warning"]/text()').extract()
            # item['lp_location'] = title.xpath('div[@class="job-info"]/p[@class="condition clearfix"]/a/text()').extract()
            # item['lp_diploma'] = title.xpath('div[@class="job-info"]/p[@class="condition clearfix"]/span[@class="edu"]/text()').extract()
            # item['lp_exp'] = title.xpath('div[@class="job-info"]/p[@class="condition clearfix"]/span[last()]/text()').extract()
            #
            # item['lp_co_nm'] = title.xpath('div[@class="company-info nohover"]/p[@class="company-name"]/a/text()').extract()
            # item['lp_co_lk'] = title.xpath('div[@class="company-info nohover"]/p[@class="company-name"]/a/@href').extract()
            # item['lp_co_fld'] = title.xpath('div[@class="company-info nohover"]/p[@class="field-financing"]/span/a/text()').extract()
            # item['lp_welfare'] = title.xpath('div[@class="company-info nohover"]/p[@class="temptation clearfix"]/span/text()').extract()
            #
            # item['lp_rls_time'] = title.xpath('div[@class="job-info"]/p[@class="time-info clearfix"]/time/text()').extract()
            # item['lp_fdbktime'] = title.xpath('div[@class="job-info"]/p[@class="time-info clearfix"]/span/text()').extract()
            # item['lp_update_datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #
            # yield item


        next_page = sel.xpath('//div[@class="pagerbar"]/a[last()-1]/@href').extract_first()
        # time.sleep(3)
        if next_page is not None:
            # next_page = response.urljoin(next_page)
            # yield SplashRequest(next_page, self.parse_title, endpoint='render.html', args={'wait': 0.5})
            yield scrapy.Request(next_page, self.parse_title)
        else:
            print('shit happens!!!nigga!\n')


    def parse_inside(self,response):
        sell = Selector(response)

        item = LiepinItem()

        load = LiepinLoader(LiepinItem(), response)

#	print('benn in the inside page, nigga!')
        load.add_xpath('lp_job_id','//head/link[@rel="canonical"]/@href')
        load.add_xpath('companyFullName','//div[@class="company-infor"]/h4/a[last()-1]/text()')
        load.add_xpath('lp_co_lk','//div[@class="company-infor"]/h4/a/@href')
        load.add_xpath('industryField','//div[@class="company-infor"]/ul/li[last()-2]/a/@title')
        load.add_xpath('companySize','//div[@class="company-infor"]/ul/li[last()-1]/text()')


        load.add_xpath('financeStage','//div[@class="company-infor"]/ul/li[last()]/text()')
        load.add_xpath('lp_co_add','//div[@class="company-infor"]/p/text()')
        load.add_xpath('lp_co_intro','//div[@class="job-item main-message noborder"]/div[@class="content content-word"]/text()')
        load.add_xpath('lp_job_pub_nm','//p[@class="publisher-name"]/span/text()')
        load.add_xpath('lp_job_pub_pos','//p[@class="publisher-name"]/em/text()')
        load.add_xpath('lp_job_apply_check_rate','//div[@class="apply-check"]/span[last()-1]/em/text()')
        load.add_xpath('lp_job_apply_check_dur','//div[@class="apply-check"]/span[last()]/em/text()')
        load.add_xpath('positionName','//div[@class="about-position"]/div[@class="title-info"]/h1/@title')
        load.add_xpath('salary','//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="job-item-title"]/text()')
        load.add_xpath('lp_job_apply_fdbk','//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="job-item-title"]/span/text()')
        load.add_xpath('lp_job_add','//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="basic-infor"]/span[last()-1]/a/text()')
        load.add_xpath('lp_job_pub_time','//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="basic-infor"]/span[last()]/text()')
        load.add_xpath('lp_job_quals','//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/div[@class="job-qualifications"]/span/text()')
        load.add_xpath('description','//div[@class="job-item main-message"]/div[@class="content content-word"]/text()')
        load.add_xpath('lp_job_dept','//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()-3]/label/text()')
        load.add_xpath('lp_job_major','//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()-2]/label/text()')
        load.add_xpath('lp_job_boss','//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()-1]/label/text()')
        load.add_xpath('lp_job_subordinate','//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()]/label/text()')

        yield load.load_item()




        # item = LiepinItem()
        # item['lp_job_id'] = sell.xpath('//head/link[@rel="canonical"]/@href').extract()
        # item['lp_co_nm'] = sell.xpath('//div[@class="company-infor"]/h4/a[last()-1]/text()').extract()
        # item['lp_co_lk'] = sell.xpath('//div[@class="company-infor"]/h4/a/@href').extract()
        # item['lp_co_tag'] = sell.xpath('//div[@class="company-infor"]/ul/li[last()-2]/a/@title').extract()
        # item['lp_co_stf_num'] = sell.xpath('//div[@class="company-infor"]/ul/li[last()-1]/text()').extract()
        # item['lp_co_ownership'] = sell.xpath('//div[@class="company-infor"]/ul/li[last()]/text()').extract()
        # item['lp_co_add'] = sell.xpath('//div[@class="company-infor"]/p/text()').extract()
        # item['lp_co_intro'] = sell.xpath(
        #     '//div[@class="job-item main-message noborder"]/div[@class="content content-word"]/text()').extract()
        #
        # item['lp_job_pub_nm'] = sell.xpath('//p[@class="publisher-name"]/span/text()').extract()
        # item['lp_job_pub_pos'] = sell.xpath('//p[@class="publisher-name"]/em/text()').extract()
        # item['lp_job_apply_check_rate'] = sell.xpath('//div[@class="apply-check"]/span[last()-1]/em/text()').extract()
        # item['lp_job_apply_check_dur'] = sell.xpath('//div[@class="apply-check"]/span[last()]/em/text()').extract()
        #
        # item['lp_job_nm'] = sell.xpath('//div[@class="about-position"]/div[@class="title-info"]/h1/@title').extract()
        # item['lp_job_salary'] = sell.xpath(
        #     '//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="job-item-title"]/text()').extract()
        # item['lp_job_apply_fdbk'] = sell.xpath(
        #     '//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="job-item-title"]/span/text()').extract()
        # item['lp_job_add'] = sell.xpath(
        #     '//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="basic-infor"]/span[last()-1]/a/text()').extract()
        # item['lp_job_pub_time'] = sell.xpath(
        #     '//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/p[@class="basic-infor"]/span[last()]/text()').extract()
        # item['lp_job_quals'] = sell.xpath(
        #     '//div[@class="about-position"]/div[@class="job-item"]/div[@class="clearfix"]/div[@class="job-title-left"]/div[@class="job-qualifications"]/span/text()').extract()
        # item['lp_job_descr'] = sell.xpath(
        #     '//div[@class="job-item main-message"]/div[@class="content content-word"]/text()').extract()
        # item['lp_job_dept'] = sell.xpath(
        #     '//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()-3]/label/text()').extract()
        # item['lp_job_major'] = sell.xpath(
        #     '//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()-2]/label/text()').extract()
        # item['lp_job_boss'] = sell.xpath(
        #     '//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()-1]/label/text()').extract()
        # item['lp_job_subordinate'] = sell.xpath(
        #     '//div[@class="job-item main-message"]/div[@class="content"]/ul/li[last()]/label/text()').extract()
        # item['lp_update_datetime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # yield item


