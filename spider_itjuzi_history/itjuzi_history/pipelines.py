# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class RemoveEmptyPipeline(object):

    def process_item(self, item, spider):
        try:
            if item['it_co_id']:
                return item
            else:
                raise DropItem("This Page Does Not Exist")
        except:
            raise DropItem("This Page Does Not Exist")

