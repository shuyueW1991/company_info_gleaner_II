# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class SpiderOfficialWebsitesPipeline(object):
    def process_item(self, item, spider):
        if item['email']:
            return item
        else:
            raise DropItem("missing contact info in {}".format(item))

class HtmlDownloadPipe(object):

    def proces_item(self, item, spider):
        return item
