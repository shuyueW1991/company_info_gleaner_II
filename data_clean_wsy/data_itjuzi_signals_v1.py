import pandas as pd
import nltk
import jieba as jb
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import numpy as np

## 00. General Vars
now = "2017.5"

## 01.Master Data Creation
# def import_data():
#
#     # Read In Raw Data
#     input_file_1 = "/root/users/JH/data/itjuzi_hist_20170402.txt"
#     input_file_2 = "/root/users/JH/data/itjuzi_hist_20170401.txt"
#     input_file_3 = "/root/users/JH/data/itjuzi_hist_20170328.txt"
#
#     in_1 = pd.read_csv(input_file_1,sep="|",dtype={'it_co_views': str, 'it_co_followers': str}) #38150 rows
#     in_2 = pd.read_csv(input_file_2,sep="|",dtype={'it_co_views': str, 'it_co_followers': str}) #36137 rows
#     in_3 = pd.read_csv(input_file_3,sep="|",dtype={'it_co_views': str, 'it_co_followers': str}) #23513 rows
#
#     # Concatenate and Remove Duplicates
#     in_all = in_1.append(in_2)
#     in_all = in_all.append(in_3)
#     in_all = in_all.drop_duplicates(subset='it_co_id') #45210 rows
#
#     all_file = "/root/users/JH/data/itjuzi_hist_mst_20170429.txt"
#     in_all.to_csv(all_file, sep="|", index=False)

## 02.Signal Generation
# Read in Master Data
mst_file = "/root/users/JH/data/itjuzi_hist_mst_20170429.txt"
mst = pd.read_csv(mst_file, sep="|", dtype={'it_co_views': str, 'it_co_followers': str})

# Static Signals
# city
mst['it_city'] = mst['it_location'].str.split(" ").str.get(0)
# age
def age_gen(x):
    today = datetime.today()
    birth = datetime.strptime(x,'%Y.%m')
    age = relativedelta(today,birth).years
    return age
time = mst['it_estab_time'].str.replace(' ','').replace('2.02011.11','2011.11') #outlier removal
time = time.replace('',now) #treat missing values
mst['it_age'] = time.apply(age_gen)
print("age distribution")
print(mst['it_age'].value_counts())

# Financing Signals
# latest date
def find_date(x):
    dates = []
    if len(str(x))>0:
        l = re.findall('\d{4}\.\d+\.\d+', str(x))
        if len(l)>0:
            dates = []
            for i in l:
                try:
                    d = datetime.strptime(i,'%Y.%m.%d').date()
                    dates.append(d)
                except ValueError:
                    print(i)
    return dates

def date_max(x):
    if len(x)>0:
        latest = max(x)
    else:
        latest = ""
    return latest
mst['it_fin_dates'] = mst['it_investment_info'].apply(find_date)
mst['it_last_fin_date'] = mst['it_fin_dates'].apply(date_max)
# speed
def date_speed(x):
    if len(x)>0:
        todate = datetime.today()
        oldest = min(x)
        interval = max(relativedelta(todate, oldest).years, 1)
        speed = interval/len(x)
    else:
        speed = 0
    return speed
mst['it_fin_speed'] = mst['it_fin_dates'].apply(date_speed)

# latest round
def find_round(x):
    round = ['上市','收购','F', 'E', 'D', 'C', 'B+','B', 'Pre-B', 'A+', 'A', 'Pre-A', '天使', '种子']
    for i in round:
        latest = re.findall(i, str(x))
        if len(latest)>0:
            latest = latest[0]
            break
    return latest
mst['it_last_round'] = mst['it_investment_info'].apply(find_round)
# total amount

# News Report Signals
# total number of articles
mst['it_news_dates'] = mst['it_news'].apply(find_date)
mst['it_tot_news'] = mst['it_news_dates'].apply(lambda x: len(x))
# speed
mst['it_news_speed'] = mst['it_news_dates'].apply(date_speed)
# latest date
mst['it_last_news_date'] = mst['it_news_dates'].apply(date_max)

## 03.Output Signal File

out_file = "/root/users/JH/data/itjuzi_signal_20170501.txt"
mst.to_csv(out_file, sep="|", index=False)