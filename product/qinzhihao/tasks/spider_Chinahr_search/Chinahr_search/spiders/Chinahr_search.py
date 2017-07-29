import json
import scrapy
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import time
from Chinahr_search.items import ChinahrSearchItem
from lxml import html
import urllib.parse, urllib.request
import http.cookiejar
import requests


# data=time.shrfttime("%Y %m %d", time.locatime(time.time()))

def clean(x):
    return x.replace('\\r', '').replace('\\t', '').replace('\\n', '').replace('"', '').replace(" ", "").replace("\"", "").replace("|","").replace('[','').replace(']','').replace("'",'').replace(',','')


class ChinahrSearchSpider(scrapy.Spider):

    name='Chinahr_search'
    allowed_domain='https://www.chinahr.com'
    cur_page = 1

    def start_requests(self):

        url = 'http://www.chinahr.com/sou/?orderField=relate&keyword=%s&city=36,400&page=1'
        yield scrapy.Request(url % self.searchword, callback= self.parse_page)

    def parse_page(self,response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        sel = Selector(response)
        titles = sel.xpath('//div[@class="jobList"]/ul')
        # totalcount = sel.xpath('//div[@class="totalResult cutWord"]/span')
        # totalpage = totalcount / 20 + 1

        for title in titles:
            # print(title)

            item = ChinahrSearchItem()
            item['positionName'] = str(title.xpath('li[1]/span[1]//text()').extract())\
                .replace('[','').replace(']','').replace("'",'').replace(',','').replace(' ','')
            item['job_add'] = str(title.xpath('li[2]/span[1]/text()').extract())\
                .split(']')[0].replace('\\t', '').replace('\\n', '').replace('\\r', '').replace("'",'').replace('[', '')
            item['job_limit'] = str(title.xpath('li[2]/span[1]/text()').extract())\
                .split(']')[1].replace('\\t', '').replace('\\n', '').replace('\\r', '')
            item['salary'] = title.xpath('li[2]/span[2]/text()').extract()

            # b = a.split(']')[1].split('/')
            # if len(b) == 2:
            #     item['job_time'] = b[0].replace('\\t','').replace('\\n','').replace('\\r','')
            #     item['job_edu'] = b[1].replace("'",'')
            # else:
            #     item['job_edu'] = str(b).replace('\\t','').replace('\\n','').replace('\\r','').replace("'",'')
            #
            item['co_inner_web'] = title.xpath('li[1]/span[3]/a/@href').extract()
            item['companySize'] = title.xpath('li[2]/span[3]/em[3]/text()').extract()
            co_url = str(title.xpath('li[1]/span[3]/a/@href').extract()).replace('[', '').replace(']', '').replace("'", '')
            job_url = title.xpath('li[1]/span[1]/a/@href').extract()[0]

            if job_url:
                job_page = requests.get(job_url)
                jobtree = Selector(job_page)
                item['description'] = str(jobtree.xpath('//div[@class="job_intro_info"]//text()').extract()).\
                    replace('\\r', '').replace('\\t', '').replace('\\n', '').replace('"', '').replace("\"", "").replace("|","").replace('[','').replace(']','').replace("'",'').replace(',','').replace('  ','')


            if co_url.startswith('http://www.chinahr.com/company'):

                print('company page',co_url)
                try:

                    company_page = requests.get(co_url)

                    tree = Selector(company_page)
                    # print(tree.xpath('//h1/text()'))
                    item['companyFullName'] = tree.xpath('//h1/text()').extract()
                    item['co_contact'] = clean(str(tree.xpath('//div[@class="address"]/p/i[@class="icon_hf people"]/parent::p/text()').extract()))
                        # \.replace('\t','').replace('\n','').replace('\r','').replace(" ",'').replace(' ','').replace('"','').replace('&nbsp;','')
                    item['co_mob'] = tree.xpath('//div[@class="address"]/p/i[@class="icon_hf mobile"]/parent::p/text()').extract()
                        # .replace('\t','').replace('\n','').replace('\r','').replace(" ",'').replace(' ','').replace('"','').replace('&nbsp;','')
                    item['co_tel'] = tree.xpath('//div[@class="address"]/p/i[@class="icon_hf tel"]/parent::p/text()').extract()
                        # .replace('\t','').replace('\n','').replace('\r','').replace(" ",'').replace(' ','').replace('"','').replace('&nbsp;','')
                    item['co_email'] = tree.xpath('//div[@class="address"]/p/i[@class="icon_hf email"]/parent::p/text()').extract()
                        # .replace('\t','').replace('\n','').replace('\r','').replace(" ",'').replace(' ','').replace('"','').replace('&nbsp;','')
                    item['co_link'] = tree.xpath('//div[@class="address"]/p/i[@class="icon_hf web"]/parent::p/text()').extract()
                        # .replace('\t','').replace('\n','').replace('\r','').replace(" ",'').replace(' ','').replace('"','').replace('&nbsp;','')
                    item['co_add'] = tree.xpath('//div[@class="address"]/p/i[@class="icon_hf add"]/parent::p/text()').extract()
                        # .replace('\t','').replace('\n','').replace('\r','').replace(" ",'').replace(' ','').replace('"','').replace('&nbsp;','')
                    item['industryField'] = str(tree.xpath('//div[@class="wrap-mc"]/em[2]/text()').extract())\
                        .replace('\\t','').replace('\\n','').replace('\\r','').replace("[",'').replace(']','').replace('"','').replace("'",'').replace(' ','')
                    item['financeStage'] = tree.xpath('//div[@class="wrap-mc"]/em[3]/text()').extract()
                    # item['description'] = clean(str(tree.xpath('//div[@class="article"]/text()').extract()))

                    # yield item

                except:
                    print('shit,nigga!')

            else:
                print('not Chinahr webpages')
                item['co_name'] = 'unavailabe on Chinahr itself'
                item['co_contact'] = 'unavailabe on Chinahr itself'
                item['co_mob'] = 'unavailabe on Chinahr itself'
                item['co_tel'] = 'unavailabe on Chinahr itself'
                item['co_email'] = 'unavailabe on Chinahr itself'
                item['co_link'] = 'unavailabe on Chinahr itself'
                item['co_add'] = 'unavailabe on Chinahr itself'
                # item['co_desc'] = str(tree.xpath('//div[@class="company-content"]/p')).replace("<p>","").replace("</p>","").replace("<br>","").replace("&nbsp","").replace('|',"").replace("\n","").replace('\t',"").replace('\r',"").replace(' ',"")
                # item['co_desc'] = 'unavailabe on zhilian itself'
                print('shit happens!!!!In inside-process!!\n')

                # yield item
            yield item



        # if self.curpage <= self.totalPageCount:
        #   self.curpage += 1
        #   start_urls = "https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false"
        #   yield scrapy.FormRequest(start_urls, formdata={'pn': str(self.curpage), 'first': 'true', 'kd': self.key}, cookies=self.cookies, callback=self.parse_page)

        next_page = sel.xpath('//div[@class="pageList"]/*[last()]/@href')
        if next_page:
             # next_page = response.urljoin(next_page)
             # yield SplashRequest(next_page, self.parse_title, endpoint='render.html', args={'wait': 0.5})
             self.cur_page += 1
             print('next page exists, number is {}'.format(self.cur_page))
             yield scrapy.Request('http://www.chinahr.com/sou/?orderField=relate&keyword=%E6%B5%B7%E5%A4%96&city=36,400&page='+str(self.cur_page), self.parse_page)
        else:
             print('No next pages, nigga!!\n')