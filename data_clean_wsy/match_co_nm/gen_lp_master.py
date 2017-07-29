# -*- coding: utf-8 -*-
import pymysql
import traceback
import datetime
import requests
import json
import re

class GenLpMaster(object):
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
 
    def fetch_lp_co_job_coinfo(self):
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user, passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        lp_sql = "select lp_co_nm, lp_co_tag, lp_co_addr, lp_co_ownership, lp_co_stf_num from lp_info_co_part limit 100"
        job_sql = "select lp_co_nm, lp_job_nm, lp_job_salary from lp_info_job_part limit 100"
        all_matches =[]
        lp_co_dict = {}
        lp_job_dict = {}
        try:
            cursor.execute(job_sql)
            lp_job_res = cursor.fetchall()
            for item in lp_job_res:
                lp_co_nm = item["lp_co_nm"].strip()
                lp_job_nm = item["lp_job_nm"]
                lp_job_salary = item["lp_job_salary"]
                if lp_co_nm not in lp_co_dict.keys():
                    lp_co_dict[lp_co_nm]=[[lp_job_nm],[lp_job_salary]]
                else:
                    lp_co_dict[lp_co_nm][0].append(lp_job_nm) 
                    lp_co_dict[lp_co_nm][1].append(lp_job_salary) 
            cursor.close()

            lp_job_result = {}
            for key in lp_co_dict.keys():
                pos_num = len(lp_co_dict[key][0]) 
                salary_all = 0
                pos_salary_num = 0
                for item in lp_co_dict[key][1]:
                    print(item)
                    if item != "" and item != "面议":
                        item_str = item.replace("万", "").split("-")
                        medium =  (int(item_str[0]) + int(item_str[1])) * 10000/2 
                        salary_all = salary_all + medium
                        pos_salary_num = pos_salary_num + 1
                    lp_job_result[key]=[pos_num, salary_all, pos_salary_num] 
            cursor = conn.cursor(pymysql.cursors.DictCursor)                 
            cursor.execute(lp_sql)
            lp_co_res = cursor.fetchall()
            print("lp_co_res: ", len(lp_co_res))
            for item in lp_co_res:
                lp_co_nm = item["lp_co_nm"].strip()
                lp_co_tag = " ".join(item["lp_co_tag"].split("/"))
                lp_co_addr = item["lp_co_addr"]
                lp_co_ownership = item["lp_co_ownership"]
                lp_co_stf_num = item["lp_co_stf_num"]
                if lp_co_nm in lp_job_result.keys():
                    lp_job_pos_num = lp_job_result[lp_co_nm][0]
                    salary_all = lp_job_result[lp_co_nm][1]
                    pos_salary_num = lp_job_result[lp_co_nm][2]
                    if pos_salary_num > 0:
                        lp_pos_avg_salary = salary_all/pos_salary_num
                    else :
                        lp_pos_avg_salary = '面议'
                    update_sql = "insert into master_co_info_lp(lp_co_nm,lp_co_addr,lp_co_tag,lp_co_ownership,lp_co_stf_num,lp_job_pos_num,lp_pos_avg_salary) values (%s,%s,%s,%s,%s,%s,%s)"
                    try:
                        cursor.execute(update_sql.format(lp_co_nm,lp_co_addr,lp_co_tag,lp_co_ownership,lp_co_stf_num,lp_job_pos_num,lp_pos_avg_salary))
                        conn.commit()
                    except:
                        traceback.print_exc()
                        pass
                    print(lp_co_nm,lp_co_addr,lp_co_tag,lp_co_ownership,lp_co_stf_num,lp_job_pos_num,lp_pos_avg_salary)
            print("done!!!")
        except:
            traceback.print_exc()
            pass
        cursor.close()
        conn.close()

if __name__ == '__main__':
    c = GenLpMaster()
    c.fetch_lp_co_job_coinfo() 
