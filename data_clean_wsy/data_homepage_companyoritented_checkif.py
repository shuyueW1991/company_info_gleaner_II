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


class data_checkif(object):
    def __init__(self):
        self.to_word_api = 'http://218.244.132.122:8080/api/HanLpAPI/toWord'
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"

    def checkif(self, text):
        flag = 0
        nom = ""
        list = ["全球各地","个国家","海外市场","全球领先","海内外","全球市场","国际贸易","海外集团","及海外","等国家","国内外","跨境","境内外"]
        for  i in list:
            if re.search(i,text):
                flag =1
                nom = i
                break

        flag = str(flag) + " " + nom
        return flag


    def fetch_insert_info(self):
        conn_fetch = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                                    passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor_fetch = conn_fetch.cursor(pymysql.cursors.SSDictCursor)

        print("job is started...")
        fetch_sql = "select host, content  from homepage_content_companyoritented"
        print(fetch_sql)
        try:
            cursor_fetch.execute(fetch_sql)
            print("cursor is executed...")
            item = cursor_fetch.fetchone()
            while item is not None:
                host = item["host"]
                try:
                    T_or_F_by_reSearch = self.checkif(item["content"])
                except:
                    traceback.print_exc()
                    T_or_F_by_reSearch = "erroroneous"
                    pass

                print("take the two things...")
                print('upload the two things ...')

                try:
                    conn_upload = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                                                 passwd=self.source_mysql_passwd, db=self.source_mysql_db,
                                                 charset='utf8')
                    cursor_upload = conn_upload.cursor(pymysql.cursors.SSDictCursor)
                    upload_language = "update homepage_content_companyoritented set T_or_F_by_reSearch = '" + str(T_or_F_by_reSearch) + "' where host = '" + str(host) + "' "
                    cursor_upload.execute(upload_language)
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

        print(' is finished checking...')

if __name__ == '__main__':
    w = data_checkif()
    w.fetch_insert_info()

    print('all tables are finished checkng...')
    # my = MyEmail()
    #
    # my.user = "henri.wang@wanxu.co"
    # my.passwd = "u8!7-ZXC"
    # my.to_list = ["han.jiang@wanxu.co","yang.yu@wanxu.co"]
    # my.cc_list = ["henri.wang@wanxu.co","benedict.qin@wanxu.co"]
    # my.tag = "automail: tables are finished checkifing..."
    # my.send()








