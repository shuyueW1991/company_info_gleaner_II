import glob
import datetime
import pandas as pd
import codecs
import os
import shutil
# from openpyxl.cell import ILLEGAL_CHARACTERS_RE


now = datetime.datetime.now().strftime("%Y%m%d")
past = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y%m%d")
list = glob.glob('*.csv')
sel = pd.DataFrame()

for file in list:

    opener = codecs.open(file, "r",encoding='utf-8', errors='ignore')
    buffer = pd.read_csv(opener,sep="|")
    # print(buffer['co_link'])
    if 'financeStage' in buffer.columns:
        if 'co_link' in buffer.columns:
            buffer = buffer[['companyFullName', 'companySize', 'industryField', 'financeStage', 'positionName', 'salary','description','co_link']]
        else:
            buffer = buffer[['companyFullName', 'companySize', 'industryField', 'financeStage', 'positionName', 'salary','description']]
    else:
        buffer = buffer[['companyFullName', 'companySize', 'industryField', 'positionName', 'salary', 'description']]

    sel = sel.append(buffer)
    shutil.move('/mnt/qinzhihao/Data/' + file, '/mnt/qinzhihao/Data/old/')

# 做DataFrame过滤旧公司，并update
db = pd.read_csv("/mnt/qinzhihao/Data/old/company_info_db.csv",sep="|")
fold = db.rename(columns={'companyFullName':'companyFullName','companySize':'filter_old'})
db = db.append(sel[['companyFullName', 'companySize']])
db = db.drop_duplicates(['companyFullName'])
# os.remove('/mnt/qinzhihao/Data/old/company_info_db.csv')
db.to_csv('/mnt/qinzhihao/Data/old/company_info_db'+now+'.csv',sep='|',index = False)


sel = pd.merge(sel,fold, how='left', on='companyFullName')
sel['filter_old'] = pd.isnull(sel['filter_old'])
sel['highlight']=sel['positionName'].str.contains('海外分公司|海外办事处|海外代表|海外公司|海外国家|海外机构|海外分支机构|驻',case = False)
sel['filter_oversea'] = sel['positionName'].str.contains('海外|国外|驻外',case = False)
sel['filter_job'] = sel['positionName'].str.contains('跟单|编辑|买手|采购|推广|广告投放|海外背景|房产|运营|清关|移民|置业|理财|招商|创业|老师|教师|培训|护士|厨师|保险|不动产|海外包|猎头|上海外|珠海外|facebook|亚马逊|SNS|SEO|google|SEM|链家链家|海底捞',case = False)
sel = sel[(sel['filter_old']>0)]

# print(good_job)
all_job = sel.groupby('companyFullName').size().to_frame().reset_index()
all_job.columns = ['companyFullName','all_job']
# print(sel['filter_oversea'])
oversea_job = sel[sel['filter_job']>0].groupby('companyFullName').size().to_frame().reset_index()
oversea_job.columns = ['companyFullName','oversea_job']
# print(sel['filter_job'])
good_job = sel[sel['filter_job']<1].groupby('companyFullName').size().to_frame().reset_index()
good_job.columns = ['companyFullName','good_job']
# print(sel['highlight']>0)
highlight = sel[sel['highlight']>0].groupby('companyFullName').size().to_frame().reset_index()
highlight.columns = ['companyFullName','highlight']
# print(all_job)
des = sel[sel['filter_job']<1].drop_duplicates(['companyFullName'])[['companyFullName','description']]
pos = sel[sel['filter_job']<1].drop_duplicates(['compangFullName'])[['companyFullName','positionName']]

co_info = sel.drop_duplicates(['companyFullName'])[['companyFullName','companySize','industryField','financeStage','co_link']]
co_info = co_info.merge(des,how='left', on='companyFullName').merge(pos,how='left', on='companyFullName').merge(oversea_job,how='left', on='companyFullName').merge(good_job,how='left', on='companyFullName').merge(highlight,how='left', on='companyFullName').merge(all_job,how='left', on='companyFullName')

# sel= ILLEGAL_CHARACTERS_RE.sub(r'', sel)
# writer = pd.ExcelWriter('company_info_for_selection_'+ date +'.xlsx')
# sel.to_excel(writer, sheet_name='data_new', index=False)
# writer.save()
# sel.to_csv('company_info_for_selection.csv',sep='|',index = False)
# sel = pd.read_csv('/mnt/qinzhihao/Data/company_info_for_selection.csv', sep="|")

# sel = sel.drop_duplicates("companyFullName")
co_info.to_csv('company_info_for_selection_'+ now +'.csv',sep='|',index = False)
shutil.move('/mnt/qinzhihao/Data/company_info_for_selection_'+ now +'.csv','/mnt/qinzhihao/Data/old/')



