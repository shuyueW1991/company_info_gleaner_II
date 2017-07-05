import json
# import scrapy
# from scrapy.selector import Selector
# import time
# from Chinahr_search.items import ChinahrSearchItem
from lxml import html
import urllib.parse, urllib.request
import http.cookiejar
import requests
from bs4 import BeautifulSoup as bs


# data=time.shrfttime("%Y %m %d", time.locatime(time.time()))


# class ChinahrSearchSpider(scrapy.Spider):
#     # name='Chinahr_search'
#     # allowed_domain='https://www.chinahr.com'
#     # curpage = 1
#
# r = requests.get('http://www.chinahr.com/sou/?orderField=relate&keyword=%E6%B5%B7%E5%A4%96&city=36,400&industrys=1101&page=1')
# print(type(r))
# print(r.status_code)
# soup = bs(r.content, 'lxml')
# # print(soup)
# job_name = soup.find_all('a')
# for job in job_name:
#     print(job.get_text())



    # def parse_page(self,response):
    #     sel = Selector(response)
    #     titles = sel.xpath('//div[@class="jobList"]')
    #     # totalcount = sel.xpath('//div[@class="totalResult cutWord"]/span')
    #     # totalpage = totalcount / 20 + 1
    #
    #     for title in titles:
    #
    #         item = ChinahrSearchItem()
    #         item['job_name'] = title.xpath('//li[1]/span[1]')
    #         item['job_pay'] = title.xpath('//li[2]/span[2]')
    #         item['job_add'] = title.xpath('//li[2]/span[1]')
    #         item['job_time'] = title.xpath('//li[2]/span[1]')
    #         item['job_edu'] = title.xpath('//li[2]/span[1]')
    #         item['co_inner_web'] = title.xpath('//li[1]/span[3]/a/@href')