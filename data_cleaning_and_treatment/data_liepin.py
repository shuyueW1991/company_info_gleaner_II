# -*- coding:utf-8 -*-
import pymysql
import traceback
import datetime
import requests
import json
import re

class data_clean_liepin(object):
    def __init__(self):
        self.to_word_api = 'http://218.244.132.122:8080/api/HanLpAPI/toWord'
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_master"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"

        self.liepin_fullname = 'nuh-uh'
        self.liepin_shortname = "nuh-uh"
        self.liepin_employee_size_floor = 'nuh-uh'
        self.liepin_employee_size_ceiling = 'nuh-uh'
        self.liepin_industry = 'nuh-uh'
        self.liepin_city = "nuh-uh"
        self.liepin_description = 'nuh-uh'
        self.liepin_avg_salary = 'nuh-uh'
        self.liepin_tot_positions = 'nuh-uh'
        self.liepin_website = "nuh-uh"


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


    def fetch_liepin_info(self):
        print("job is started...")
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                               passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.SSDictCursor)
        liepin_sql = "select fullname, address, industry, type, employee_size, tot_positions, avg_salary, city, province, region from data_co_info_lp"
        print("sql sentence is set-up...")

        try:
            cursor.execute(liepin_sql)
            print("cursor is executed...")
            item = cursor.fetchone()
            while item is not None:
                self.liepin_fullname = item["fullname"]
                self.liepin_address = item["address"]
                self.liepin_industry = item["industry"]
                self.liepin_type = item["type"]

                liepin_employee_size_floorceiling = item["employee_size"]
                (self.liepin_employee_size_floor, self.liepin_employee_size_ceiling) = self.floorceiling(liepin_employee_size_floorceiling)
                self.liepin_tot_positions = item["tot_positions"]
                self.liepin_avg_salary = item["avg_salary"]
                self.liepin_city = item["city"]
                self.liepin_province = item["province"]
                self.liepin_region = item["region"]

                self.insert_cleansed_liepin_info()
                print('this line is lit...')
                item = cursor.fetchone()

        except:
            traceback.print_exc()
            pass
        cursor.close()
        conn.close()


    def insert_cleansed_liepin_info(self):
        print('upload this line of company data ...')
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                               passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.SSDictCursor)
        data_liepin_sql = "insert into data2_co_info_lp(fullname, address, industry, type, employee_size_floor, employee_size_ceiling, tot_positions, avg_salary, city, province, region) values ('{0}','{1}','{2}', '{3}', '{4}','{5}','{6}','{7}', '{8}', '{9}','{10}')"
        try:
            cursor.execute(data_liepin_sql.format(self.liepin_fullname, self.liepin_address, self.liepin_industry, self. liepin_type, self.liepin_employee_size_floor, self.liepin_employee_size_ceiling, self.liepin_tot_positions, self.liepin_avg_salary, self.liepin_city, self.liepin_province, self.liepin_region))
            conn.commit()
        except:
            traceback.print_exc()
            pass

if __name__ == '__main__':
    w = data_clean_liepin()
    w.fetch_liepin_info()







