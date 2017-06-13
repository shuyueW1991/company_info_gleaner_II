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


class SpiderChinahrItem(scrapy.Item):
    # define the fields for your item here like:
    chr_co_name = scrapy.Field()
    chr_co_city = scrapy.Field()
    chr_co_industry = scrapy.Field()
    chr_co_type = scrapy.Field()
    chr_co_estab = scrapy.Field()
    chr_co_regcap = scrapy.Field()
    chr_contact_name = scrapy.Field()
    chr_mobile_num = scrapy.Field()
    chr_fixline_num = scrapy.Field()
    chr_email_addr = scrapy.Field()
    chr_co_address = scrapy.Field()
    chr_co_desc = scrapy.Field()

def clean(x):
    return x.replace('\r', '').replace('\t', '').replace('\n', '').replace("\n", '').replace('"', '').replace(" ", "").replace("\"", "").replace("|","")


class SpiderChinahrLoader(ItemLoader):
    default_item_class = SpiderChinahrItem
    default_output_processor = Join()

    chr_co_name_in = MapCompose(clean)
    chr_co_city_in = MapCompose(clean)
    chr_co_industry_in = MapCompose(clean)
    chr_co_type_in = MapCompose(clean)
    chr_co_estab_in = MapCompose(clean)
    chr_co_regcap_in = MapCompose(clean)
    chr_contact_name_in = MapCompose(clean)
    chr_mobile_num_in = MapCompose(clean)
    chr_fixline_num_in = MapCompose(clean)
    chr_email_addr_in = MapCompose(clean)
    chr_co_address_in = MapCompose(clean)
    chr_co_desc_in = MapCompose(clean)


class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)