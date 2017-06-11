# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.conf import settings
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.exporters import CsvItemExporter
from scrapy.loader.processors import TakeFirst, MapCompose, Join
import re

class SpiderZhilianSearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    job_nm = scrapy.Field()
    month_pay = scrapy.Field()
    job_loc = scrapy.Field()

    co_id = scrapy.Field()
    co_nm = scrapy.Field()
    co_ownership = scrapy.Field()
    co_ee_size = scrapy.Field()
    co_link = scrapy.Field()
    co_industry = scrapy.Field()
    co_add = scrapy.Field()
    co_desc = scrapy.Field()
#
def clean(x):
    return x.replace('|',"").replace("\n","").replace('\t',"").replace('\r',"").replace(' ',"")


def numeric_only(x):
    text = re.sub("\D", "", x)
    if text:
        return str(text)
    else:
        return 'NaN'
#
class SpiderZhilianSearchLoader(ItemLoader):
    default_item_class = SpiderZhilianSearchItem
    default_output_processor = Join()


    co_id_in = MapCompose(numeric_only)
    co_nm_in = MapCompose(clean)
    co_ownership_in = MapCompose(clean)
    co_ee_size_in = MapCompose(clean)
    # co_link_in = MapCompose(clean)
    co_industry_in = MapCompose(clean)
    co_add_in = MapCompose(clean)
    co_desc_in = MapCompose(clean)

class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)
