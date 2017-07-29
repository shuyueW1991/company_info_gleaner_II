# -*- coding: utf-8 -*-
import sys
import os
import time
import signal
#note, this script is run under python3
# reload(sys)
# sys.setdefaultencoding('utf-8')

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

signal.signal(signal.SIGALRM, timeout_handler)

def main():
    with open('sample.csv', 'r') as the_file:
        content = the_file.readlines()
        # print(content[2])
        # print(type(content[0]))

    for i in content:
        print(i)
        cmdstr = 'python geetest_better_gsxt_selenium.py ' + i
        os.system(cmdstr)
        time.sleep(0.3)
    #

    # for i in content:
    #     print(i)
    #     signal.alarm(5)
    #     try:
    #         cmdstr = 'python geetest_better_gsxt_selenium.py ' + i
    #         os.system(cmdstr)
    #     except TimeoutException:
    #         print('it takes too long time!')
    #         continue
    #     else:
    #         signal.alarm(0)

        time.sleep(0.3)

if __name__ == "__main__":
    main()






#
# with open('sample.csv', 'r') as the_file:
#     content = the_file.readlines()
#     # print(content[2])
#     # print(type(content[0]))
#
# for i in content:
#     print(i)
#     cmdstr = 'python geetest_better_gsxt_selenium.py ' + i
#
#     os.system(cmdstr)
#     time.sleep(0.3)