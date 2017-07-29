import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import numpy as np
from datetime import *



readin_file = '/root/users/WSY/JData_Action_201604_startfrom2016-04-10 23:59:59_endby2016-04-15 23:59:59.csv'
rdin_file = pd.read_csv(readin_file, sep=",", dtype={'user_id': np.int64, 'time': str}, parse_dates=['time'])


selected = rdin_file[['user_id', 'type']]

selg = selected.groupby('user_id')['type'].apply(lambda x: 4 in x.tolist())
selg
print(type(selg))

selu = selected.groupby('user_id')['user_id'].first()
print(type(selu))

buyornot =  pd.DataFrame([selu, selg]).T
print(type(buyornot))
out_file = '/root/users/WSY/buyornot.csv'
buyornot.to_csv(out_file, sep=",", index=False)
