# -*- coding:utf-8 -*-
import pymysql
import traceback
import datetime
import requests
import json
import re

class data_clean_dajie(object):
    def __init__(self):
        self.to_word_api = 'http://218.244.132.122:8080/api/HanLpAPI/toWord'
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"

        self.dajie_fullname = 'nuh-uh'
        self.dajie_shortname = "nuh-uh"
        self.dajie_employee_size_floor = 'nuh-uh'
        self.dajie_employee_size_ceiling = 'nuh-uh'
        self.dajie_industry = 'nuh-uh'
        self.dajie_city = "nuh-uh"
        self.dajie_description = 'nuh-uh'
        self.dajie_avg_salary = 'nuh-uh'
        self.dajie_tot_positions = 'nuh-uh'
        self.dajie_website = "nuh-uh"


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

    def city_clean(self,string):
        if string.startswith("暂无"):
            string = "NaN"
        return string

    def website_clean(self, string):
        if string.startswith("暂无"):
            string = "NaN"
        return string


    def fetch_dajie_info(self):
        print("job is started...")
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                               passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.SSDictCursor)
        dajie_sql = "select co_name, co_add, co_type, co_number, co_web_add from dajie_co"
        print("sql sentence is set-up...")

        try:
            cursor.execute(dajie_sql)
            print("cursor is executed...")
            item = cursor.fetchone()
            while item is not None:
                self.dajie_fullname = item["co_name"].replace(" ","")
                dajie_city = item["co_add"].replace(" ","")
                self.dajie_city = self.city_clean(dajie_city)
                self.dajie_industry = item["co_type"].replace(" ","")
                dajie_employee_size_floorceiling = item["co_number"]
                (self.dajie_employee_size_floor, self.dajie_employee_size_ceiling) = self.floorceiling(dajie_employee_size_floorceiling)
                self.dajie_website = item["co_web_add"].replace(" ","")

                self.insert_cleansed_dajie_info()
                print('this line is lit...')
                item = cursor.fetchone()

        except:
            traceback.print_exc()
            pass
        cursor.close()
        conn.close()


    def insert_cleansed_dajie_info(self):
        print('upload this line of company data ...')
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                               passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.SSDictCursor)
        data_dajie_sql = "insert into data_dajie_co(fullname, city, industry, employee_size_floor, employee_size_ceiling, website) values ('{0}','{1}','{2}', '{3}', '{4}','{5}')"
        try:
            cursor.execute(data_dajie_sql.format(self.dajie_fullname, self.dajie_city, self.dajie_industry, self.dajie_employee_size_floor, self.dajie_employee_size_ceiling, self.dajie_website))
            conn.commit()
        except:
            traceback.print_exc()
            pass

if __name__ == '__main__':
    w = data_clean_dajie()
    w.fetch_dajie_info()







