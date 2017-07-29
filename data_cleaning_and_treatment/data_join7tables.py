# -*- coding:utf-8 -*-
import pymysql
import traceback
import datetime
import requests
import json
import re

import email
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class MyEmail:
    def __init__(self):
        self.user = None
        self.passwd = None
        self.to_list = []
        self.cc_list = []
        self.tag = None
        self.doc = None

    def send(self):
        '''
        发送邮件
        '''
        try:
            server = smtplib.SMTP_SSL("smtp.exmail.qq.com",port=465)
            server.login(self.user,self.passwd)
            server.sendmail("<%s>"%self.user, self.to_list, self.get_attach())
            server.close()
            print("send email successful")
        except:
            traceback.print_exc()
            pass


    def get_attach(self):
        '''
        构造邮件内容
        '''
        attach = MIMEMultipart()
        if self.tag is not None:
            #主题,最上面的一行
            attach["Subject"] = self.tag
        if self.user is not None:
            #显示在发件人
            attach["From"] = "hw<%s>"%self.user
        if self.to_list:
            #收件人列表
            attach["To"] = ";".join(self.to_list)
        if self.cc_list:
            #抄送列表
            attach["Cc"] = ";".join(self.cc_list)
        if self.doc:
            #估计任何文件都可以用base64，比如rar等
            #文件名汉字用gbk编码代替
            name = os.path.basename(self.doc).encode("gbk")
            f = open(self.doc,"rb")
            doc = MIMEText(f.read(), "base64", "gb2312")
            doc["Content-Type"] = 'application/octet-stream'
            doc["Content-Disposition"] = 'attachment; filename="'+name+'"'
            attach.attach(doc)
            f.close()
        return attach.as_string()


class data_join_seven(object):
    def __init__(self):
        self.to_word_api = 'http://218.244.132.122:8080/api/HanLpAPI/toWord'
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"

        self.fullname = 'nuh-uh'
        self.shortname = "nuh-uh"
        self.city = "nuh-uh"
        self.industry = 'nuh-uh'
        self.type = 'nuh-uh'
        self.address = 'nuh-uh'
        self.description = 'nuh-uh'
        self.employee_size_floor = 'nuh-uh'
        self.employee_size_ceiling = 'nuh-uh'
        self.website = "nuh-uh"
        self.finance_round = "nuh-uh"
        self.tot_positions = 'nuh-uh'
        self.avg_salary = 'nuh-uh'
        self.province = 'nuh-uh'
        self.region = 'nuh-uh'


    def fetch_insert_info(self, tablename):
        conn_fetch = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                                    passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor_fetch = conn_fetch.cursor(pymysql.cursors.SSDictCursor)

        print("job is started...")
        fetch_sql = "select * from " + tablename
        print(fetch_sql)
        try:
            cursor_fetch.execute(fetch_sql)
            print("cursor is executed...")
            item = cursor_fetch.fetchone()
            while item is not None:
                upload_sql = "insert into" + " bigdata_sept_tables("
                value_sql = " values ("
                fullname_flag = 0
                for k,v in item.items():
                    print(k)
                    if k == 'fullname':
                        fullname_flag = 1
                    if k == 'shortname':
                        shortname = v
                    upload_sql = upload_sql + k + ", "
                    print(v)
                    value_sql = value_sql + " '" + str(v) + "' ,"

                upload_sql = upload_sql.rstrip(", ")
                if fullname_flag == 0:
                    upload_sql = upload_sql + ", fullname"
                upload_sql = upload_sql + ")"

                value_sql = value_sql.rstrip(",")
                if fullname_flag == 0:
                    value_sql = value_sql + ", " + "'" + str(shortname) + "'"
                value_sql = value_sql + ")"
                upload_sql = upload_sql + value_sql + " on duplicate key update fullname=fullname ;"
                print(upload_sql)
                print('upload this line of company data ...')
                # self.conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                #                             passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
                # self.cursor = self.conn.cursor(pymysql.cursors.SSDictCursor)

                try:
                    conn_upload = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                                                 passwd=self.source_mysql_passwd, db=self.source_mysql_db,
                                                 charset='utf8')
                    cursor_upload = conn_upload.cursor(pymysql.cursors.SSDictCursor)
                    cursor_upload.execute(upload_sql)
                    conn_upload.commit()
                except:
                    traceback.print_exc()
                    pass
                print("this line is lit...")
                item = cursor_fetch.fetchone()

        except:
            traceback.print_exc()
            pass
        # conn_upload.close()
        conn_fetch.close()
        cursor_fetch.close()
        # cursor_upload.close()
        print('the table of ')
        print(tablename)
        print(' is finished uploading...')

if __name__ == '__main__':
    w = data_join_seven()
    # w.fetch_insert_info('data_chinahr_co')
    w.fetch_insert_info('data_bosszp_co')
    w.fetch_insert_info('data_dajie_co')
    w.fetch_insert_info('data_kanzhun_co')
    w.fetch_insert_info('data_lagou_co')
    w.fetch_insert_info('data_lp_co')
    w.fetch_insert_info('data_wuyaojob_co')

    print('all tables are finished uploading...')
    my = MyEmail()

    my.user = "henri.wang@wanxu.co"
    my.passwd = "u8!7-ZXC"
    my.to_list = ["han.jiang@wanxu.co","yang.yu@wanxu.co"]
    my.cc_list = ["henri.wang@wanxu.co","benedict.qin@wanxu.co"]
    my.tag = "automail: seven tables are finished uploading..."
    # my.doc = "/Users/yuyang/notreProgram/my/data_clean_wsy"
    my.send()








