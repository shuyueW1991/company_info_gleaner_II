# -*- coding: utf-8 -*-
import scrapy
import time
from zhilian_history.items import ZhilianItem
from zhilian_history.items import ZhilianLoader

date=time.strftime("%Y%m%d",time.localtime(time.time()))

class ZhilianSpider(scrapy.Spider):
    name = "zhilian"

    def start_requests(self):
        init_list = "https://company.zhaopin.com/CC000000000"
        # for i in range(0,99999999):
        # for i in range(0, 20000):
        for i in range(199880000,199890000):
        #     print("current page is {}".format(i))
            loc = min(len(str(i))+1,9)
            start_url = init_list[:-loc] + str(i)+".html"
            yield scrapy.Request(start_url, callback=self.parse_co)


    def parse_co(self, response, date=date):
        load = ZhilianLoader(ZhilianItem(), response)

        load.add_xpath('zl_co_id','//input[@id="companyNumber"]/@value')
        load.add_xpath('zl_co_name','//div[@class="mainLeft"]/div/h1/text()')

        # load.add_xpath('zl_co_tags','//table[@class="comTinyDes"]/tbody/tr[4]/td[2]/span/text()')
        load.add_xpath('zl_co_tags', '//div[@class="mainLeft"]/div/table//tr[1]/td[2]/span/text()')
        load.add_xpath('zl_co_website','//table[@class="comTinyDes"]//tr[3]/td[2]/span/a/text()')
        load.add_xpath('zl_co_type','//table[@class="comTinyDes"]//tr[1]/td[2]/span/text()')
        load.add_xpath('zl_co_ee_size','//table[@class="comTinyDes"]//tr[2]/td[2]/span/text()')
        load.add_xpath('zl_co_address','//table[@class="comTinyDes"]//tr[5]/td[2]/span/text()')

        load.add_xpath('zl_co_desc','//div[@class="company-content"]/p//text()')

        load.add_value('zl_update_time', repr(date))

        yield load.load_item()