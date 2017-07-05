import scrapy
from scrapy.selector import Selector
import requests
import time
import requests
from boss_search.items import BossSearchItem
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
import ssl

class MyAdapter(HTTPAdapter):
    def init_poolmanager(self,connections,maxsize,block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)
s = requests.Session()
s.mount('https://', MyAdapter())

headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)"}

proxyHost = "proxy.abuyun.com"
proxyPort = "9020"

proxyUser = "H020G39R1142524D"
proxyPass = "E440F4C798A80714"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}

proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}

def clean(x):
    x = str(x)
    x = x.replace('\\r', '').replace('\\t', '').replace('\\n', '').replace('"', '').replace("  ", "").replace("|","").replace('[','').replace(']','').replace("'",'').replace(',','').replace('\n','').replace('\t','').replace('\r','')
    return x

class BossSearchSpider(scrapy.Spider):
    name = 'boss_search'
    allowed_domain = 'https://www.zhipin.com'
    page = 1

    def start_requests(self):

        url ='https://www.zhipin.com/c100010000/h_100010000/?query=海外page=1&ka=page-1'
        yield scrapy.Request(url, callback= self.parse_page)

    def parse_page(self,response):

        sel = Selector(response)
        titles = sel.xpath('//div[@class="job-list"]/ul/li')

        for title in titles:

            item = BossSearchItem()
            item['positionName'] = title.xpath('a/div[1]/div[1]/h3/text()').extract()
            item['salary'] = title.xpath('a/div[1]/div[1]/h3/span/text()').extract()
            # item['job_loc'] = title.xpath('a/div[1]/div[1]/p/text()').extract()[0]
            item['job_suffer'] = title.xpath('a/div[1]/div[1]/p/text()').extract()[1]
            item['job_edu'] = title.xpath('a/div[1]/div[1]/p/text()').extract()[2]
            item['job_tag'] = clean(title.xpath('a/div[2]//span/text()').extract())
            item['job_time'] = title.xpath('a/div[3]/span/text()|a/div[2]/span[@class="time"]/text()').extract()

            item['companyFullName'] = title.xpath('a/div[1]/div[2]/div/h3/text()').extract()
            item['companySize'] = title.xpath('a/div[1]/div[2]/div/p/text()').extract()[-1]
            item['industryField'] = title.xpath('a/div[1]/div[2]/div/p/text()').extract()[0]

            try:
                item['financeStage'] = title.xpath('a/div[1]/div[2]/div/p/text()').extract()[1]
            except:
                item['financeStage'] = 'NaN'

            # job_url = 'https://www.zhipin.com' + title.xpath('a/@href').extract()[0]
            job_url = title.xpath('a/@href').extract()[0]

            if job_url.startswith('/job_detail/'):

                try:
                    job_page = s.get('https://www.zhipin.com' + job_url, headers = headers, proxies=proxies)
                    # job_page = requests.get('https://www.zhipin.com' + job_url, headers = headers, proxies=proxies)
                    job_sel = Selector(job_page)
                    item['description'] = clean(job_sel.xpath('//div[@class="text"]//text()').extract())
                    item['job_loc'] = job_sel.xpath('//div[@class="location-address"]/text()').extract()

                    try:
                        co_inner_link = job_sel.xpath('//div[@class="company-logo"]/a/@href').extract()[0]
                        print(co_inner_link)
                        co_inner_link = str(co_inner_link).replace('[','').replace('[','').replace("'",'')
                        co_page = s.get('https://www.zhipin.com' + co_inner_link, headers = headers, proxies=proxies)
                        # co_page = requests.get('https://www.zhipin.com' + co_inner_link, headers = headers, proxies=proxies)
                        co_sel = Selector(co_page)
                        item['co_link'] = co_sel.xpath('//div[@class="inner"]/div[1]/div[@class="info-primary"]/p[2]/text()').extract()

                    except:
                        print('shit company page')

                except:
                    print('shit job page')
            else:
                print('shit job page')

            yield item

        next_page = sel.xpath('//div[@class="page"]/a[@class="next"]/@href')

        if next_page:

            next_page = 'https://www.zhipin.com' + next_page.extract()[0]
            self.page += 1
            print('go {} page'.format(self.page))
            yield scrapy.Request(next_page, callback= self.parse_page)

        else:
             print('No next pages, nigga!!\n')



