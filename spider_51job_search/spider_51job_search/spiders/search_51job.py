# -*- coding: utf-8 -*-
import scrapy
import json
import time
from lxml import html
import requests
from spider_51job_search.items import Spider51JobSearchItem
from spider_51job_search.items import search51jobLoader
from bs4 import BeautifulSoup as bs
from scrapy.selector import Selector

date=time.strftime("%Y%m%d",time.localtime(time.time()))

def clean(x):
    return x.replace('\r', '').replace('\t', '').replace('\n', '').replace("\n", '').replace('"', '').replace(" ", "").replace("\"", "").replace("|","")

class Search51jobSpider(scrapy.Spider):
    name = "search_51job"
    keyword = "海外"
    cur_page = 0
    ## headers are for the request package
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}

    search_start_url = "http://search.51job.com/jobsearch/search_result.php?keyword="+keyword
    # search_start_url = "http://search.51job.com/jobsearch/search_result.php?jobarea=360000"
    # print("the start url is {}".format(search_start_url))

    def start_requests(self):
        yield scrapy.Request(self.search_start_url, callback=self.parse_page)

    def parse_page(self, response):
        out = Spider51JobSearchItem()
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        iterators = response.xpath('//div[@class="dw_table"]/div[@class="el"]')
        for item in iterators:
            out['qc_job_name'] = item.xpath('p/span/a/@title').extract()
            out['qc_co_name'] = item.xpath('span[@class="t2"]/a/@title').extract()
            out['qc_job_loc'] = item.xpath('span[@class="t3"]/text()').extract()
            out['qc_job_pay'] = item.xpath('span[@class="t4"]/text()').extract()
            out['qc_job_date'] = item.xpath('span[@class="t5"]/text()').extract()
            job_link = item.xpath('p/span/a/@href').extract()
            job_page = requests.get(clean(str(job_link[0])), headers=self.headers)
            print('the job page is {}'.format(job_link[0]))
            biscuit = bs(job_page.content, 'html.parser')
            out['qc_job_desc'] = clean(biscuit.find("div", class_="tBorderTop_box").get_text())
            co_link = item.xpath('span[@class="t2"]/a/@href').extract()
            print('the co link is {}'.format(co_link[0]))
            try:
                co_page = requests.get(clean(str(co_link[0])), headers=self.headers)
                print("the co parsing result is {}".format(co_page.status_code))
                soup = bs(co_page.content, 'html.parser')
                try:
                    out['qc_co_type'] = clean(soup.find("div", class_="tHeader tHCop").div.find("p", class_="ltype").get_text().split('|')[0])
                    out['qc_co_ee_size'] = clean(soup.find("div", class_="tHeader tHCop").div.find("p", class_="ltype").get_text().split('|')[1])
                    out['qc_co_tags'] = clean(soup.find("div", class_="tHeader tHCop").div.find("p", class_="ltype").get_text().split('|')[2])

                    out['qc_co_address'] = clean(soup.find("div", class_="bmsg inbox").p.get_text())
                    out['qc_co_desc'] = clean(soup.find("div", class_="con_msg").find("div", class_="in").p.get_text())
                except:
                    print('special hiring page')
            except:
                print('request failure')
            yield out

        next_page = response.xpath('//div[@class="dw_page"]//div[@class="p_in"]/ul/li[@class="bk"][2]/a/@href').extract()[0]
        print("the next page is {}".format(next_page))
        if next_page is not None:
            self.cur_page += 1
            print('next page exists, number is {}'.format(self.cur_page))
            yield scrapy.Request(next_page, callback=self.parse_page)








