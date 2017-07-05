import scrapy, json
from KZjob.items import KzjobItem
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
# from scrapy_splash import SplashRequest
import random
import time
from scrapy.http import HtmlResponse
import requests
import datetime

date=time.strftime("%Y%m%d",time.localtime(time.time()))

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

class KZjob(scrapy.Spider):
    name = "kanzhunjob"
    allowed_domains = ["https://www.kanzhun.com"]

    def start_requests(self):
        for i in range(2000,500000):
            # start_urls=['http://jobs.51job.com/all/co'+str(i)+'.html']
            start_urls=["http://www.kanzhun.com/job/g"+str(i)+".html?ka=com-floater-job"]
            for url in start_urls:
                yield scrapy.Request(url, callback=self.parse_page)
                # yield SplashRequest(url, self.parse_page,args={'wait':0.5})

    def parse_page(self,response):

        # print(response.body)
        sel = Selector(response)
        a = str(sel.xpath('//h1/text()').extract()).replace('[', '').replace("'", '').replace(']','')
        b = sel.xpath('//div[@class="co_pk"]/a/@data-id').extract()[0]
        # job_Num = str(sel.xpath('//span[@class="f_right"]/em/text()').extract()).replace('[', '').replace("'", '').replace(']','').replace('条','')
        job_Num = str(sel.xpath('//span[@class="f_right"]/em/text()').extract()).replace('[','').replace(']','').replace("'",'').replace('条', '')
        # print(job_Num)
        # job_num = int(sel.xpath('//span[@class="f_right"]/em/text()').extract()[0].replace('条', ''))

        if job_Num:

            job_num = int(job_Num)
            page_num = int(job_num/ 10) +1
            i = 0

            while i < page_num:

                i += 1
                # try:

                time.sleep(1)
                # job_page = requests.get(
                #     'http://www.kanzhun.com/job/g'+ b +'/page.json?companyName='+ a +'&pageNum='+str(i)+'&cityName=&jobTitle=', proxies = proxies, headers = headers)
                job_page = requests.get(
                    'http://www.kanzhun.com/job/g' + b + '/page.json?companyName=' + a + '&pageNum=' + str(i) + '&cityName=&jobTitle=',  headers=headers, timeout=1)

                # print(job_page.content)
                Jobs = Selector(job_page)
                jobs = Jobs.xpath('//div[@class="position_info"]')
                # print(jobs)
                lab = 0
                for job in jobs:
                    # print(job)
                    lab += 1
                    item = KzjobItem()
                    item['co_name'] = a
                    item['co_web_id'] = b
                    item['job_name'] = job.xpath('dl[1]/dd/p[1]/a/text()').extract()[0].replace('\n','')
                    item['job_pay'] = job.xpath('dl[1]/dd/p[2]/span[@class="salary"]/text()').extract()[0].replace('￥','')
                    item['job_add'] = str(job.xpath('dl[1]/dd/p[2]/span[2]/text()').extract()).replace('[','').replace(']','').replace("'",'')
                    item['job_suffer'] = str(job.xpath('dl[1]/dd/p[2]/span[3]/text()').extract()).replace('[','').replace(']','').replace("'",'')
                    item['job_edu'] = str(job.xpath('dl[1]/dd/p[2]/span[4]/text()').extract()).replace('[','').replace(']','').replace("'",'')
                    item['job_type'] = str(job.xpath('dl[1]/dd/p[2]/span[5]/text()').extract()).replace('[','').replace(']','').replace("'",'')
                    item['job_desc'] = str(job.xpath('following-sibling::*[1]/a/text()').extract()).replace('\\n',"").replace('\t','').replace('\r','').replace('\n','').replace('\n','').replace('[','').replace(']','').replace("'",'')
                    item['update_datetime'] = repr(date).replace("'",'')
                    yield item

                # except:
                #     print('shit,nigga!')

        else:
            pass