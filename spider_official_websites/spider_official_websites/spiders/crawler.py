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
from difflib import SequenceMatcher as sqm
import tldextract as tld

date=time.strftime("%Y%m%d",time.localtime(time.time()))
urls_to_crawl = "/mnt/qinzhihao/tasks/spider_official_websites/url_list_short.txt"
deny_list = ["www.adobe.com", "www.linkedin.com","www.weibo.com","www.zhihu.com","open.weibo.com"]

## Function to Clean URL for Pattern Matching


def url_clean(url):
    # to_replace=["/","//",":","http","https","www.",".com",".co",".net",".cn",".cc",".mobi",".link",".me",".tech",".gov.cn",".asia",".ltd",".tv"]
    to_replace = ["http://", "https://", "www."]
    for i in to_replace:
        url = url.replace(i,"")
    return url

def content_clean(content):
    content = str(content).replace('|',"")
    return content


class CrawlerSpider(CrawlSpider):
    name = "crawler"
    date = date

    ## Defining Link Extraction Method Here
    def __init__(self, *args, **kwargs):

        super(CrawlerSpider, self).__init__(*args, **kwargs)
        self.le = LinkExtractor(deny_domains=deny_list) ## exclude crawl from wellknown big sites
        self.not_follow_count = 100 ## exclude webpages with follow link > 100
        self.similarity = 0.9 ## exclude extracted web urls that are too similar to current url
        self.email_pattern = re.compile(r'\b[\w.-]+?@[\w.-]+?\.\w+\.?\w+')
        self.mobile_pattern = re.compile(r'1\d{2}\W?\d{4}\W?\d{4}')
        self.pre_link = "init"
        self.pre_host = "init"
        self.host_dict = {}
        self.url_max_len = 100


    ## Read URLs from External File and Generate Request
    def start_requests(self):

        for line in open(urls_to_crawl, 'r', encoding='utf8'):
            url = line.strip("\n").strip("\t").replace('http://','')
            print('url is {}'.format(url))
            yield scrapy.Request('http://'+str(url), callback=self.parse_page)

    ## Parsing Extracted Information
    def parse_page(self, response):

        domain = tld.extract(response.url).domain
        inner_link = []

        for link in self.le.extract_links(response):
            print(link.url)
            print(domain)
            if domain in link.url:
                inner_link.append(link.url)

            else:
                pass

        self.log('page is {}'.format(response.url))

        if not isinstance(response, HtmlResponse):
            print('link {} is not html response'.format(response.url))
            return None

        else:
            out = SpiderOfficialWebsitesItem()
            out['url'] = response.url
            out['host_url'] = domain
            email = re.findall(self.email_pattern,response.text )
            mobile = re.findall(self.mobile_pattern, response.text)
            out['email'] = list(set(email)) if email else None
            out['mobile'] = list(set(mobile)) if mobile else None

            yield out

            print('the url count dict is {}'.format(self.host_dict))

            # if (len(self.le.extract_links(response)) > self.not_follow_count) or (self.host_dict[out['host_url']] > self.not_follow_count): ## filter out hub pages


            for link in inner_link:
                check = re.search(url_clean(out['host_url']), str(link).split('/')[2]) ## limit crawling to within the website
                sim_w_res = sqm(None, str(link), out['url']).ratio()
                sim_w_pre = sqm(None, str(link), self.pre_link).ratio()
                # sim_w_host = sqm(None, str(link.url).split('/')[2], self.pre_host)
                print('pre link is {}'.format(self.pre_link))
                print('cleaned host url is {}'.format(url_clean(out['host_url'])))
                print('link to follow is {}'.format(str(link)))

                if check and len(link)<self.url_max_len and (sim_w_res < self.similarity) and (sim_w_pre < self.similarity) and (sim_w_res > 0.5):

                    try:
                        self.host_dict[out['host_url']] += 1
                    except:
                        self.host_dict[out['host_url']] = 1

                    if self.host_dict[out['host_url']] > self.not_follow_count:
                        print('too many links to follow')

                    else:
                        r = scrapy.Request(url=link, callback=self.parse_page)
                        # r.meta.update(link_text=link.text)
                        self.pre_link = str(link)
                        yield r

                else:
                    print('outside link {}, not followed'.format(link))
                    continue