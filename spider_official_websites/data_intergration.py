import re
import pandas as pd
import pickle
import json
import csv
url_list = "/root/users/JH/company_info_gleaner_II/spider_official_websites/crawler_20170701.txt"

# out_file = "/root/users/JH/company_info_gleaner_II/spider_official_websites/urL_with_contact_20170629_1.txt"
# df_in = pd.read_csv(url_list, sep="|")
# df_out = df_in.drop_duplicates(['host_url','email','mobile'])
# df_out = df_out[['host_url','email','mobile']]
# df_out.to_csv(out_file,sep="|",index=False)

dict = {}

for line in open(url_list,'r',encoding='utf8'):
    data = line.split("|")
    host = data[0]
    email = data[2]
    lll=[]
    lll.insert(0, email)
    print('host and email is {} {}'.format(host,lll))
    try:
        dict[host].update(lll)
    except:
        dict[host] = set(lll)

print('the dict is {}'.format(dict))

# with open('urL_with_contact_20170629_1.txt', 'wb') as handle:
#     pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open('urL_with_contact_20170629_1.txt', 'w') as file:
#     file.write(json.dumps(dict))

with open('/root/users/JH/company_info_gleaner_II/spider_official_websites/urL_with_contact_20170701_1.csv', 'wt') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in dict.items():
       writer.writerow([key, value])









