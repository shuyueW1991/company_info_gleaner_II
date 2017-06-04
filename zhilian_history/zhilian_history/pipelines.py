# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class ZhilianHistoryPipeline(object):
    def process_item(self, item, spider):
        return item

class RemoveEmptyPipeline(object):

    def process_item(self, item, spider):
        try:
            if str(item['zl_co_id']).startswith('C'):
                return item
            else:
                raise DropItem("None Company ID")
        except:
            raise DropItem("This Page Does Not Exist")