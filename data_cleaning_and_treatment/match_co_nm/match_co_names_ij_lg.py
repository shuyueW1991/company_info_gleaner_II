# -*- coding: utf-8 -*-

import pymysql
import traceback
import datetime
import requests
import json
import re

class MatchCoNames(object):
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
 
    def fetch_lg_ij_coinfo(self):
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user, passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
  #      lp_sql = "select lp_co_nm, lp_co_intro from lp_job_co_info"
        lg_sql = "select lg_co_name, lg_co_desc from lagou_history_co"
        ij_sql = "select it_short_name, it_full_name from ij_co_info_nonscrapy where it_co_id > 36610"
        all_matches =[]
        lg_co_dict = {}
        try:
            cursor.execute(lg_sql)
            lg_res = cursor.fetchall()
            for item in lg_res:
                lg_co_nm = item["lg_co_name"]
                lg_co_desc = item["lg_co_desc"]
                if lg_co_nm not in lg_co_dict.keys():
                    lg_co_dict[lg_co_nm]=lg_co_desc
            print("lg_co_dict: ", len(lg_co_dict))
            cursor.close()

            cursor = conn.cursor(pymysql.cursors.DictCursor)                 
            cursor.execute(ij_sql)
            ij_res = cursor.fetchall()
            print("ij_res: ", len(ij_res))
            for item in ij_res:
                it_short_names = item["it_short_name"].split(",") 
                it_full_name = item["it_full_name"]
                self.find_co_name_match(it_short_names,it_full_name,lg_co_dict, cursor, conn)
                #all_matches = self.find_co_name_match(it_short_names,it_full_name,lp_co_dict, all_matches)
            #print("all_matches: ", len(all_matches))
            #match_sql = "insert into co_names_mapping(it_full_name, it_short_names, lp_co_nm) values (%s,%s,%s)"
            #try:
            #    cursor.executemany(match_sql, all_matches)
            #    conn.commit()
            #except:
            #    traceback.print_exc()
            #    pass
            print("done!!!")
        except:
            traceback.print_exc()
            pass
        cursor.close()
        conn.close()

    #def find_co_name_match(self, it_short_names, it_full_name, lp_co_nm_info, all_matches):
    def find_co_name_match(self, it_short_names, it_full_name, lg_co_nm_info, cursor, conn):
        find_status = 0
        print("*************************************************")
        print("it_short_names: ", it_short_names , "; it_full_name: ", it_full_name)
        for it_short_name in it_short_names:
            if it_short_name.replace("+","").strip() != '':
                for lg_co_nm in lg_co_nm_info.keys():
                    lg_co_intro = lg_co_nm_info[lg_co_nm]
                    status = re.search(it_short_name.replace("+","").replace("（","(").replace("）",")").strip(), lg_co_intro)
                    if status != None:
                        #tmp = (it_full_name, ",".join(it_short_names), lp_co_nm)
                        #all_matches.append(tmp)
                        #match_sql = "insert into co_names_mapping(it_full_name, it_short_names, lp_co_nm) values (%s,%s,%s)"
                        match_sql = "insert into map_ij_lg_co_names(it_full_name, it_short_names, lg_co_nm) values ('{0}','{1}','{2}')"
                        try:
                            #cursor.executemany(match_sql, all_matches)
                            cursor.execute(match_sql.format(it_full_name, ",".join(it_short_names), lg_co_nm))
                            conn.commit()
                        except:
                            traceback.print_exc()
                            pass
                        print(it_full_name, " match ok !!")
                        find_status = 1
                        break
            print("find_status: ", find_status)
            if find_status == 1:
                break 
      #  return all_matches

if __name__ == '__main__':
    c = MatchCoNames()
    c.fetch_lg_ij_coinfo()
