# -*- coding: utf-8 -*-

import pymysql
import traceback
import datetime
import requests
import json
import re

class baiduMatchCoNames(object):
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
 
    def baidufetch_lp_ij_coinfo(self):
        conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user, passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
  #      lp_sql = "select lp_co_nm, lp_co_intro from lp_job_co_info"
        baidulp_sql = "select lp_co_nm, lp_co_bd from new_lp_co_nm_bd"
        baiduit_sql = "select it_co_nm from new_it_co_nm_bd"
        all_matches =[]
        lp_co_dict = {}
        try:
            cursor.execute(baidulp_sql)
            lp_res = cursor.fetchall()
            for item in lp_res:
                lp_co_nm = item["lp_co_nm"]
                lp_co_bd = item["lp_co_bd"]
                if lp_co_nm not in lp_co_dict.keys():
                    lp_co_dict[lp_co_nm]=lp_co_bd
            print("lp_co_dict: ", len(lp_co_dict))
            cursor.close()

            cursor = conn.cursor(pymysql.cursors.DictCursor)                 
            cursor.execute(baiduit_sql)
            ij_res = cursor.fetchall()
            print("ij_res: ", len(ij_res))
            for item in ij_res:
                # it_short_names = item["it_short_name"].split(",")
                it_full_name = item["it_co_nm"]
                self.find_co_name_match(it_full_name,lp_co_dict, cursor, conn)
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
    def find_co_name_match(self, it_full_name, lp_co_nm_info, cursor, conn):
        find_status = 0
        print("*************************************************")
        print("it_full_name: ", it_full_name)
        if it_full_name.replace("+","").strip() != '':
            for lp_co_nm in lp_co_nm_info.keys():
                lp_co_intro = lp_co_nm_info[lp_co_nm]
                #status = re.search(it_full_name.replace("+","").replace("（","(").replace("）",")").strip(), lg_co_intro)
                status = len(re.findall(it_full_name, lp_co_intro))

                if status >= 3:
                    #tmp = (it_full_name, ",".join(it_short_names), lp_co_nm)
                    #all_matches.append(tmp)
                    #match_sql = "insert into co_names_mapping(it_full_name, it_short_names, lp_co_nm) values (%s,%s,%s)"
                    match_sql = "insert into new_baidumap_ij_lp_co_names(it_full_name, lp_co_nm) values ('{0}','{1}')"
                    try:
                        #cursor.executemany(match_sql, all_matches)
                        cursor.execute(match_sql.format(it_full_name, lp_co_nm))
                        conn.commit()
                    except:
                        traceback.print_exc()
                        pass
                    print(it_full_name, " match ok !!")
                    find_status = 1
                    break
        print("find_status: ", find_status)
        # if find_status == 1:
        #     break
      #  return all_matches

if __name__ == '__main__':
    c = baiduMatchCoNames()
    c.baidufetch_lp_ij_coinfo()
