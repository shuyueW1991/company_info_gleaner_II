# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import re
import time
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http.response.html import HtmlResponse
import requests
import urllib.request
from bs4 import BeautifulSoup as bs
from scrapy.selector import Selector
from spider_official_websites.items import SpiderOfficialWebsitesItem
from difflib import SequenceMatcher as sqm
import tldextract as tld
import traceback

date=time.strftime("%Y%m%d",time.localtime(time.time()))
# urls_to_crawl = "/mnt/qinzhihao/Try/spider_content_crawl/company_list.csv"
urls_to_crawl ='company_list.csv'
deny_list = ["www.adobe.com", "www.linkedin.com","www.weibo.com","www.zhihu.com","open.weibo.com"]

## Function to Clean URL for Pattern Matching
def extract_text_by_bs(doc_text):

    title, text = '', ''
    soup = bs(doc_text, 'lxml')
    try:
        for script in soup(["script", "style"]):
            script.extract()
    except Exception as error:
        print(error)
        pass
    else:
        try:
         # get text
            title = soup.title.string
        except Exception as error:
            print(error)
            pass
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ''.join(chunk for chunk in chunks if chunk)
    return title+text

def clean(x):
    x = str(x)
    x = x.replace('\\r', '').replace('\\t', '').replace('\\n', '').replace('\n','').replace('\t','').replace('\r','').replace("  ", "").replace("|","")
    return x

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
    name = “urlcrawler"
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
        self.searchword = ''
        self.co_page = ''




    ## Read URLs from External File and Generate Request
    def start_requests(self):

        for line in open(urls_to_crawl, 'r', encoding='utf8'):

            self.searchword = line.strip("\n").strip("\t").replace('http://','')

            try:
                # yield scrapy.Request('http://'+str(url), callback=self.parse_page)
                print('company name is {}'.format(self.searchword))
                yield scrapy.Request('https://www.baidu.com/s?wd=%s@v' % self.searchword, meta = {'searchword':self.searchword}, callback = self.parse_v)

            except:
                traceback.print_exc()
                print('shit searchword {}'.format(self.searchword))


    def parse_v(self, response):
        out = SpiderOfficialWebsitesItem()
        print('We are going to find company homepage')
        sel = Selector(response)
        self.co_page = sel.xpath('//div[@class="inner-section"]//tr[2]/td/a[1]/@href').extract()
        # self.co_page = sel.xpath('//table[@class="content-table"]/*/tr/td/a[1]/@href').extract()

        if len(self.co_page) > 0:
            print('shit')
            print('@v is good, nigga, url: '+ str(self.co_page[0]))
            out['co_homepage'] = self.co_page[0].replace('http://','')
            out['co_name'] = sel.xpath('//div[@class="c-row section header-section"]/h2/text()').extract()
            out['match_res'] = ['@v']
            yield out

        else:
            # title_left = sel.xpath('//div[@id="container"]/div[@id="content_left"]')
            # title_left_nonbd = title_left.xpath('div[@class="result c-container"]/h3/a/@href').extract()
            yield scrapy.Request(response.url.replace('@v',''), meta = {'searchword':response.meta['searchword']}, callback = self.parse_search)

    def parse_search(self,response):
        out = SpiderOfficialWebsitesItem()
        print('no @v, nigga')
        sel = Selector(response)
        title_left_nonbd = sel.xpath('//div[@class="result c-container "]')

        for title in title_left_nonbd:
            out['co_name'] = response.meta['searchword']
            out['co_homepage'] = 'shit homepage'
            out['match_res'] = 'match shit'
            match_res = str(title.xpath('h3/a//text()').extract()).replace('[', '').replace(']', '').replace("'","").replace(',', '')
            match_res_ = match_res.count('_') + match_res.count('-')
            match_res_space = match_res.count(' ') + match_res.count('/\\xa0') + match_res.count('/\xa0')
            url = title.xpath('//div[@class="f13"]/a[1]/text()').extract()[0]
            # url = str(title.xpath('//div[@class="f13"]/a[1]//text()').extract()).replace('[', '').replace(']', '').replace("'", "").replace(',', '').replace(' ', '')
            print(url)
            # url = str(title.xpath('div[1]/div[@class="c-span18 c-span-last"]/div[@class="f13"]/a[1]//text()').extract())\
            #     .replace('[','').replace(']','').replace("'","").replace(',','').replace(' ','')
            # print(type(url))

            if url=='www.':
                url = str(title.xpath('div[1]/div[@class="c-span18 c-span-last"]/div[@class="f13"]/a[1]//text()').extract())\
                    .replace('[','').replace(']','').replace("'","").replace(',','').replace(' ','')

            if title.xpath('//div[@class="f13"]/a[1]/b/text()').extract():
                url = str(title.xpath('div[1]/div[@class="c-span18 c-span-last"]/div[@class="f13"]/a[1]//text()').extract())\
                    .replace('[','').replace(']','').replace("'","").replace(',','').replace(' ','')


            if url.count('/') < 2 and '...' in url:
                timeout_try = 15

                while timeout_try > 0:
                    try:
                        url = title.xpath('h3/a/@href').extract()[0]
                        url = urllib.request.urlopen(url, None, 1).geturl()
                        break
                    except TimeoutError:
                        time.sleep(0.1)
                        timeout_try = timeout_try - 1
                        continue

            url_subdomain = tld.extract(url).subdomain
            url = url.strip('/\xa0').strip('/\\xa0').replace('http://','')
            # print(title_parse,url,url_subdomain)

            # print(match_res_,match_res_space,len(url_subdomain),url)
            if match_res_ < 1 and match_res_space < 5 and len(url_subdomain) < 5 and url.count('/') < 2 or 'index' in url or url.count('/') < 1:
                print('search result match good')
                out['co_homepage'] = url
                out['match_res'] = match_res
                break

            else:
                pass

        yield out

                # get final url in baidu redirection process
                # url = urllib.request.urlopen(url, None, 1).geturl()




    ## Parsing Extracted Information
    # def parse_page(self, response):
    #
    #     domain = tld.extract(response.url).domain
    #     inner_link = []
    #
    #     for link in self.le.extract_links(response):
    #         link_domain = tld.extract(link.url).domain
    #         # print(link_domain)
    #         # print(domain)
    #         if link_domain == domain:
    #             inner_link.append(link.url)
    #
    #         else:
    #             pass
    #
    #     self.log('page is {}'.format(response.url))
    #
    #     if not isinstance(response, HtmlResponse):
    #         print('link {} is not html response'.format(response.url))
    #         return None
    #
    #     else:
    #         out = SpiderOfficialWebsitesItem()
    #         # soup = bs(response.body, 'html.parser')
    #         out['url'] = response.url
    #         out['host_url'] = domain
    #         # email = re.findall(self.email_pattern,response.text )
    #         # mobile = re.findall(self.mobile_pattern, response.text)
    #         # out['email'] = list(set(email)) if email else None
    #         # out['mobile'] = list(set(mobile)) if mobile else Non
    #         # print(response.body)
    #         out['content'] = extract_text_by_bs(response.body)
    #
    #
    #         yield out
    #
    #         print('the url count dict is {}'.format(self.host_dict))
    #
    #         # if (len(self.le.extract_links(response)) > self.not_follow_count) or (self.host_dict[out['host_url']] > self.not_follow_count): ## filter out hub pages
    #
    #
    #         for link in inner_link:
    #             check = re.search(url_clean(out['host_url']), str(link).split('/')[2]) ## limit crawling to within the website
    #             sim_w_res = sqm(None, str(link), out['url']).ratio()
    #             sim_w_pre = sqm(None, str(link), self.pre_link).ratio()
    #             # sim_w_host = sqm(None, str(link.url).split('/')[2], self.pre_host)
    #             print('pre link is {}'.format(self.pre_link))
    #             print('cleaned host url is {}'.format(url_clean(out['host_url'])))
    #             print('link to follow is {}'.format(str(link)))
    #
    #             if check and len(link)<self.url_max_len and (sim_w_res < self.similarity) and (sim_w_pre < self.similarity) and (sim_w_res > 0.5):
    #
    #                 try:
    #                     self.host_dict[out['host_url']] += 1
    #                 except:
    #                     self.host_dict[out['host_url']] = 1
    #
    #                 if self.host_dict[out['host_url']] > self.not_follow_count:
    #                     print('too many links to follow')
    #
    #                 else:
    #                     try:
    #                         r = scrapy.Request(url=link, callback=self.parse_page)
    #                         # r.meta.update(link_text=link.text)
    #                         self.pre_link = str(link)
    #                         yield r
    #
    #                     except:
    #                         pass
    #
    #                     # timeout_retry = 15
    #                     # while timeout_retry > 0:
    #                     #
    #                     #     try:
    #                     #         r = scrapy.Request(url=link, callback=self.parse_page)
    #                     #         # r.meta.update(link_text=link.text)
    #                     #         self.pre_link = str(link)
    #                     #         yield r
    #                     #     except TimeoutError:
    #                     #         timeout_retry =timeout_retry -1
    #                     #         continue
    #                     #     else:
    #                     #         pass
    #
    #
    #             else:
    #                 print('outside link {}, not followed'.format(link))
    #                 continue
