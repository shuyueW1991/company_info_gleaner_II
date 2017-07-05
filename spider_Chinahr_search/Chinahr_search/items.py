# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.exporters import CsvItemExporter
from scrapy.conf import settings

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

    positionName = scrapy.Field()
    salary = scrapy.Field()
    job_add = scrapy.Field()
    job_limit = scrapy.Field()

    companyFullName=scrapy.Field()
    companySize = scrapy.Field()
    industryField = scrapy.Field()
    financeStage = scrapy.Field()
    co_contact=scrapy.Field()
    co_mob=scrapy.Field()
    co_tel=scrapy.Field()
    co_email=scrapy.Field()
    co_link = scrapy.Field()
    co_add = scrapy.Field()
    co_inner_web=scrapy.Field()
    description = scrapy.Field()











    # pass
