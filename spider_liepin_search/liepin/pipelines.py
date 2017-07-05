# -*- coding: utf-8 -*-
import codecs
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import types

from scrapy.exceptions import DropItem

class LiepinPipeline(object):

    def process_item(self, item, spider):
        try:
            if item['lp_job_id']:
                return item
            else:
                raise DropItem("This Page Does Not Exist, nigga!\n")
        except:
            raise DropItem("This Page Does Not Exist")
