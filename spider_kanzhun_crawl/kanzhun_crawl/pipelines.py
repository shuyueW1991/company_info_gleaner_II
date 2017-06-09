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


class KanzhunCrawlPipeline(object):
    def __init__(self):
        # upload to database ...
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"
        self.conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                                    passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)


    def void_to_NaN(self,content):
        if len(content) > 0:
            return content
        else:
            content = "NaN"
            return content


    def process_item(self, item, spider):
        sql = "insert into kanzhun_co_init(co_short_nm, co_type, co_city, co_staff_num, co_short_desc, co_goodcommnt_rate, co_goodcommnt_rate_emply_num, co_avg_pay, co_avg_pay_emply_num) \
        values ('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}','{7}', '{8}')"
        # if len(item['title']) > 0:
        #     try:
        #         print("++++++++++++++++++++++++++++++++++++")
        #         self.cursor.execute(sql.format(item['url'], item['title'][0].replace(" ", ""), item['time'][0],
        #                                        ";".join(item['guilei']).replace(" ", ""),
        #                                        ";".join(item['abst']).replace(" ", ""),
        #                                        ";".join(item['contents']).replace(" ", ""),
        #                                        ";".join(item['tags']).replace(" ", ""), curTime))
        #         self.conn.commit()
        #     except:
        #         traceback.print_exc()


        try:
            if len(item['co_short_nm']) > 0:
                print("++++++++++++++++++++++++++++++++++++")
                print(type(item['co_short_nm']))
                print(len(item['co_short_nm']))
                print("++++++++++++++++++++++++++++++++++++")
                print(type(item['co_type']))
                print(len(item['co_type']))
                print("++++++++++++++++++++++++++++++++++++")
                print(type(item['co_city']))
                print(len(item['co_city']))
                print("++++++++++++++++++++++++++++++++++++")
                print(type(item['co_staff_num']))
                print(len(item['co_staff_num']))
                print("++++++++++++++++++++++++++++++++++++")
                print(type(item['co_short_desc']))
                print(len(item['co_short_desc']))
                print("++++++++++++++++++++++++++++++++++++")
                print(type(item['co_goodcommnt_rate']))
                print(len(item['co_goodcommnt_rate']))
                print("++++++++++++++++++++++++++++++++++++")
                print(type(item['co_goodcommnt_rate_emply_num']))
                print(len(item['co_goodcommnt_rate_emply_num']))
                print("++++++++++++++++++++++++++++++++++++")
                print(type(item['co_avg_pay']))
                print(len(item['co_avg_pay']))
                print("++++++++++++++++++++++++++++++++++++")
                print(type(item['co_avg_pay_emply_num']))
                print(len(item['co_avg_pay_emply_num']))

                for k,v in item.items():
                    if len(v) == 0:
                        v = 'NaN'
                print('checked. okay.')


                self.cursor.execute(sql.format(item['co_short_nm'], item['co_type'], item['co_city'], item['co_staff_num'], item['co_short_desc']\
                                               , item['co_goodcommnt_rate'], \
                                               item['co_goodcommnt_rate_emply_num'], \
                                               item['co_avg_pay'][:], \
                                               item['co_avg_pay_emply_num']))
                self.conn.commit()
                return item
            else:
                raise DropItem("This Page Does Not Exist")


        except:
            traceback.print_exc()
            raise DropItem("This Page Does Not Exist")


#
# class RemoveEmptyPipeline(object):
#
#     def process_item(self, item, spider):
#         try:
#             if item['lg_co_id']:
#                 return item
#             else:
#                 raise DropItem("This Page Does Not Exist")
#         except:
#             raise DropItem("This Page Does Not Exist")