# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import types
import codecs
import re
import traceback
import pymysql
import string

class BaiduPipeline(object):
    def __init__(self):

        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"
        self.conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user, passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def process_item(self, item, spider):
        line = ''
        for k in item:
            if item[k]:
                if not isinstance(item[k], str):
                    for j in range(len(item[k])):
                        if item[k][j]:
                            content = item[k][j].replace("\n", "").replace("\t", "").replace("\r", "").replace('|', '')
                            content_cl = re.sub(r'<[^>]+>', '', content)
                            content_clean = re.sub(r'\s+', '', content_cl)
                            # print('*****************************')
                            # print(content)
                            line = line + content_clean + '|'
                        else:
                            line = line + 'NaN'+ '|'
                else:
                    content = item[k].replace("\n", "").replace("\t", "").replace("\r", "").replace('|', '')
                    content_cl = re.sub(r'<[^>]+>', '', content)
                    content_clean = re.sub(r'\s+', '', content_cl)
                    # print('*****************************')
                    # print(content)
                    line = line + content_clean+ '|'
            else:
                line = line + 'NaN'+ '|'
            line = line + '|'

        line = line.rstrip('|')
        # print(line.split("|")[0])
        # searchword = line.split("|")[0]
        searchword = item['bd_coname']
        # print('coname is that:' + searchword)

        print('line type is :\n')
        print(type(line))
        print('coname type is \n')
        print(type(searchword))


        # sql = "insert into lp_co_nm_bd(lp_co_nm, lp_co_bd) values ({0},{1}) on DUPLICATE KEY UPDATE lp_co_nm=values(lp_co_nm)"
        sql = "insert into it_co_nm_bd(it_co_nm, it_co_bd) values ('{0}', '{1}')"

        try:
            self.cursor.execute(sql.format(searchword, line))
            self.conn.commit()
        except:
            traceback.print_exc()

        return item
