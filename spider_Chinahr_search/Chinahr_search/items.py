# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.exporters import CsvItemExporter


class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', '|')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export:
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)


class ChinahrSearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    job_name = scrapy.Field()
    job_pay = scrapy.Field()
    job_add = scrapy.Field()
    job_limit = scrapy.Field()

    co_name=scrapy.Field()
    co_ee_size = scrapy.Field()
    co_type = scrapy.Field()
    co_ownership = scrapy.Field()
    co_contact=scrapy.Field()
    co_mob=scrapy.Field()
    co_tel=scrapy.Field()
    co_email=scrapy.Field()
    co_link = scrapy.Field()
    co_add = scrapy.Field()
    co_inner_web=scrapy.Field()











    # pass
