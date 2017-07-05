# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import traceback
import datetime
from scrapy.exceptions import DropItem

class KzjobPipeline(object):
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
        sql = "insert into kanzhun_job_info(co_web_id,co_name,job_name,job_pay,job_add,job_suffer,job_edu,job_type,job_desc,update_datetime) values ('{0}', '{1}', '{2}', '{3}', '{4}','{5}','{6}','{7}','{8}','{9}')"

        # try:
        #     if item['co_name']:
        #         self.cursor.execute(sql.format(item['co_web_id'], item['co_name'], item['co_add'], item['co_type'], item['co_number']\
        #                                    , item['co_web_add']))
        #         self.conn.commit()
        #         # return item
        #
        # except:
        #     # traceback.print_exc()
        #     raise DropItem("Something nasty happens, nigger!")


        if item['co_name']:
            self.cursor.execute(sql.format(item['co_web_id'], item['co_name'], item['job_name'], item['job_pay'], item['job_add'], item['job_suffer'], item['job_edu'], item['job_type'],item['job_desc'], item['update_datetime']))
            self.conn.commit()

        # except:
        #     # traceback.print_exc()
        #     raise DropItem("Something nasty happens, nigger!")
        # return item

