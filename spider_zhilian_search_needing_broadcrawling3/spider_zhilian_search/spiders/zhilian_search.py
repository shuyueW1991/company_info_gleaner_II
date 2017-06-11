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


import requests
from lxml import html

date=time.strftime("%Y%m%d",time.localtime(time.time()))

class SpiderZhilianSearchSpider(scrapy.Spider):
    name = "zhiliansearch2"

    def start_requests(self):
        yield scrapy.Request('http://sou.zhaopin.com/jobs/searchresult.ashx?kw=%s&p=1' %self.searchword, callback=self.parse_page)


    def parse_page(self, response):
        sel = Selector(response)
        titles = sel.xpath('//div[@class="newlist_list_content"]/table[position()>1]')



        for title in titles:

            inside_page = title.xpath('tr/td[@class="gsmc"]/a/@href').extract_first()
            print('insidepage:')
            print(inside_page)

            item = SpiderZhilianSearchItem()

            item['job_nm'] = title.xpath('tr/td[@class="zwmc"]/div/a/text()').extract()
            item['month_pay'] = title.xpath('tr/td[@class="zwyx"]/text()').extract()
            item['job_loc'] = title.xpath('tr/td[@class="gzdd"]/text()').extract()

            # if inside_page is not None:
            if inside_page.startswith('http://company.zhaopin.com'):

                print('we go to deep!')
                try:

                    company_page = requests.get(inside_page)

                    print('the parsing result is '.format(company_page.status_code))
                    tree = html.fromstring(company_page.content)
                    item['co_id'] = tree.xpath('//input[@id="companyNumber"]/@value')
                    item['co_nm'] = list(tree.xpath('//div[@class="mainLeft"]/div[1]/h1/text()'))[0].replace('|',"").replace("\n","").replace('\t',"").replace('\r',"").replace(' ',"")
                    item['co_ownership'] = str(tree.xpath('//table[@class="comTinyDes"]/tr[1]/td[2]/span/text()'))[2:-2].replace('|',"").replace("\n","").replace('\t',"").replace('\r',"").replace(' ',"")
                    item['co_ee_size'] = str(tree.xpath('//table[@class="comTinyDes"]/tr[2]/td[2]/span/text()'))[2:-2].replace('|',"").replace("\n","").replace('\t',"").replace('\r',"").replace(' ',"")
                    item['co_link'] = str(tree.xpath('//table[@class="comTinyDes"]//tr[3]/td[2]/span/a/text()'))[2:-2]
                    item['co_industry'] = str(tree.xpath('//table[@class="comTinyDes"]//tr[4]/td[2]/span/text()'))[2:-2].replace('|',"").replace("\n","").replace('\t',"").replace('\r',"").replace(' ',"")
                    item['co_add'] = str(tree.xpath('//table[@class="comTinyDes"]//tr[5]/td[2]/span/text()'))[2:-2].replace('|',"").replace("\n","").replace('\t',"").replace('\r',"").replace(' ',"")
                    # item['co_desc'] = str(tree.xpath('//div[@class="company-content"]/p')).replace("<p>","").replace("</p>","").replace("<br>","").replace("&nbsp","").replace('|',"").replace("\n","").replace('\t',"").replace('\r',"").replace(' ',"")
                    item['co_desc'] = tree.xpath('//div[@style="FONT-SIZE: 12px"]')

                    yield item

                    # yield scrapy.Request(inside_page, callback=self.parse_inside)
                except:
                    print('ight,nigga!')
            else:
                print('not zhilian webpages')
                item['co_id'] = 'unavailabe on zhilian itself'
                item['co_nm'] = 'unavailabe on zhilian itself'
                item['co_ownership'] = 'unavailabe on zhilian itself'
                item['co_ee_size'] = 'unavailabe on zhilian itself'
                item['co_link'] = 'unavailabe on zhilian itself'
                item['co_industry'] = 'unavailabe on zhilian itself'
                item['co_add'] = 'unavailabe on zhilian itself'
                # item['co_desc'] = str(tree.xpath('//div[@class="company-content"]/p')).replace("<p>","").replace("</p>","").replace("<br>","").replace("&nbsp","").replace('|',"").replace("\n","").replace('\t',"").replace('\r',"").replace(' ',"")
                item['co_desc'] = 'unavailabe on zhilian itself'
                print('shit happens!!!!In inside-process!!\n')
                yield item


        next_page = sel.xpath('//li[@class="pagesDown-pos"]/a/@href').extract_first()
        if next_page is not None:
            # next_page = response.urljoin(next_page)
            # yield SplashRequest(next_page, self.parse_title, endpoint='render.html', args={'wait': 0.5})
            yield scrapy.Request(next_page, self.parse_page)
        else:
            print('No next pages, nigga!!\n')

    # def parse_error(self, response):
        # print('there is an error!')

    # def parse_inside(self, response):
        # print('parsing in company page has been started!')
        #
        # load = SpiderZhilianSearchLoader(SpiderZhilianSearchItem(), response)
        # load.add_xpath('co_id','//input[@id="companyNumber"]/@value')
        # load.add_xpath('co_nm','//div[@class="mainLeft"]/div[1]/h1/text()')
        # load.add_xpath('co_ownership','//table[@class="comTinyDes"]/ tbody/tr[1]/td[2]/span/text()')
        # load.add_xpath('co_ee_size', '//table[@class="comTinyDes"]/tbody/tr[2]/td[2]/span/text()')
        # load.add_xpath('co_link','//table[@class="comTinyDes"]//tr[3]/td[2]/span/a/text()')
        # load.add_xpath('co_industry','//table[@class="comTinyDes"]//tr[4]/td[2]/span/text()')
        # load.add_xpath('co_add','//table[@class="comTinyDes"]//tr[5]/td[2]/span/text()')
        # load.add_xpath('co_desc','//div[@class="company-content"]/p/text()')
        #
        # yield load.load_item()



        #
        # print('parsing started!')
        #
        # sel = Selector(response)
        # item = SpiderZhilianSearchItem()
        # item['co_id'] = sel.xpath('//input[@id="companyNumber"]/@value').extract()
        # item['co_nm'] = sel.xpath('//div[@class="mainLeft"]/div[1]/h1/text()').extract()
        # item['co_ownership'] = sel.xpath('//table[@class="comTinyDes"]/ tbody/tr[1]/td[2]/span/text()').extract()
        # item['co_ee_size'] = sel.xpath('//table[@class="comTinyDes"]/tbody/tr[2]/td[2]/span/text()').extract()
        # item['co_link'] = sel.xpath('//table[@class="comTinyDes"]//tr[3]/td[2]/span/a/text()').extract()
        # item['co_industry'] = sel.xpath('//table[@class="comTinyDes"]//tr[4]/td[2]/span/text()').extract()
        # item['co_add'] = sel.xpath('//table[@class="comTinyDes"]//tr[5]/td[2]/span/text()').extract()
        # item['co_desc'] = sel.xpath('//div[@class="company-content"]/p/text()').extract()
        #
        # yield item