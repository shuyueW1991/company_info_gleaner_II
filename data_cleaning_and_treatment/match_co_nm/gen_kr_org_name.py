# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import traceback
import datetime
import requests
import json
class KrOrgRecog(object):
    def __init__(self):
        mode = "prod"
        if mode == 'dev':
            self.source_mysql_host="localhost"
            self.source_mysql_db="buz_source_data"
            self.source_mysql_user="root"
            self.source_mysql_passwd="123456"
        else:
            self.to_word_api = 'http://218.244.132.122:8080/api/HanLpAPI/toWord'
            self.source_mysql_host="rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
            self.source_mysql_db="buz_source_data"
            self.source_mysql_user="root"
            self.source_mysql_passwd="u8!7-ZXC"
 
    def update_kr_org_name(self, kr_id, kr_title_org_name, kr_content_org_name):
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user, passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "update kr_news set kr_title_org_name='{0}', kr_content_org_name='{1}' where kr_id={2} "
        try:
            cursor.execute(sql.format(kr_title_org_name, kr_content_org_name, kr_id))
            conn.commit()
            print(kr_title_org_name, kr_content_org_name, kr_id)
        except:
            traceback.print_exc()
        cursor.close()
        conn.close()

    def gen_org_names(self):
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user, passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select kr_id, kr_title, kr_content from kr_news limit 10"
        try:
            cursor.execute(sql)
            res = cursor.fetchall()
            for item in res:
                kr_id = item["kr_id"]
                kr_title = item["kr_title"]
                kr_content = item["kr_content"]
                self.recog_org_name(kr_id, kr_title, kr_content)
        except:
            pass
        cursor.close()
        conn.close()

    def recog_org_name(self, kr_id, kr_title, kr_content):
        title = {"text": kr_title}
        if len(kr_content) > 800:
            content = {"text": kr_content[0:800]} 
        else:
            content = {"text": kr_content}
        title_words = requests.post(self.to_word_api,params=title)
        title_info = json.loads(title_words.content.decode("utf8"))
   
        content_words = requests.post(self.to_word_api,params=content)
        content_info = json.loads(content_words.content.decode("utf8"))

        title_org_name_list = []
        content_org_name_list = []
        for item in content_info:
            nature = item['nature']
            org_name = item['word']
            if nature == 'nt':
                content_org_name_list.append(org_name)
        if len(content_org_name_list) > 0:
            kr_content_org_name = ";".join(content_org_name_list)
        else:
            kr_content_org_name = ""

        for item in title_info:
            nature = item['nature']
            org_name = item['word']
            if nature == 'nt':
                title_org_name_list.append(org_name)                   
        if len(title_org_name_list) > 0:
            kr_title_org_name = ";".join(title_org_name_list)
        else:
            kr_title_org_name = ""
        self.update_kr_org_name(kr_id, kr_title_org_name, kr_content_org_name)

if __name__ == '__main__':
    c = KrOrgRecog()
    c.gen_org_names() 
