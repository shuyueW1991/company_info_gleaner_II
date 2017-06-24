# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinItem(scrapy.Item):
    # define the fields for your item here like:
    # def __init__(self):
    lp_exist = scrapy.Field()

    lp_job_id = scrapy.Field()

    lp_co_stf_num = scrapy.Field()
    lp_co_tag = scrapy.Field()
    lp_co_nm = scrapy.Field()
    lp_co_lk = scrapy.Field()
    lp_co_ownership = scrapy.Field()
    lp_co_add = scrapy.Field()
    lp_co_intro = scrapy.Field()
    # pass
    lp_job_pub_nm = scrapy.Field()
    lp_job_pub_pos = scrapy.Field()
    lp_job_apply_check_rate = scrapy.Field()
    lp_job_apply_check_dur = scrapy.Field()

    lp_job_nm = scrapy.Field()
    lp_job_salary = scrapy.Field()
    lp_job_apply_fdbk = scrapy.Field()
    lp_job_add = scrapy.Field()
    lp_job_pub_time = scrapy.Field()
    lp_job_quals = scrapy.Field()
    lp_job_descr = scrapy.Field()
    lp_job_dept = scrapy.Field()
    lp_job_major = scrapy.Field()
    lp_job_boss = scrapy.Field()
    lp_job_subordinate = scrapy.Field()

    lp_update_datetime =scrapy.Field()
