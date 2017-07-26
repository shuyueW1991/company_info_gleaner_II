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
import sys
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# seg_list = jb.cut("我来到了美丽的复旦大学，太漂亮了啊。可是我还是喜欢上海外滩。正如我们知道的那样，上海自来水来自海上, shit.",cut_all=False)
# print("/".join(seg_list))


def jieba_cut(text):
    return " ".join(jb.cut(text, cut_all=False))

file_to_open = sys.argv[1]
file_to_write = sys.argv[2]
fw = open(file_to_write,"a", encoding='utf-8', errors='ignore')
with open(file_to_open, "r", encoding='utf-8', errors='ignore') as fp:
    for line in fp:
        fw.writelines(jieba_cut(line))

fw.close()



