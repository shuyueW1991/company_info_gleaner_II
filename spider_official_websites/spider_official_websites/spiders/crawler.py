# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import re
import time
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http.response.html import HtmlResponse
import requests
from bs4 import BeautifulSoup as bs
from scrapy.selector import Selector as sle
from spider_official_websites.items import SpiderOfficialWebsitesItem

date=time.strftime("%Y%m%d",time.localtime(time.time()))
urls_to_crawl = "/Users/Han/Desktop/url_list.txt"

class CrawlerSpider(CrawlSpider):
    name = "crawler"
    date = date

    ## Defining Link Extraction Method Here
    def __init__(self, *args, **kwargs):
        super(CrawlerSpider, self).__init__(*args, **kwargs)
        self.le = LinkExtractor()


    ## Read URLs from External File and Generate Request
    def start_requests(self):
        for line in open(urls_to_crawl, 'r', encoding='utf8'):
            url = line.strip("\n").strip("\t")
            print('url is {}'.format(url))
            yield scrapy.Request(str(url), callback=self.parse_page)

    ##
    def parse_page(self, response):
        self.log('page is {}'.format(response.url))
        if not isinstance(response, HtmlResponse):
            print('not html response')
            return

        out = SpiderOfficialWebsitesItem()
        out['url'] = response.url
        out['host_url'] = response.url.split('/')[2]

        for link in self.le.extract_links(response):
            r = scrapy.Request(url=link.url, callback=self.parse_page)
            r.meta.update(link_text=link.text)
            yield r

        yield out


