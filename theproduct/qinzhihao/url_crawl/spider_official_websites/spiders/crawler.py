# -*- coding: utf-8 -*-
import scrapy
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
import glob,datetime,codecs,os,shutil,numpy
import pandas as pd
# from openpyxl.cell import ILLEGAL_CHARACTERS_RE

date=time.strftime("%Y%m%d",time.localtime(time.time()))
now = datetime.datetime.now().strftime("%Y%m%d")

def data_auto_merge():
    now = datetime.datetime.now().strftime("%Y%m%d")
    # past = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
    list = glob.glob('*.csv')
    sel = pd.DataFrame()

    for file in list:

        if os.stat(file).st_size > 0:
            opener = codecs.open(file, "r",encoding='utf-8', errors='ignore')
            buffer = pd.read_csv(opener,sep="|")
            # print(buffer['co_link'])
            if 'financeStage' in buffer.columns:
                if 'co_link' in buffer.columns:
                    buffer = buffer[['companyFullName', 'companySize', 'industryField', 'financeStage', 'positionName', 'salary','description','co_link']]
                else:
                    buffer = buffer[['companyFullName', 'companySize', 'industryField', 'financeStage', 'positionName', 'salary','description']]
            else:
                buffer = buffer[['companyFullName', 'companySize', 'industryField', 'positionName', 'salary', 'description']]

            sel = sel.append(buffer)

        else:
            pass

        shutil.move('/mnt/qinzhihao/url_crawl/' + file, '/mnt/qinzhihao/url_crawl/old/')

    sel = sel[['companyFullName', 'companySize', 'industryField', 'financeStage', 'positionName', 'salary','description']]
    sel.to_csv('company_info_for_selection_' + now + '.csv', sep='|', index=False)

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


class CrawlerSpider(CrawlSpider):

    name = "urlcrawler"
    date = date

    ## Defining Link Extraction Method Here
    def __init__(self, *args, **kwargs):

        super(CrawlerSpider, self).__init__(*args, **kwargs)
        # self.le = LinkExtractor(deny_domains=deny_list) ## exclude crawl from wellknown big sites
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
        data_auto_merge()
        # urls_to_crawl = 'company_info_for_selection_' + now + '.csv'
        for line in open('company_info_for_selection_' + now + '.csv', 'r', encoding='utf8'):

            self.searchword = line.split('|')[0].strip("\n").strip("\t").replace('http://','')

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