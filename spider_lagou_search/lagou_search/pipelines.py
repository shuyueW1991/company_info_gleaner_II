# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem

class CleanPipeline(object):

    def process_item(self, item, spider):
        item["description"] = str(item["description"]).replace('</p>','').replace('\r','').replace('\t','').replace('\n','').replace('<p>','').replace('&nbsp','').replace('<br />','').replace('<br/>','').replace('</p>','').replace('"','').replace(' ','')

