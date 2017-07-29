# -*- coding: utf-8 -*-

import pymysql
import traceback
import datetime
import requests
import json
import re

class MatchLgLpCoNames(object):
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
 
    def map_lg_lp_coinfo(self):
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user, passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        map_lp_lg_sql = "insert into map_lp_lg_co_names(`lp_co_id`,`lg_co_id`,`lp_co_name` , `lg_co_name` ) SELECT * from (select a.`id`, b.`lg_co_id`, a.`lp_co_nm` , b.`lg_co_name`  FROM `buz_source_data`.`lp_info_co_part` a join `lagou_history_co` b on trim(a.`lp_co_nm`) = trim(b.`lg_co_name`)) as tbl"
        all_matches =[]
        lp_co_dict = {}
        try:
            cursor.execute(map_lp_lg_sql)
            conn.commit()
            print("done!!!")
        except:
            traceback.print_exc()
            pass
        cursor.close()
        conn.close()

if __name__ == '__main__':
    c = MatchLgLpCoNames()
    c.map_lg_lp_coinfo() 
