# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import traceback
import datetime
from scrapy.exceptions import DropItem

class SpiderChinahrPipeline(object):
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
        # sql = "insert into chinahr_co(chr_co_name, chr_co_city, chr_co_industry, chr_co_type, chr_co_estab, chr_co_regcap, chr_contact_name, chr_mobile_num, chr_fixline_num, chr_email_addr, chr_co_address, chr_co_desc, chr_co_url) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')"
        sql1 = "insert into chinahr_co(chr_co_name, chr_co_city, chr_co_industry, chr_co_type, chr_co_estab, chr_co_regcap, chr_contact_name, chr_mobile_num, chr_fixline_num, chr_email_addr, chr_co_address, chr_co_desc, chr_web) values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')"
        # try:
        #     if item['co_name']:
        #         # self.cursor.execute(sql.format(item['co_web_id'], item['co_name'], item['co_add'], item['co_type'], item['co_number']\
        #         #                            , item['co_web_add']))
        #         # self.conn.commit()
        #         # return item

        #
        #
        # except:
        #     # traceback.print_exc()
        #     raise DropItem("Something nasty happens, nigger!")

        # self.cursor.execute(sql.format(item['chr_co_name'], item['chr_co_city'], item['chr_co_industry'], item['chr_co_type'], item['chr_co_estab'], item['chr_co_regcap'], item['chr_contact_name'], item['chr_mobile_num'], item['chr_fixline_num'], item['chr_email_addr'], item['chr_co_address'], item['chr_co_desc'], item['chr_co_url']))
        def void_to_NaN(self, content):
            if len(content) > 0:
                return content
            else:
                content = "NaN"
                return content

        for k, v in item.items():
            if len(v) == 0:
                v = 'NaN'
        print('checked. okay.')

        if item['chr_co_name']:
            self.cursor.execute(
                sql1.format(item['chr_co_name'], item['chr_co_city'], item['chr_co_industry'], item['chr_co_ownership'],
                           item['chr_co_estab'], item['chr_co_regcap'], item['chr_contact_name'],
                           item['chr_mobile_num'], item['chr_fixline_num'], item['chr_email_addr']
                            ,item['chr_co_address'], item['chr_co_des'], item['chr_co_url']))
            self.conn.commit()
        # return item