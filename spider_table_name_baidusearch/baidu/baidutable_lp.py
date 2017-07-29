# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import traceback
import datetime
import time
import requests
import os
import subprocess
import codecs
import pymysql

class baiduProcess(object):
    def __init__(self):
        self.to_word_api = 'http://218.244.132.122:8080/api/HanLpAPI/toWord'
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"

    def baiduit(self, word):
        word1 = word.replace(" ","").replace("(","").replace(")","").replace("（","").replace("）","")
        print('**************'+word)
        try:
            scrapystring = 'scrapy crawl bdsearch -a searchword=' + str(word1)
            print(scrapystring)
            os.system(scrapystring)

        except:
            print('An error may\' ve occur\'d, nigga!\n')

    def main_process(self):
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        lp_sql = "select lp_co_nm from lp_info_co_part"
        try:
            cursor.execute(lp_sql)
            lp_res = cursor.fetchall()
            for item in lp_res:
                lp_co_nm = item["lp_co_nm"]
                # print("***********************")
                # print("\n"+lp_co_nm)
                # lp_upload_sql = "insert into lp_co_nm_bd(lp_co_nm) values ('{0}') on DUPLICATE KEY UPDATE lp_co_nm=values(lp_co_nm)"
                # cursor.execute(lp_upload_sql.format(lp_co_nm))
                # conn.commit()

                self.baiduit(str(lp_co_nm))
                # filecheck = open(str(lp_co_nm).replace(" ","") + '.csv', 'r')
                # lines = len(filecheck.readlines())
                # if lines < 2:
                #     self.baiduit(lp_co_nm)
                # else:
                #     deletestring = 'rm ' + lp_co_nm + '.csv'
                #     os.system(deletestring)

            cursor.close()
        except:
            traceback.print_exc()

if __name__ == '__main__':
    c = baiduProcess()
    c.main_process()
