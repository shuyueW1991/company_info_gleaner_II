import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import numpy as np
from datetime import *



readin_file = '/root/data/JData_Action_201604.csv'
rdin_file = pd.read_csv(readin_file, sep=",", dtype={'user_id': np.int64, 'time': str}, parse_dates=['time'])

filenamewithsuffix = readin_file.split('/')[-1]
filename =filenamewithsuffix.split('.')[0]

# start_time = datetime(2016, 4, 10, 23, 59, 59)
# time_length = timedelta(days=5)
# end_time = start_time + time_length

# 2016-04-15 23:59:59
# 2016-03-31 23:59:01

start_time = datetime(2016, 03, 31, 23, 59, 01)
end_time = datetime(2016, 4, 10,23, 59,59)

selected_data = rdin_file[(rdin_file['time']>start_time) & (rdin_file['time'] < end_time)]

out_file = "/root/users/WSY/" + filename + '_startfrom' + str(start_time) + '_endby' +str(end_time) + '.csv'
selected_data.to_csv(out_file, sep=",", index=False)

