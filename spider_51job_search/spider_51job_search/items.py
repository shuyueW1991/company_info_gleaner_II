# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class Spider51JobSearchItem(scrapy.Item):
    # define the fields for your item here like:

    qc_job_name = scrapy.Field()
    qc_co_name = scrapy.Field()
    qc_job_loc = scrapy.Field()
    qc_job_pay = scrapy.Field()
    qc_job_date = scrapy.Field()
    qc_job_desc = scrapy.Field()
    qc_co_type = scrapy.Field()
    qc_co_ee_size = scrapy.Field()
    qc_co_tags = scrapy.Field()
    qc_co_desc = scrapy.Field()
    qc_co_address = scrapy.Field()
    qc_job_desc = scrapy.Field()

class search51jobLoader(ItemLoader):
    default_item_class = Spider51JobSearchItem
    default_output_processor = Join()


class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)