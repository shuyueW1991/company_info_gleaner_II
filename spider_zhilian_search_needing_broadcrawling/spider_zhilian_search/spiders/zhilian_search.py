# -*- coding: utf-8 -*-
import re
import scrapy
import datetime
from scrapy.selector import Selector
import time
from spider_zhilian_search.items import SpiderZhilianSearchItem
# from scrapy.linkextractors import LinkExtractor
# from scrapy.spiders import CrawlSpider, Rule
from spider_zhilian_search.items import SpiderZhilianSearchLoader


date=time.strftime("%Y%m%d",time.localtime(time.time()))

class SpiderZhilianSearchSpider(scrapy.Spider):
    name = "zhiliansearch"
    allowed_domains = "sou.zhaopin.com"

    def start_requests(self):
        yield scrapy.Request('http://sou.zhaopin.com/jobs/searchresult.ashx?kw=%s&p=1' %self.searchword, callback=self.parse_page)

    def parse_page(self, response):
        sel = Selector(response)
        titles = sel.xpath('//div[@class="newlist_list_content"]/table[position()>1]')


        for title in titles:

            inside_page = title.xpath('tr/td[@class="gsmc"]/a/@href').extract_first()
            print('insidepage:')
            print(inside_page)
            print('endofinsedpage!!!')

            if inside_page is not None:
                print('we go to deep!')
                yield scrapy.Request(str(inside_page), self.parse_inside)
            else:
                print('shit happens!!!nigga!In inside-process!!\n')

            time.sleep(5)


        next_page = sel.xpath('//li[@class="pagesDown-pos"]/a/@href').extract_first()
        if next_page is not None:
            # next_page = response.urljoin(next_page)
            # yield SplashRequest(next_page, self.parse_title, endpoint='render.html', args={'wait': 0.5})
            yield scrapy.Request(next_page, self.parse_page)
        else:
            print('No next pages, nigga!!\n')


    def parse_inside(self, response):
        # print('been in a webpage, nigga!')
        load = SpiderZhilianSearchLoader(SpiderZhilianSearchItem(), response)
        load.add_xpath('co_id','//link[@rel="canonical"]/@ref')
        load.add_xpath('co_nm','//div[@class="mainLeft"]/div[1]/h1/text()')
        load.add_xpath('co_ownership','//table[@class="comTinyDes"]/tbody/tr[1]/td[2]/span/text()')
        load.add_xpath('co_ee_size', '//table[@class="comTinyDes"]/tbody/tr[2]/td[2]/span/text()')
        load.add_xpath('co_link','//table[@class="comTinyDes"]//tr[3]/td[2]/span/a/text()')
        load.add_xpath('co_industry','//table[@class="comTinyDes"]//tr[4]/td[2]/span/text()')
        load.add_xpath('co_add','//table[@class="comTinyDes"]//tr[5]/td[2]/span/text()')
        load.add_xpath('co_desc','//div[@class="company-content"]/p/text()')

        yield load.load_item()