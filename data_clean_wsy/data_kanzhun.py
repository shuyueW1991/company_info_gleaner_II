# -*- coding:utf-8 -*-
import pymysql
import traceback
import datetime
import requests
import json
import re

class data_clean_kanzhun(object):
    def __init__(self):
        self.to_word_api = 'http://218.244.132.122:8080/api/HanLpAPI/toWord'
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"

        self.kanzhun_fullname = 'nuh-uh'
        self.kanzhun_shortname = "nuh-uh"
        self.kanzhun_employee_size_floor = 'nuh-uh'
        self.kanzhun_employee_size_ceiling = 'nuh-uh'
        self.kanzhun_industry = 'nuh-uh'
        self.kanzhun_city = "nuh-uh"
        self.kanzhun_description = 'nuh-uh'
        self.kanzhun_avg_salary = 'nuh-uh'
        self.kanzhun_tot_positions = 'nuh-uh'


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
                ceiling = lala[1].rstrip("人")
            elif string.endswith("以上"):
                floor = string.rstrip("人以上")
                ceiling = 'Inf'
            else:
                floor = "NaN"
                ceiling = "NaN"

            return (floor, ceiling)
        except:
            traceback.print_exc()
            pass

    def desc_clean(self, string):
        if string.startswith("这个公司比较低调，没有什么介绍"):
            string = "NaN"
        return string

    def fetch_kanzhun_info(self):
        print("job is started...")
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                               passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.SSDictCursor)
        kanzhun_sql = "select co_short_nm,  co_type, co_city, co_staff_num, co_short_desc, co_avg_pay, co_avg_pay_emply_num from kanzhun_co_init"
        print("sql sentence is set-up...")

        try:
            cursor.execute(kanzhun_sql)
            print("cursor is executed...")
            item = cursor.fetchone()
            while item is not None:
                self.kanzhun_shortname = item["co_short_nm"].replace(" ","")
                self.kanzhun_industry = item["co_type"].replace(" ","")
                self.kanzhun_city = item["co_city"].replace(" ","")
                kanzhun_employee_size_floorceiling = item["co_staff_num"]
                (self.kanzhun_employee_size_floor, self.kanzhun_employee_size_ceiling) = self.floorceiling(kanzhun_employee_size_floorceiling)
                kanzhun_description = item["co_short_desc"].replace(" ","")
                self.kanzhun_description = self.desc_clean(kanzhun_description)
                self.kanzhun_avg_salary = item["co_avg_pay"].replace(" ","")
                self.kanzhun_tot_positions = item["co_avg_pay_emply_num"].replace(" ","")

                self.insert_cleansed_kanzhun_info()
                print('this line is lit...')
                item = cursor.fetchone()

        except:
            traceback.print_exc()
            pass
        cursor.close()
        conn.close()


    def insert_cleansed_kanzhun_info(self):
        print('upload this line of company data ...')
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                               passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.SSDictCursor)
        data_kanzhun_sql = "insert into data_kanzhun_co_init(shortname, industry, city, employee_size_floor, employee_size_ceiling, description, avg_salary, tot_positions) values ('{0}','{1}','{2}', '{3}', '{4}','{5}','{6}','{7}')"
        try:
            cursor.execute(data_kanzhun_sql.format(self.kanzhun_shortname, self.kanzhun_industry, self.kanzhun_city, self.kanzhun_employee_size_floor, self.kanzhun_employee_size_ceiling, self.kanzhun_description, self.kanzhun_avg_salary, self.kanzhun_tot_positions))
            conn.commit()
        except:
            traceback.print_exc()
            pass

if __name__ == '__main__':
    w = data_clean_kanzhun()
    w.fetch_kanzhun_info()







