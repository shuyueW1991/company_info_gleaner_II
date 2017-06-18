# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class ZhilianItem(scrapy.Item):
    # define the fields for your item here like:
    zl_co_id = scrapy.Field()
    zl_co_name = scrapy.Field()
    zl_co_tags = scrapy.Field()
    zl_co_website = scrapy.Field()
    zl_co_type = scrapy.Field()
    zl_co_ee_size = scrapy.Field()
    zl_co_address = scrapy.Field()
    zl_co_desc = scrapy.Field()
    zl_update_time = scrapy.Field()

def clean(x):
    return x.replace('|','').replace('</p>','').replace("\n",'').replace('\t','').replace('\r','').replace("<p>",'').replace('&nbsp','').replace('<br />','').replace('<br/>','').replace('</p>','').replace('"','').replace(' ','')


class ZhilianLoader(ItemLoader):
    default_item_class = ZhilianItem
    default_output_processor = Join()

    zl_co_id_in = MapCompose(clean)
    zl_co_name_in = MapCompose(clean)
    zl_co_tags_in = MapCompose(clean)
    zl_co_website_in = MapCompose(clean)
    zl_co_type_in = MapCompose(clean)
    zl_co_ee_size_in = MapCompose(clean)
    zl_co_address_in = MapCompose(clean)
    zl_co_desc_in = MapCompose(clean)


class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)
