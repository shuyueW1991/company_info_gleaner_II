# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import traceback
import datetime
class KrPipeline(object):
    def __init__(self):
        mode = "prod"
        if mode == 'dev':
            self.source_mysql_host="localhost"
            self.source_mysql_db="buz_source_data"
            self.source_mysql_user="root"
            self.source_mysql_passwd="123456"
            self.conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user, passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        else:
            self.source_mysql_host="rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
            self.source_mysql_db="buz_source_data"
            self.source_mysql_user="root"
            self.source_mysql_passwd="u8!7-ZXC"
            self.conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user, passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
 
    def process_item(self, item, spider):
        curTime =  datetime.datetime.now()
        sql = "insert into kr_news(kr_url, kr_title, kr_rls_time, kr_cate, kr_abstr, kr_content, kr_ind_tag, create_time) values ('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}','{7}')"
        if len(item['title']) > 0:
            try:
                print("++++++++++++++++++++++++++++++++++++")
                self.cursor.execute(sql.format(item['url'], item['title'][0].replace(" ",""), item['time'][0], ";".join(item['guilei']).replace(" ",""), ";".join(item['abst']).replace(" ",""), ";".join(item['contents']).replace(" ",""), ";".join(item['tags']).replace(" ",""), curTime))
                self.conn.commit()
            except:
                traceback.print_exc()
        return item
