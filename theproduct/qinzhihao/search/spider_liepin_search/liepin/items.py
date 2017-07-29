# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.conf import settings
from scrapy.exporters import CsvItemExporter
import re
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class LiepinItem(scrapy.Item):
    # define the fields for your item here like:
    # def __init__(self):
    # lp_job = scrapy.Field()
    # lp_pay = scrapy.Field()
    # lp_location = scrapy.Field()
    # lp_diploma = scrapy.Field()
    # lp_exp = scrapy.Field()
    #
    # lp_co_nm = scrapy.Field()
    # lp_co_lk = scrapy.Field()
    # lp_co_fld = scrapy.Field()
    # lp_welfare = scrapy.Field()
    #
    # lp_rls_time = scrapy.Field()
    # lp_fdbktime = scrapy.Field()
    #
    # lp_update_datetime =scrapy.Field()
    #
    # lp_co_full_nm = scrapy.Field()



    lp_job_id = scrapy.Field()

    companySize = scrapy.Field()
    industryField = scrapy.Field()
    companyFullName = scrapy.Field()
    lp_co_lk = scrapy.Field()
    financeStage = scrapy.Field()
    lp_co_add = scrapy.Field()
    lp_co_intro = scrapy.Field()

    lp_job_pub_nm = scrapy.Field()
    lp_job_pub_pos = scrapy.Field()
    lp_job_apply_check_rate = scrapy.Field()
    lp_job_apply_check_dur = scrapy.Field()
    positionName = scrapy.Field()
    salary = scrapy.Field()
    lp_job_apply_fdbk = scrapy.Field()
    lp_job_add = scrapy.Field()
    lp_job_pub_time = scrapy.Field()
    lp_job_quals = scrapy.Field()
    description = scrapy.Field()
    lp_job_dept = scrapy.Field()
    lp_job_major = scrapy.Field()
    lp_job_boss = scrapy.Field()
    lp_job_subordinate = scrapy.Field()

    # lp_update_datetime =scrapy.Field()

def strip_clean(x):
    return x.replace('\t','').replace('\n','').replace(' ','').replace('<b>','').replace('</b>','').replace('\r','').replace('|','')

class LiepinLoader(ItemLoader):
    default_item_class = LiepinItem
    default_output_processor = Join()
    lp_job_id_in = MapCompose(strip_clean)
    companySize_in = MapCompose(strip_clean)
    industryField_in = MapCompose(strip_clean)
    companyFullName_in = MapCompose(strip_clean)
    lp_co_lk_in = MapCompose(strip_clean)
    financeStage_in = MapCompose(strip_clean)
    lp_co_add_in = MapCompose(strip_clean)
    lp_co_intro_in = MapCompose(strip_clean)
    lp_job_pub_nm_in = MapCompose(strip_clean)
    lp_job_pub_pos_in = MapCompose(strip_clean)
    lp_job_apply_check_rate_in = MapCompose(strip_clean)
    lp_job_apply_check_dur_in = MapCompose(strip_clean)
    positionName_in = MapCompose(strip_clean)
    salary_in = MapCompose(strip_clean)
    lp_job_apply_fdbk_in = MapCompose(strip_clean)
    lp_job_add_in = MapCompose(strip_clean)
    lp_job_pub_time_in = MapCompose(strip_clean)
    lp_job_quals_in = MapCompose(strip_clean)
    description_in = MapCompose(strip_clean)
    lp_job_dept_in = MapCompose(strip_clean)
    lp_job_major_in = MapCompose(strip_clean)
    lp_job_boss_in = MapCompose(strip_clean)
    lp_job_subordinate = MapCompose(strip_clean)

class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export :
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)