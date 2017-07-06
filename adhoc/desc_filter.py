import pandas as pd
import pymysql
import codecs
import traceback

class db_conn(object):
    def __init__(self):
        # upload to database ...
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"
        self.conn = pymysql.connect(host=self.source_mysql_host,
                                    user=self.source_mysql_user,
                                    passwd=self.source_mysql_passwd,
                                    db=self.source_mysql_db,
                                    charset='utf8')
        self.cursor = self.conn.cursor(pymysql.cursors.Cursor)


    def void_to_NaN(self,content):
        if len(content) > 0:
            return content
        else:
            content = "NaN"
            return content

    def employee_size(self):
        return None


    def process_item(self, item, spider):
        # sql = "insert into kanzhun_co_init(co_short_nm, co_type, co_city, co_staff_num, co_short_desc, co_goodcommnt_rateco_avg_pay_emply_num) values ('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}','{7}', '{8}')"
        sql = "SELECT * FROM 'bosszp_co'"
        self.cursor.execute(sql)
        self.conn.commit()
        result = self.cursor.fetchone()
        print('the result is {}'.format(result))
        self.conn.close()


        # try:
        #     if len(item['co_short_nm']) > 0:
        #         print("++++++++++++++++++++++++++++++++++++")
        #         print(type(item['co_avg_pay_emply_num']))
        #         print(len(item['co_avg_pay_emply_num']))
        #
        #         for k,v in item.items():
        #             if len(v) == 0:
        #                 v = 'NaN'
        #         print('checked.okay.')
        #
        #
        #         self.cursor.execute(sql.format(item['co_short_nm'],
        #                                        item['co_type'],
        #                                        item['co_city'],
        #                                        item['co_staff_num'],
        #                                        item['co_short_desc'],
        #                                        item['co_goodcommnt_rate'],
        #                                        item['co_goodcommnt_rate_emply_num'],
        #                                        item['co_avg_pay'][:],
        #                                        item['co_avg_pay_emply_num']))
        #         self.conn.commit()
        #         result = self.cursor.fetchone()
        #         print('the result is {}'.format(result))
        #         return item
        #     else:
        #         pass
        #
        # except:
        #     traceback.print_exc()
        #     pass

if __name__ == "__main__":
    db_conn().process_item()


