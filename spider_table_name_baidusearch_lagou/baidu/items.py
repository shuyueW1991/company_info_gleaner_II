# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduLeftNonbdItem(scrapy.Item):
    bd_coname = scrapy.Field()
    bd_ln_head = scrapy.Field()
    bd_ln_abs =scrapy.Field()
    pass

# class BaiduLeftBdItem(scrapy.Item):
#     bd_coname = scrapy.Field()
#     bd_lb_txt = scrapy.Field()
#     # bd_lb_abs = scrapy.Field()
#     pass
