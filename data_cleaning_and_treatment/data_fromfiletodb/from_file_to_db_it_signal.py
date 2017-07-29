# -*- coding:utf-8 -*-
import pymysql
import traceback
import datetime

#PREPARE CONNECTION WITH DATABASE UP THERE IN CLOUD
source_mysql_host="rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
source_mysql_db="buz_source_data"
source_mysql_user="root"
source_mysql_passwd="u8!7-ZXC"
conn = pymysql.connect(host=source_mysql_host, user=source_mysql_user, passwd=source_mysql_passwd, db=source_mysql_db, charset='utf8')
cursor = conn.cursor(pymysql.cursors.DictCursor)


# READ FILE & SEND THE DATA TO CLOUD
myfile = open('/root/users/JH/data/itjuzi_signal_20170501.txt','r')
allWords = []
line = myfile.readline()
while line:
    list = line.split('|')
    for word in list:
        allWords.append(word.strip('\n'))
    print(len(allWords))
    sql = "insert into ij_signals(it_co_id, it_short_name, it_full_name, it_short_desc, it_full_desc, it_desc_tag, it_ind_tag, it_location, it_website, it_estab_time, it_ee_size, it_active_status, it_investment_info, it_mgmt_name, it_mgmt_desc, it_prd_info, it_news, it_milestone, it_co_views, it_co_followers, it_update_time, it_city, it_age, it_fin_dates, it_last_fin_date, it_fin_speed, it_last_round, it_news_dates, it_tot_news, it_news_speed, it_last_news_date) values ('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}','{17}','{18}','{19}',{20},'{21}','{22}','{23}','{24}','{25}','{26}','{27}','{28}','{29}','{30}') on DUPLICATE KEY UPDATE it_co_id=values(it_co_id)"

    try:
        print("++++++++++++++++++++++++++++++++++++")
        cursor.execute(sql.format(allWords[0],allWords[1],allWords[2],allWords[3],allWords[4],allWords[5],allWords[6],allWords[7],allWords[8],allWords[9],allWords[10],allWords[11],allWords[12],allWords[13],allWords[14],allWords[15],allWords[16],allWords[17],allWords[18],allWords[19],allWords[20],allWords[21],allWords[22],allWords[23],allWords[24],allWords[25],allWords[26],allWords[27],allWords[28],allWords[29],allWords[30]))
        conn.commit()
    except:
        traceback.print_exc()


    allWords = []
    line = myfile.readline()
myfile.close()

