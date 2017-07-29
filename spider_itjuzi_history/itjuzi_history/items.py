# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy
from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter
import re
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class ItjuziHistoryItem(scrapy.Item):
    # define the fields for your item here like:
    it_co_id = scrapy.Field()
    it_short_name = scrapy.Field()
    it_full_name = scrapy.Field()
    it_short_desc = scrapy.Field()
    it_full_desc = scrapy.Field()
    it_desc_tag = scrapy.Field()
    it_ind_tag = scrapy.Field()
    it_location = scrapy.Field()
    it_website = scrapy.Field()
    it_estab_time = scrapy.Field()
    it_ee_size = scrapy.Field()
    it_active_status = scrapy.Field()
    it_investment_info = scrapy.Field()
    it_mgmt_name = scrapy.Field()
    it_mgmt_desc = scrapy.Field()
    it_prd_info = scrapy.Field()
    it_news = scrapy.Field()
    it_milestone = scrapy.Field()
    it_co_views = scrapy.Field()
    it_co_followers = scrapy.Field()
    it_update_time = scrapy.Field()

# Item Loader Functions are Defined Here
def strip_clean(x):
    return x.replace('\t','').replace('\n','').replace(' ','').replace('<b>','').replace('</b>','').replace('\r','').replace('|','').strip('\n')

def co_id_extract(x):
    match = re.search(r'company/\d+',x)
    return match.group().strip('company/')

def co_short_name_extract(x):
    name = x.split('|')[0]
    return name

def estab_time_extract(x):
    match = re.search(r'\d+\.\d+',x)
    if match:
        out = match.group()
    else:
        out = ""
    return out

def co_ee_size_extract(x):
    match = re.search(r'\d+-\d+',x)
    if match:
        out = match.group()
    else:
        out = ""
    return out

# def news_extract(x):
#     for li in x:
#         e = str("")
#         e += "link:" + li.xpath('div/p[1]/a/@href').extract()[0] + ","
#         e += 'text:' + li.xpath('div/p[1]/a/text()').extract()[0] + ","
#         e += 'time:' + li.xpath('div/p[2]/span[1]/text()').extract()[0] + ","
#         e += 'tag:' + li.xpath('div/p[2]/span[2]/text()').extract()[0] + ","
#         e += 'from:' + li.xpath('div/p[2]/span[2]/text()').extract()[0] + ";"
#     return e

class ItjuziHistoryLoader(ItemLoader):
    default_item_class = ItjuziHistoryItem
    default_output_processor = Join()
    it_co_id_in = MapCompose(co_id_extract,strip_clean)
    it_short_name_in = MapCompose(co_short_name_extract,strip_clean)
    it_full_name_in = MapCompose(strip_clean)
    it_short_desc_in = MapCompose(strip_clean)
    it_full_desc_in = MapCompose(strip_clean)
    it_desc_tag_in = MapCompose(strip_clean)
    it_ind_tag_in = MapCompose(strip_clean)
    it_location_in = MapCompose(strip_clean)
    it_website_in = MapCompose(strip_clean)
    it_estab_time_in = MapCompose(strip_clean,estab_time_extract)
    it_ee_size_in = MapCompose(strip_clean,co_ee_size_extract)
    it_active_status_in = MapCompose(strip_clean)
    it_mgmt_name_in = MapCompose(strip_clean)
    it_mgmt_desc_in = MapCompose(strip_clean)
    it_prd_info_in = MapCompose(strip_clean)
    it_investment_info_in = MapCompose(strip_clean)
    it_news_in = MapCompose(strip_clean)
    it_milestone_in = MapCompose(strip_clean)
    it_co_views_in = MapCompose(strip_clean)
    it_co_followers_in = MapCompose(strip_clean)
    it_update_time_in = MapCompose(strip_clean)

class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)

