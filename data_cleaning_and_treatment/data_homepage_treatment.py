# -*- coding:utf-8 -*-
import pymysql
import traceback
import datetime
import requests
import json
import re
import jieba as jb
from gensim import corpora, models, similarities
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class data_treatment(object):
    def __init__(self):
        self.to_word_api = 'http://218.244.132.122:8080/api/HanLpAPI/toWord'
        self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
        self.source_mysql_db = "buz_source_data"
        self.source_mysql_user = "root"
        self.source_mysql_passwd = "u8!7-ZXC"

    def jieba_cut(self, text):
        return " ".join(jb.cut(text, cut_all=False))

    def fetch_append_info(self):
        conn_fetch = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
                                    passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
        cursor_fetch = conn_fetch.cursor(pymysql.cursors.SSDictCursor)

        doc_list_T = []
        doc_list_F = []
        fetch_sql = "select * from homepage_content "
        try:
            cursor_fetch.execute(fetch_sql)
            item = cursor_fetch.fetchone()
            while item is not None:
                id = item["id"]
                doc = self.jieba_cut(item["content"])
                # print(type(doc))
                # print(doc)
                if str(item["T_or_F"]).startswith("0"):
                    doc_list_F.append(doc)
                else:
                    doc_list_T.append(doc)
                print("take the web content...")

                item = cursor_fetch.fetchone()
        except:
            traceback.print_exc()
            pass
        print('the fetch is done.')
        # conn_fetch.close()
        # cursor_fetch.close()
        print(len(doc_list_T))
        print(len(doc_list_F))

        len_t = len(doc_list_T)
        doc_list_T.extend(doc_list_F)
        doc_list = doc_list_T
        print(doc_list[0:4])

        texts = [[word for word in document.split()] for document in doc_list]

        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        tfidf = models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]

        for doc_ in corpus_tfidf[-2:-1]:
            print(doc_)

        lsi = models.LsiModel(corpus_tfidf[0:len_t - 1], id2word=dictionary, num_topics=2) # note:here the id's for positive doc is required. Also the number of topics is also required.
        lsi.print_topics(2)
        corpus_lsi = lsi[corpus_tfidf]
        index = similarities.MatrixSimilarity(lsi[corpus])

        query = self.jieba_cut("我想要找海外国际贸易，最好有和国内外有关系。")
        print(query)
        query_bow = dictionary.doc2bow(query.split())
        print(query_bow)
        query_lsi = lsi[query_bow]
        # print(query_lsi)
        sims = index[query_lsi]
        # print(list(enumerate(sims)))
        sort_sims = sorted(enumerate(sims), key=lambda item: -item[1])
        print(sort_sims)
#



if __name__ == '__main__':
    w = data_treatment()
    w.fetch_append_info()

    print('done...')
    # my = MyEmail()
    #
    # my.user = "henri.wang@wanxu.co"
    # my.passwd = "u8!7-ZXC"
    # my.to_list = ["han.jiang@wanxu.co","yang.yu@wanxu.co"]
    # my.cc_list = ["henri.wang@wanxu.co","benedict.qin@wanxu.co"]
    # my.tag = "automail: tables are finished checkifing..."
    # my.send()
