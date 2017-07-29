import pandas as pd

# master data generation

readin_file1 = '/root/data/JData_Action_201602.csv'
rdin_file1 = pd.read_csv(readin_file1, sep=",", dtype={'user_id': np.int64, 'time': str}, parse_dates=['time'])

readin_file2 = '/root/data/JData_Action_201603.csv'
rdin_file2 = pd.read_csv(readin_file2, sep=",", dtype={'user_id': np.int64, 'time': str}, parse_dates=['time'])

readin_file3 = '/root/users/WSY/JData_Action_201604_startfrom2016-03-31 23:59:01_endby2016-04-10 23:59:59.csv'
rdin_file3 = pd.read_csv(readin_file3, sep=",", dtype={'user_id': np.int64, 'time': str}, parse_dates=['time'])

# moving window indicator

# rd_all_train =
#
# rd_all_test =





# train_material.groupby('user_id')['']

# group by user_id and moving window indicator


# result output