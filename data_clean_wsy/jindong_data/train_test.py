import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import numpy as np
from datetime import *



readin_file = '/root/users/WSY/buyornot.csv'
rdin_file = pd.read_csv(readin_file, sep=",")

train, test = np.split(rdin_file.sample(frac=1), [int(.7*len(rdin_file))])


out_file = '/root/users/WSY/train_user_buyornot.csv'
train.to_csv(out_file, sep=",", index=False)

out_file = '/root/users/WSY/test_user_buyornot.csv'
test.to_csv(out_file, sep=",", index=False)
