# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import pymysql
import traceback
import datetime
from scrapy.exceptions import DropItem


class SpiderZhilianSearchPipeline(object):
    # def __init__(self):
    #     # upload to database ...
    #     self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
    #     self.source_mysql_db = "buz_source_data"
    #     self.source_mysql_user = "root"
    #     self.source_mysql_passwd = "u8!7-ZXC"
    #     self.conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
    #                                 passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
    #     self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)



    def process_item(self, item, spider):
        # sql = "insert into wuyaojob_co_template(wuyaojob_co_web_id,co_nm,co_staff_num,co_type,co_short_desc,co_add)\
        # values ('{0}', '{1}', '{2}', '{3}', '{4}','{5}')"

        try:
            print(item['co_nm'])
            if len(item):
                print(len(item))
            else:
                print('rien in item!!')
            # if item['co_nm']:
                # self.cursor.execute(sql.format(item['wuyaojob_co_web_id'], item['co_nm'], item['co_staff_num'], item['co_type'], item['co_short_desc']\
                #                            , item['co_add']))
                # self.conn.commit()
                # return item
            return item


        except:
            traceback.print_exc()
            raise DropItem("Something nasty happens, nigger!")

