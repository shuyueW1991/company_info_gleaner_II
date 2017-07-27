# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import traceback
import datetime
from scrapy.exceptions import DropItem
from scrapy.exceptions import DropItem

class SpiderOfficialWebsitesPipeline(object):
    def __init__(self):
        # upload to database ...
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"
        self.conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                                    passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        self.cursor = self.conn.cursor(pymysql.cursors.SSDictCursor)

    def process_item(self, item, spider):

        sql = "insert into homepage_content(host, url, content) values ('{0}', '{1}', '{2}')"

        if item['content']:
                try:
                    self.cursor.execute(sql.format(item['host_url'],item['url'],item['content']))
                    self.conn.commit()

                except:
                    print('something shit happen!')

        else:
            pass


class HtmlDownloadPipe(object):

    def proces_item(self, item, spider):
        return item
