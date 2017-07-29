# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class LagouHistoryItem(scrapy.Item):
    # define the fields for your item here like:
    lg_co_id = scrapy.Field()
    lg_co_short_name = scrapy.Field()
    lg_co_name = scrapy.Field()
    lg_co_website = scrapy.Field()
    lg_co_tags = scrapy.Field()
    lg_co_rounds = scrapy.Field()
    lg_co_ee_size = scrapy.Field()
    lg_co_city = scrapy.Field()

    lg_mgmt_name = scrapy.Field()
    lg_mgmt_title = scrapy.Field()
    lg_mgmt_desc = scrapy.Field()

    lg_prd_name = scrapy.Field()
    lg_prd_desc = scrapy.Field()
    lg_co_desc = scrapy.Field()

    lg_num_position = scrapy.Field()
    lg_handle_rate = scrapy.Field()
    lg_handle_time = scrapy.Field()
    lg_num_review = scrapy.Field()

    # lg_pos_name = scrapy.Field()
    # lg_pos_pay = scrapy.Field()
    # lg_pos_location = scrapy.Field()
    # lg_pos_experience = scrapy.Field()
    # lg_pos_education = scrapy.Field()
    # lg_pos_type = scrapy.Field()
    # lg_pos_desc = scrapy.Field()
    # lg_pos_time = scrapy.Field()

    lg_update_time = scrapy.Field()

def strip(x):
    return x.strip('\t').strip('\n').strip('\r')

def clean(x):
    return x.replace('|','').replace('</p>','').replace('\n','').replace('<p>','').replace('&nbsp','').replace('<br />','').replace('<br/>','').replace('</p>','').replace('"','').replace(' ','')

def span_regex(x):
    clean = re.search(r'<span>.*</span>',x)
    return clean.group().strip('<span>').strip('</span>')

def mgmt_name_clean(x):
    clean = re.findall(r'"name":".+?"',x)
    return clean

def mgmt_title_clean(x):
    clean = re.findall(r'"position":".+?"',x)
    return clean

def mgmt_remark_clean(x):
    clean = re.findall(r'"remark":".+?"',x)
    return clean

def co_desc_clean(x):
    clean = re.search(r'"introduction":{.+?}',x)
    return clean.group().strip('"introduction":')

def prd_desc_clean(x):
    clean = re.findall(r'"productprofile":".+?"',x)
    return clean

def prd_name_clean(x):
    clean = re.findall(r'"product":".+?"',x)
    return clean

def position_count_clean(x):
    clean = re.search(r'"positionCount":\d+',x)
    return clean.group().strip('"positionCount":')

def resume_rate_clean(x):
    clean = re.search(r'"resumeProcessRate":\d+',x)
    return clean.group().strip('"resumeProcessRate":')

def experience_count_clean(x):
    clean = re.search(r'"experienceCount":\d+',x)
    return clean.group().strip('"experienceCount":')

def resume_time_clean(x):
    clean = re.search(r'"resumeProcessTime":\d+',x)
    return clean.group().strip('"resumeProcessTime":')

def co_id_clean(x):
    clean = re.search(r'"companyId":\d+',x)
    return clean.group().strip('"companyId":')

class LagouHistroyLoader(ItemLoader):
    default_item_class = LagouHistoryItem
    default_output_processor = Join()

    lg_co_id_in = MapCompose(strip,co_id_clean,clean)
    lg_co_name_in = MapCompose(strip,clean)
    lg_co_website_in = MapCompose(strip,clean)
    lg_co_tags_in = MapCompose(strip,span_regex,clean)
    lg_co_rounds_in = MapCompose(strip,span_regex,clean)
    lg_co_ee_size_in = MapCompose(strip,span_regex,clean)
    lg_co_city_in = MapCompose(strip,span_regex,clean)

    lg_mgmt_name_in = MapCompose(strip,mgmt_name_clean,clean)
    lg_mgmt_title_in = MapCompose(strip,mgmt_title_clean,clean)
    lg_mgmt_desc_in = MapCompose(strip,mgmt_remark_clean,clean)

    lg_num_position_in = MapCompose(strip,position_count_clean,clean)
    lg_handle_rate_in = MapCompose(strip,resume_rate_clean,clean)
    lg_handle_time_in = MapCompose(strip,resume_time_clean,clean)
    lg_num_review_in = MapCompose(strip,experience_count_clean,clean)

    lg_prd_name_in = MapCompose(strip,prd_name_clean,clean)
    lg_prd_desc_in = MapCompose(strip,prd_desc_clean,clean)
    lg_co_desc_in = MapCompose(strip,co_desc_clean,clean)

    # lg_pos_name_in = MapCompose(strip_space)
    # lg_pos_pay_in = MapCompose(strip_space)
    # lg_pos_location_in = MapCompose(strip_space)
    # lg_pos_experience_in = MapCompose(strip_space)
    # lg_pos_education_in = MapCompose(strip_space)
    # lg_pos_type_in = MapCompose(strip_space)
    # lg_pos_desc_in = MapCompose(strip_space)
    # lg_pos_time_in = MapCompose(strip_space)

class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)