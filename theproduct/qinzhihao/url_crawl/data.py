import glob
import datetime
import pandas as pd
import codecs
import os
import shutil
import numpy
# from openpyxl.cell import ILLEGAL_CHARACTERS_RE


now = datetime.datetime.now().strftime("%Y%m%d")
# past = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
file = '/mnt/qinzhihao/url_crawl/company_info_for_selection_' + now + '.csv'
opener = codecs.open(file, "r",encoding='utf-8', errors='ignore')
sel = pd.read_csv(opener, sep="|")
url_file = '/mnt/qinzhihao/url_crawl/urlcrawler.txt'
url = pd.read_csv(url_file, sep='|')
url.columns = ['companyFullName','co_homepage','match_res']
sel = sel.merge(url, how='left', on='companyFullName')
url = sel[['co_homepage']]

os.remove(file)
sel.to_csv('company_info_for_selection_'+ now +'.csv',sep='|',index = False)
try:
    os.remove('/mnt/qinzhihao/url_crawl/old/urlcrawler.txt')
except:
    pass
shutil.move(url_file,'/mnt/qinzhihao/url_crawl/old/')
shutil.move('/mnt/qinzhihao/url_crawl/company_info_for_selection_'+ now +'.csv','/mnt/qinzhihao/url_crawl/old/')

# url['filter'] = url['co_homepage'].str.contains('shit',case = False)
# sel['highlight']=sel['positionName'].str.contains('海外分公司|海外办事处|海外代表|海外公司|海外国家|海外机构|海外分支机构|驻',case = False)

# url = url[url['filter']<1]
# url['filter'] = pd.isnull(url['co_homepage'])
# url = url[url['filter']<0]
url['co_homepage'].to_csv('url_list_short.txt',sep='|',index = False)

try:
    shutil.move('/mnt/qinzhihao/text_crawl/url_list_short.txt','/mnt/qinzhihao/text_crawl/old')
except:
    print('brand new')

shutil.move('/mnt/qinzhihao/url_crawl/url_list_short.txt','/mnt/qinzhihao/text_crawl')

