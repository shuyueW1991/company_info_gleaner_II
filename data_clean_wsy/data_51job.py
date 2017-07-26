# -*- coding:utf-8 -*-
import pymysql
import traceback
import datetime
import requests
import json
import re

class data_clean_51job(object):
    def __init__(self):
        self.to_word_api = 'http://218.244.132.122:8080/api/HanLpAPI/toWord'
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"

        self.wuyaojob_fullname = 'nuh-uh'
        self.wuyaojob_employee_size_floor = 'nuh-uh'
        self.wuyaojob_employee_size_ceiling = 'nuh-uh'
        self.wuyaojob_industry = 'nuh-uh'
        self.wuyaojob_description = 'nuh-uh'
        self.wuyaojob_address = 'nuh-uh'


    def floorceiling(self, string):
        try:
            if string.startswith("少于"):
                floor = 0
                ceiling = string.lstrip("少于").rstrip("人")
            elif len(string.split('-')) > 1:
                lala = string.split('-')
                print('lala:')
                print(lala)
                print(type(lala))
                floor = lala[0]
                ceiling = lala[1]
            else:
                floor = 'NaN'
                ceiling = 'NaN'

            return (floor, ceiling.rstrip("人"))
        except:
            traceback.print_exc()
            pass

    def fetch_51job_info(self):
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                               passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        wuyaojob_sql = "select co_nm, co_staff_num, co_type, co_short_desc, co_add from wuyaojob_co"

        try:
            cursor.execute(wuyaojob_sql)
            # wuyaojob_res = cursor.fetchall()
            # for item in wuyaojob_res:
            #     self.wuyaojob_fullname = item("co_nm").replace(" ","")
            #     wuyaojob_employee_size_floorceiling = item("co_staff_num")
            #     self.wuyaojob_employee_size_floorceiling = self.floorceiling(wuyaojob_employee_size_floorceiling)
            #     self.wuyaojob_industry = item("co_type").strip('<label class="at">')
            #     self.wuyaojob_description = item("co_short_desc").replace(" ","")
            #     self.wuyaojob_address = item("co_add").replace(" ","")
            #
            #     self.insert_cleansed_51job_info()
            #     print('this line is lit...')

            item = cursor.fetchone()
            while item is not None:
                self.wuyaojob_fullname = item["co_nm"].replace(" ","")
                wuyaojob_employee_size_floorceiling = item["co_staff_num"]
                (self.wuyaojob_employee_size_floor, self.wuyaojob_employee_size_ceiling) = self.floorceiling(wuyaojob_employee_size_floorceiling)
                self.wuyaojob_industry = item["co_type"].strip('<label class="at">')
                self.wuyaojob_description = item["co_short_desc"].replace(" ","")
                self.wuyaojob_address = item["co_add"].replace(" ","")

                self.insert_cleansed_51job_info()
                print('this line is lit...')
                item = cursor.fetchone()

        except:
            traceback.print_exc()
            pass
        cursor.close()
        conn.close()


    def insert_cleansed_51job_info(self):
        print('upload this line of company data ...')
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                               passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        data_51job_sql = "insert into data_wuyaojob_co(fullname, employee_size_floor, employee_size_ceiling, industry, description, address) values ('{0}','{1}','{2}', '{3}', '{4}','{5}')"
        try:
            cursor.execute(data_51job_sql.format(self.wuyaojob_fullname, self.wuyaojob_employee_size_floor, self.wuyaojob_employee_size_ceiling, self.wuyaojob_industry, self.wuyaojob_description, self.wuyaojob_address))
            conn.commit()
        except:
            traceback.print_exc()
            pass

if __name__ == '__main__':
    w = data_clean_51job()
    w.fetch_51job_info()







