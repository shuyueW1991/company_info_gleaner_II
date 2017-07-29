# -*- coding: utf-8 -*-
import scrapy
import time
from itjuzi_history.items import ItjuziHistoryItem
from itjuzi_history.items import ItjuziHistoryLoader
from scrapy.selector import Selector

date=time.strftime("%Y%m%d",time.localtime(time.time()))

class ItjuziHistSpider(scrapy.Spider):
    name = "itjuzi_hist"

    def start_requests(self):
        for i in range(0,65000):
            start_urls = ["https://www.itjuzi.com/company/"+str(i)]
            for url in start_urls:
                yield scrapy.Request(url, callback=self.parse_co)

    def parse_co(self, response, date=date):
        # print(response.request.headers['User-Agent'])
        # print(response.request.meta['proxy'])
        load = ItjuziHistoryLoader(ItjuziHistoryItem(), response)

        load.add_xpath('it_co_id','//a[@id="loginurl"]/@href')
        load.add_xpath('it_short_name','//meta[@name="Keywords"]/@content')
        load.add_xpath('it_full_name','//input[@name="com_registered_name"]/@value')
        load.add_xpath('it_short_desc','//input[@name="com_slogan"]/@value')
        load.add_xpath('it_full_desc','//meta[@name="Description"]/@content')
        load.add_xpath('it_desc_tag','//div[@class="tagset dbi c-gray-aset"]/a/span[@class="tag"]/text()')
        load.add_xpath('it_ind_tag','//span[@class="scope c-gray-aset"]/a/text()')
        load.add_xpath('it_location','//span[@class="loca c-gray-aset"]/a/text()')
        load.add_xpath('it_website','//input[@name="com_url"]/@value')
        load.add_xpath('it_estab_time','//h2[@class="seo-second-title"][1]')
        load.add_xpath('it_ee_size','//select[@name="com_scale"]/option[@selected]')
        load.add_xpath('it_active_status','//select[@name="com_status_id"]/option[@selected]/text()')
        load.add_xpath('it_mgmt_name','//span[@class="c"]/text()')
        load.add_xpath('it_mgmt_desc','//h4[@class="person-name"]/ancestor::div[@class="right"]/p/text()')
        load.add_xpath('it_prd_info','//input[@name="pro_name"]/@value')
        load.add_xpath('it_co_views','//i[@class="fa fa-eye"]/ancestor::div/p/b')
        load.add_xpath('it_co_followers','//i[@class="fa fa-heart"]/ancestor::div/p/b')
        load.add_value('it_update_time', repr(date))

        invest_info = str("")
        table = response.xpath('//table[@class="list-round-v2"]/tr')
        for line in table:
            columns = line.xpath('td')
            for column in columns:
                element = column.xpath('span/a')
                if len(element) != 0:
                    invest_info += stripline(column.xpath('span/a/text()').extract()[0]) + ','
                element = column.xpath('a/text()')
                if len(element) != 0:
                    for e in element:
                        invest_info += stripline(e.extract() + ',')
                else:
                    element = column.xpath('span/text()')
                    for e in element:
                        invest_info += stripline(e.extract() + ',' )
            invest_info += ';'

        news = str("")
        sel = response.xpath('//ul[contains(@class,"list-news")]/li')
        for li in sel:
            e = str("")
            e += "link:" + stripline(li.xpath('div/p[1]/a/@href').extract()[0]) + ","
            e += 'text:' + stripline(li.xpath('div/p[1]/a/text()').extract()[0]) + ","
            e += 'time:' + stripline(li.xpath('div/p[2]/span[1]/text()').extract()[0]) + ","
            e += 'tag:' + stripline(li.xpath('div/p[2]/span[2]/text()').extract()[0]) + ","
            e += 'from:' + stripline(li.xpath('div/p[2]/span[2]/text()').extract()[0]) + ";"
            news += e

        milestone = []
        sel = response.xpath('//ul[contains(@class,"list-milestone")]/li')
        for li in sel:
            text = stripline(li.xpath('div/p/text()').extract()[0])
            time = stripline(li.xpath('div/p[2]/span/text()').extract()[0])
            milestone.append(text + "," + time)
        milestone = ";".join(milestone)

        load.add_value('it_investment_info',invest_info)
        load.add_value('it_news',news)
        load.add_value('it_milestone',milestone)

        yield load.load_item()

    def parse(self, response):
        pass

def stripline(str):
	return str.replace('\t','').replace('\n','')
