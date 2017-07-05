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
            print(item['companyFullName'])
            if len(item):
                print(len(item))
            else:
                print('rien in item!!')
            # if item['co_nm']:
                # self.cursor.execute(sql.format(item['wuyaojob_co_web_id'], item['co_nm'], item['co_staff_num'], item['co_type'], item['co_short_desc']\
                #                            , item['co_add']))
                # self.conn.commit()
                # return item
            flag = 'pos'

            neg_list = ['上海外滩','海外游','海外旅游','房产中介','链家','海底捞','海外背景','海外留学','海外置业','跟单','编辑','买手','采购','推广','广告投放','房产投资','房产','运营','清关','SNS','SEO','facebook','亚马逊','google','SEM','移民','置业','理财','招商','创业','老师','教师','培训','护士','厨师','保险','房产销售','上海外','珠海外','不动产','海外包','猎头']

            for word in neg_list:
                if word in item['companyFullName']:
                    flag = 'neg'
                    break
                for i, val in enumerate(item['positionName']):
                    if word in val:
                        flag = 'neg'
                        break

            if flag == 'pos':
                return item
            else:
                raise DropItem("neg word in item, so it is dropped.")



        except:
            traceback.print_exc()
            raise DropItem("Something nasty happens, nigger!")

