# -*- coding: utf-8 -*-
import scrapy
import sys
sys.path.append("..")
from kr.items import KrItem
from scrapy_splash import SplashRequest
from scrapy.selector import Selector

# from selenium import webdriver
import time
import random


class KrSpider(scrapy.Spider):
    name = "kr_bianli"
    allowed_domains = ["36kr.com"]


    def __init__(self):
        self.begin = 5036000
        self.end = 5066000
#        self.file = open('krbianli_'+str(self.begin)+'_'+str(self.end),'a')
#        self.null_file = open('krbianli_null_'+str(self.begin)+'_'+str(self.end),'a')
        #self.file.write('title'+'|'+'time'+'|'+'guilei'+'|'+'abst'+'|'+'contents'+'|'+'tags'+'\n')

    def __del__(self):
        self.file.close()


    def start_requests(self):
        for i in range(5063069, self.begin, -1):
            if i % 500 == 0:
                time.sleep(10)
            else:
                start_urls = ["http://36kr.com/p/" + str(i) + ".html"]
                for url in start_urls:
                    yield SplashRequest(url, self.parse_title, endpoint='render.html', args={'wait': 0.5})


    def parse_title(self, response):
        sel = Selector(response)
        titles = sel.xpath('//div[@class="mobile_article"]')

        if len(titles) > 0 :
            for title in titles:
                item = KrItem()
                item['url'] = str(response.url)
                item['title'] =title.xpath('h1/text()').extract()
                item['time'] = title.xpath('div[@class="content-font"]/div[@class="am-cf author-panel"]/div[@class="author am-fl"]/span[last()-1]/abbr/text()').extract()
                item['guilei'] = title.xpath('div[@class="content-font"]/div[@class="am-cf author-panel"]/div[@class="author am-fl"]/span[last()]/abbr/text()').extract()
                item['abst'] = title.xpath('div[@class="content-font"]/section[@class="summary"]/text()').extract()
                #item['contents'] = title.xpath('div[@class="content-font"]/div[2]/section[1]/p/text()').extract()
                item['contents'] = title.xpath('div[@class="content-font"]/div/section[@class="textblock"]/p/text()').extract()
                item['tags'] = title.xpath('div[@class="content-font"]/section[@class="single-post-tags"]/a/text()').extract()
                # item['comments'] = title.xpath('div[@class="info"]/div[@class="comments-list"]/span[@class="comments"]/text()').extract()

                if len(item['title'])>0:
  #                  self.file.write(str(response.url)+'|'+item['title'][0])

  #                  if len(item['time'])>0:
  #                      self.file.write('|'+item['time'][0])

   #                 if len(item['guilei']) > 0 :
   #                     guilei = ";".join(item['guilei'])
   #                     self.file.write('|'+ guilei)

   #                 if len(item['abst']) > 0:
   #                     abst = ";".join(item['abst'])
   #                     self.file.write('|' + abst)

   #                 if len(item['contents'])>0:
   #                     content_str = ";".join(item['contents'])
   #                     self.file.write('|'+content_str)

   #                 if len(item['tags'])>0:
   #                     tags = ";".join(item['tags'])
   #                     self.file.write('|'+item['tags'][0])
   #                 self.file.write('\n')

                    #lapse = random.randint(1,4)
                    #time.sleep(lapse)
 #                   self.file.flush()
 #                   time.sleep(1)
                    time.sleep(3)
                    yield item
 #       else:
 #           self.null_file.write(response.url)
 #           self.null_file.write('\n')
            #lapse = random.randint(1,4)
            #time.sleep(lapse)
 #           self.file.flush()
 #           print(str(response.url) + ", 数据为空!")
