import scrapy
from scrapy.selector import Selector
import requests
import time
import requests
from kanzhun_search.items import KanzhunSearchItem

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
    x = x.replace('\\r', '').replace('\\t', '').replace('\\n', '').replace('"', '').replace(" ", "").replace("|","").replace('[','').replace(']','').replace("'",'').replace(',','').replace('\n','').replace('\t','').replace('\r','')
    return x

class KanzhunSearchSpider(scrapy.Spider):
    name = 'kanzhun_search'
    allowed_domain = 'http://www.kanzhun.com'
    page = 1

    def start_requests(self):

        for type in [116,119,5,4,65,64,62,54,53,57,56,60,55]:

            url = 'http://www.kanzhun.com/jobli_' +str(type) +'-t_0-e_0-d_0-s_0-j_0-k_0/p1/?q=%E6%B5%B7%E5%A4%96&ka=paging1'
            yield scrapy.Request(url, callback= self.parse_page)

    def parse_page(self,response):

        sel = Selector(response)
        titles = sel.xpath('//div[@class="sparrow"]/dl/dd')

        for title in titles:

            item = KanzhunSearchItem()
            item['positionName'] = clean(title.xpath('h3/a//text()').extract())
            item['salary'] = clean(title.xpath('p[@class="request grey_99"]/b[@class="salary"]/text()').extract())
            item['description'] = clean(title.xpath('p[@class="company_advantage"]/text()').extract())
            item['job_loc'] = clean(title.xpath('p[@class="request grey_99"]/span[@class="city"]/text()').extract())
            # print(title.xpath('p[@class="request grey_99"]/text()').extract())
            item['job_suffer'] = clean(title.xpath('p[@class="request grey_99"]/text()').extract()[2])
            item['job_edu'] = clean(title.xpath('p[@class="request grey_99"]/text()').extract()[3])
            item['job_type'] = clean(title.xpath('p[@class="request grey_99"]/text()').extract()[4])
            item['job_time'] = clean(title.xpath('p[@class="request grey_99"]/text()').extract()[5])



            item['companyFullName'] = clean(title.xpath('p[@class="jieshao"]/a/text()').extract())

            if title.xpath('p[@class="jieshao"]/a/@href').extract():

                co_url = 'http://www.kanzhun.com' + title.xpath('p[@class="jieshao"]/a/@href').extract()[0]
                co_page = requests.get(co_url, headers = headers, proxies=proxies)
                co_sel = Selector(co_page)

                try:
                    # print(co_sel.xpath('//div[@class="bw_explain"]/text()'))
                    item['industryField'] = clean(co_sel.xpath('//div[@class="bw_explain"]/span[1]/text()').extract())
                    item['co_loc'] = clean(co_sel.xpath('//div[@class="bw_explain"]/span[2]/text()').extract())
                    item['companySize'] = clean(co_sel.xpath('//div[@class="bw_explain"]/span[last()]/text()').extract())
                    item['co_des'] = clean(co_sel.xpath('//div[@class="bw_brief"]/text()').extract())

                except:
                    print('shit company')

                yield item

        next_page = sel.xpath('//a[@class="p_next"]/@href')

        if next_page:

            next_page = 'http://www.kanzhun.com' +next_page.extract()[0]
            self.page += 1
            print('go {} page'.format(self.page))
            yield scrapy.Request(next_page, callback= self.parse_page)

        else:
            print('No next pages, nigga!!\n')

