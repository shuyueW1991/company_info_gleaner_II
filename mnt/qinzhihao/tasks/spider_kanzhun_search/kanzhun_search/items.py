# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


import scrapy
from scrapy.exporters import CsvItemExporter
from scrapy.conf import settings


class KanzhunSearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    positionName = scrapy.Field()
    salary = scrapy.Field()
    description = scrapy.Field()
    job_loc = scrapy.Field()
    job_suffer = scrapy.Field()
    job_edu = scrapy.Field()
    job_type = scrapy.Field()
    job_time = scrapy.Field()

    companyFullName = scrapy.Field()
    companySize = scrapy.Field()
    financeStage = scrapy.Field()
    industryField = scrapy.Field()
    co_des = scrapy.Field()
    co_loc = scrapy.Field()
    # pass

class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', '|')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export:
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)