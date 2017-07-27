# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class LagouSearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    companyID = scrapy.Field()
    companyFullName = scrapy.Field()
    companyShortName = scrapy.Field()
    companySize = scrapy.Field()
    financeStage = scrapy.Field()
    industryField = scrapy.Field()
    jobNature = scrapy.Field()
    positionID = scrapy.Field()
    positionName = scrapy.Field()
    positionLables = scrapy.Field()
    city = scrapy.Field()
    education = scrapy.Field()
    salary = scrapy.Field()
    firstType = scrapy.Field()
    secondType = scrapy.Field()
    workYear = scrapy.Field()
    formatCreatedTime = scrapy.Field()
    scrapeTime = scrapy.Field()
    description = scrapy.Field()

def clean(x):
    return x.replace('</p>','').replace('\r','').replace('\t','').replace('\n','').replace('<p>','').replace('&nbsp','').replace('<br />','').replace('<br/>','').replace('</p>','').replace('"','').replace(' ','')


class LagouSearchLoader(ItemLoader):
    default_item_class = LagouSearchItem
    default_output_processor = Join()
    companyID_in = MapCompose(clean)
    companyFullName_in = MapCompose(clean)
    companyShortName_in = MapCompose(clean)
    companySize_in = MapCompose(clean)
    financeStage_in = MapCompose(clean)
    industryField_in = MapCompose(clean)
    jobNature_in = MapCompose(clean)
    positionID_in = MapCompose(clean)
    positionName_in = MapCompose(clean)
    positionLables_in = MapCompose(clean)
    city_in = MapCompose(clean)
    education_in = MapCompose(clean)
    salary_in = MapCompose(clean)
    firstType_in = MapCompose(clean)
    secondType_in = MapCompose(clean)
    workYear_in = MapCompose(clean)
    formatCreatedTime_in = MapCompose(clean)
    scrapeTime_in = MapCompose(clean)
    description_in = MapCompose(clean)

class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)