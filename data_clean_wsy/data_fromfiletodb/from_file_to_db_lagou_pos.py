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
myfile = open('lagou_history_pos_20170418.txt','r')
allWords = []
line = myfile.readline()
while line:
    list = line.split('|')
    for word in list:
        allWords.append(word.strip('\n'))
    print(len(allWords))
    sql = "insert into lagou_pos(lg_pos_id, lg_co_id, lg_co_name, lg_pos_name, lg_pos_type, lg_pos_tag, lg_pos_pay, lg_pos_location, lg_pos_experience, lg_pos_education, lg_pos_time, lg_pos_desc, lg_pos_update_time) values ('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}','{7}','{8}','{9}','{10}','{11}','{12}') on DUPLICATE KEY UPDATE lg_pos_id=values(lg_pos_id)"

    try:
        print("++++++++++++++++++++++++++++++++++++")
        cursor.execute(sql.format(allWords[0],allWords[1],allWords[2],allWords[3],allWords[4],allWords[5],allWords[6],allWords[7],allWords[8],allWords[9],allWords[10],allWords[11],allWords[12]))
        conn.commit()
    except:
        traceback.print_exc()


    allWords = []
    line = myfile.readline()
myfile.close()


