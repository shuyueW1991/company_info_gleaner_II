# -*- coding: utf-8 -*-

import scrapy
import json
import time
from lxml import html
import requests
from lagou_search.items import LagouSearchItem
from lagou_search.items import LagouSearchLoader

date=time.strftime("%Y%m%d",time.localtime(time.time()))

class LagouSearchSpider(scrapy.Spider):
    name = "lagou_search"
    # key = "海外"
    curpage = 1

    cookies = {'user_trace_token':'20170223163946-7ff6ed5a7f1a4618b96eef638a4796f4',
               'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6':'1492420764',
               'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6':'1491829470,1491983089,1492256840,1492420764',
               '_ga':'GA1.2.61490707.1491186433',
               'LGRID':'20170417171923-f2348746-234e-11e7-898d-525400f775ce	',
               'LGSID':'20170417171923-f2348578-234e-11e7-898d-525400f775ce',
               'LGUID':'20170223163947-a2018e8a-f9a3-11e6-88f1-525400f775ce',
               'PRE_HOST':'www.google.com',
               'PRE_LAND':'https%3A%2F%2Fwww.lagou.com%2F',
               'TG-TRACK-CODE':'search_code',
               'JSESSIONID':'4138BB06BC7720EB04C28945A049D618',
               'SEARCH_ID':'82ab5970c3e3405aad34161d679e93a2'}

    def start_requests(self):
        start_urls = "https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false"
        return [scrapy.FormRequest(start_urls, formdata={'pn':'1','first':'true','kd': '%s' % self.searchword} , cookies=self.cookies, callback=self.parse_page)]

    def parse_page(self, response):
        print("Scraping Page Number {}".format(self.curpage))
        out = LagouSearchItem()
        # print(response.body)
        data = str(response.body,'utf-8')
        # print(data)
        jdict = json.loads(data)
        jcontent = jdict["content"]
        jresult = jcontent["positionResult"]
        jposition = jresult["result"]
        self.totalPageCount = jresult['totalCount'] / 15 + 1

        for item in jposition:
            out["companyID"] = item["companyId"]
            out["companyFullName"] = item["companyFullName"]
            out["companyShortName"] = item["companyShortName"]
            out["formatCreatedTime"] = item["formatCreateTime"]
            out["positionID"] = item["positionId"]
            out["positionName"] = item["positionName"]
            out["companySize"] = item["companySize"]
            out["financeStage"] = item["financeStage"]
            out["industryField"] = item["industryField"]
            out["jobNature"] = item["jobNature"]
            out["positionLables"] = item["positionLables"]
            out["city"] = item["city"]
            out["education"] = item["education"]
            out["salary"] = item["salary"]
            out["firstType"] = item["firstType"]
            out["secondType"] = item["secondType"]
            out["workYear"] = item["workYear"]
            out["scrapeTime"] = date
            # pos_request = scrapy.Request("https://www.lagou.com/jobs/{}.html".format(str(item['positionId'])), callback=self.parse_pos, meta={'item':out})
            # print("the company is {}".format(str(out['companyID'])))
            # pos_request.meta['out'] = out
            page = requests.get("https://www.lagou.com/jobs/{}.html".format(str(item['positionId']).strip(" ")))
            print("the pos parsing result is {}".format(page.status_code))
            tree = html.fromstring(page.content)
            # print("the content is {}".format(tree))
            out["description"] = str(tree.xpath('//dd[@class="job_bt"]/div//text()')).replace("'", '').replace('\r', '').replace('\t', '').replace('\n', '').replace("\n", '').replace('"', '').replace(' ', '').replace("xa0", '')
            yield out
            # yield pos_request

        # if self.curpage <= 2:
        if self.curpage <= self.totalPageCount:
            self.curpage += 1
            start_urls = "https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false"
            yield scrapy.FormRequest(start_urls, formdata={'pn': str(self.curpage), 'first': 'true', 'kd': self.key}, cookies=self.cookies, callback=self.parse_page)
        else:
            print("shit's finished nigga")

