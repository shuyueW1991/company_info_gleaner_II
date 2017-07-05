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


class KzjobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    co_web_id = scrapy.Field()
    co_name = scrapy.Field()
    job_name = scrapy.Field()
    job_pay =  scrapy.Field()
    job_add =  scrapy.Field()
    job_suffer = scrapy.Field()
    job_edu = scrapy.Field()
    job_type = scrapy.Field()
    job_desc = scrapy.Field()
    update_datetime = scrapy.Field()
    # pass

class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', '|')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export:
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)
