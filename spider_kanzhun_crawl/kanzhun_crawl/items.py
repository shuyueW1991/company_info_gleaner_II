# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.exporters import CsvItemExporter
from scrapy.conf import settings
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose



class KanzhunCrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    co_short_nm = scrapy.Field()
    co_type = scrapy.Field()
    co_city = scrapy.Field()
    co_staff_num = scrapy.Field()
    co_short_desc = scrapy.Field()
    co_goodcommnt_rate = scrapy.Field()
    co_goodcommnt_rate_emply_num = scrapy.Field()
    co_avg_pay =scrapy.Field()
    co_avg_pay_emply_num = scrapy.Field()


def strip(x):
    return x.strip('\t').strip('\n').strip('\r').strip(" ").strip(' ')

def clean(x):
    return x.replace('|','').replace('"','')

def numeric_only(x):
    text = re.sub("\D","", x)
    return str(text)

def list_string_merge(x):
    return "".join(x)

def void_alert(x):
    if x == "":
        print('void alert!!!')

    print(x)




# def span_regex(x):
#     clean = re.search(r'<span>.*</span>',x)
#     return clean.group(0).strip('<span>').strip('</span>')
#
# def p_regex(x):
#     clean = re.search(r'<p>.*</p>',x)
#     return clean.group(0).strip('<p>').strip('</p>')
#
# def mgmt_name_clean(x):
#     clean = re.findall(r'"name":".+?"',x)
#     return clean
#
# def mgmt_title_clean(x):
#     clean = re.findall(r'"position":".+?"',x)
#     return clean
#
# def mgmt_remark_clean(x):
#     clean = re.findall(r'"remark":".+?"',x)
#     return clean
#
# def co_desc_clean(x):
#     clean = re.search(r'"introduction":{.+?}',x)
#     return clean.group().strip('"introduction":')
#
# def prd_desc_clean(x):
#     clean = re.findall(r'"productprofile":".+?"',x)
#     return clean
#
# def prd_name_clean(x):
#     clean = re.findall(r'"product":".+?"',x)
#     return clean
#
# def position_count_clean(x):
#     clean = re.search(r'"positionCount":\d+',x)
#     return clean.group().strip('"positionCount":')
#
# def resume_rate_clean(x):
#     clean = re.search(r'"resumeProcessRate":\d+',x)
#     return clean.group().strip('"resumeProcessRate":')
#
# def experience_count_clean(x):
#     clean = re.search(r'"experienceCount":\d+',x)
#     return clean.group().strip('"experienceCount":')
#
# def resume_time_clean(x):
#     clean = re.search(r'"resumeProcessTime":\d+',x)
#     return clean.group().strip('"resumeProcessTime":')
#
# def co_id_clean(x):
#     clean = re.search(r'"companyId":\d+',x)
#     return clean.group().strip('"companyId":')

class KanzhunCrawlLoader(ItemLoader):
    default_item_class = KanzhunCrawlItem
    default_output_processor = Join()

    co_short_nm_in = MapCompose(strip,clean)
    co_type_in = MapCompose(strip,clean)
    co_city_in = MapCompose(strip,clean)
    co_staff_num_in = MapCompose(strip,clean)
    co_short_desc_in = MapCompose(strip,clean)
    co_goodcommnt_rate_in = MapCompose(numeric_only)
    co_goodcommnt_rate_emply_num_in = MapCompose(numeric_only)

    co_avg_pay_in = MapCompose(numeric_only)
    co_avg_pay_emply_num_in = MapCompose(numeric_only)



class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export:
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)
