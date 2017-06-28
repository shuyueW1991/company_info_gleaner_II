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


class BosszpCoPipeline(object):
    def __init__(self):
        # upload to database ...
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"
        self.conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                                    passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)



    def process_item(self, item, spider):
        sql = "insert into bosszp_co(bosszp_co_web_id,co_short_nm,co_financing_round,co_staff_num,co_type,co_link,co_emply_blank,co_boss_num,co_short_desc) values ('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}','{7}', '{8}')"

        # try:
        print('co_short_desc' in item)
        print('co_short_nm' in item)
        if item['co_short_desc'] is not None:
            self.cursor.execute(sql.format(item['bosszp_co_web_id'], item['co_short_nm'], item['co_financing_round'], item['co_staff_num'], item['co_type'], item['co_link'], item['co_emply_blank'], item['co_boss_num'], item['co_short_desc']))
            self.conn.commit()
            # return item

        # except:
        #     traceback.print_exc()
            # raise DropItem("This Page Does Not Exist")





