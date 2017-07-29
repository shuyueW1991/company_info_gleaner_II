#-*-coding:utf-8-*-
import requests
import re
import traceback
import random

import math
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sys
import signal
import os
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementNotVisibleException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
import logging

# from pyvirtualdisplay import Display


logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='tyc.log',
                filemode='w')


# proxyHost = "proxy.abuyun.com"
# proxyPort = "9020"
# proxyUser = "H020G39R1142524D"
# proxyPass = "E440F4C798A80714"
# service_args = [
#     "--proxy-type=http",
#     "--proxy=%(host)s:%(port)s" % {
#         "host": proxyHost,
#         "port": proxyPort,
#     },
#     "--proxy-auth=%(user)s:%(pass)s" % {
#         "user": proxyUser,
#         "pass": proxyPass,
#     },
# ]



class tyc(object):

    def __init__(self, br_name="phantomjs", searchword=u"京东金融"):
        self.br = self.get_webdriver(br_name)

# the following  line is for  ubuntu server
#         self.display = Display(visible=0, size = (1920,1080)).start()
#         self.br = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
#         self.br.set_window_size(800,600)
# the above  line is for ubuntu server

        self.wait = WebDriverWait(self.br, 10, 1.0)
        self.br.set_page_load_timeout(18)
        self.br.set_script_timeout(8)
        self.name_list = []

        self.searchword = "this cannot be void"
        self.co_nm = "not there"
        self.co_add = "not there"
        self.co_tel = "not there"
        self.co_email = "not there"
        self.co_website = "not there"

        self.capital = "not there"
        self.status = "not there"
        self.industry = "not there"
        self.co_type = "not there"
        self.stock = "not there"
        self.rep = "not there"


    def write(self):
        the_line = ""
        the_line = the_line + self.searchword.replace(" ", "") + '|'
        the_line = the_line + self.co_nm.replace(" ", "") + '|'
        the_line = the_line + self.co_add.replace(" ", "") + '|'
        the_line = the_line + self.co_tel.replace(" ", "") + '|'
        the_line = the_line + self.co_email.replace(" ", "") + '|'
        the_line = the_line + self.co_website.replace("网址：","").replace(" ","") + '|'

        the_line = the_line + self.capital.replace(" ", "") + '|'
        the_line = the_line + self.status.replace(" ", "") + '|'
        the_line = the_line + self.industry.replace(" ", "") + '|'
        the_line = the_line + self.co_type.replace(" ", "") + '|'
        the_line = the_line + self.rep.replace(" ", "") + '|'
        the_line = the_line + self.stock.replace(" ","") + '\n'

        with open('file_info_tyc_name.txt', 'a') as the_file:
            the_file.write(the_line)
            the_file.flush()

    def input_params(self, name):
        # self.br.get("http://www.tianyancha.com/search?key={}&checkFrom=searchBox".format(name.encode("utf-8")))
        timeout_retry = 15
        while timeout_retry > 0:
            try:
                self.br.get("http://www.tianyancha.com")
            except TimeoutException:
                logging.debug("time out when opening tianyancha")
                timeout_retry = timeout_retry - 1
                time.sleep(5)
                continue
            else:
                break


        element = self.wait_for(By.ID, "live-search")
        element.send_keys(name)
        # time.sleep(10)
        element.send_keys(Keys.RETURN)
        time.sleep(1.1)

    # Added method to read-in company name list for scraping
    def wait_for(self, by1, by2):
        return self.wait.until(EC.presence_of_element_located((by1, by2)))


    def run(self, sousuoci):
        self.searchword = sousuoci
        self.hack_tyc(sousuoci)
        self.quit_webdriver()


    def hack_tyc(self, company=u"招商银行"):
        flag = True
        self.input_params(company)

        logging.info("trying to get the signal of successful input....")
        time.sleep(3)

        try:
            WebDriverWait(self.br, 18).until(EC.presence_of_element_located((By.CLASS_NAME, "search_result_single")))
            logging.info('there are results in tianyancha.')
        except TimeoutException:
            print('the name is not found in tyc')
            self.write()
            return None
        else:
            print('go.')

        # menu_list = self.br.find_elements_by_class_name('search_result_single search-2017 pb20 pt20 pl30 pr30')
        # menu_list = self.br.find_elements_by_xpath('//div[@class="search_result_single"]')
        menu_list = self.br.find_elements_by_class_name("search_result_single")

        val = menu_list[0]
        self.co_tyc_lk = self.br.find_elements_by_class_name("col-xs-10")
        self.co_tyc_link = self.co_tyc_lk[0].find_element_by_tag_name('a').get_attribute('href')
        print(self.co_tyc_link)

        logging.info(self.co_tyc_link)
        timeout_retry = 15
        while timeout_retry > 0:
            try:
                self.br.get(self.co_tyc_link)

            except TimeoutException:
                logging.info('we have an timeout error, retrying...')
                time.sleep(2.5)
                timeout_retry = timeout_retry -1
                continue
            else:
                break

        val = self.br.find_element_by_class_name('company_header_width')
        self.co_nm = val.find_element_by_class_name('f18').text
        self.co_tel = val.find_elements_by_class_name('mr20')[0].text
        self.co_website = val.find_elements_by_class_name('mr20')[1].text
        self.co_email = val.find_elements_by_class_name('emailWidth')[0].text
        self.co_add = val.find_elements_by_class_name('emailWidth')[1].text

        self.capital = self.br.find_elements_by_class_name('baseinfo-module-content-value')[0].text
        self.status = self.br.find_elements_by_class_name('baseinfo-module-content-value')[2].text

        table = self.br.find_element_by_class_name('base2017')
        self.industry = table.find_elements_by_class_name('basic-td')[5].find_element_by_tag_name('span').text
        self.co_type = table.find_elements_by_class_name('basic-td')[3].find_element_by_tag_name('span').text
        try:
            self.rep = self.br.find_elements_by_class_name('human-top')[0].find_element_by_class_name('new-c3').get_attribute('title')
        except:
            print('a company without rep. weird')

        try:
            self.stock = self.br.find_element_by_class_name('ml12').text
        except NoSuchElementException:
            print("not shangshi'ed yet")


        # self.stock = self.br.find_element_by_class_name('ml12').text if self.br.find_element_by_class_name('ml12').text else "not there"
        self.write()
        # self.br.delete_all_cookies()

        return 1


    def quit_webdriver(self):
        self.br.quit()
        # print('ok')



    def get_webdriver(self, name):
        if name.lower() == "phantomjs":
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            # dcap["phantomjs.page.settings.userAgent"] = (
            # "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")

            user_agent_list = [ \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
                "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
                "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
                "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
                "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
            ]

            dcap["phantomjs.page.settings.userAgent"] = (random.choice(user_agent_list))


            return webdriver.PhantomJS(desired_capabilities=dcap)

        elif name.lower() == "chrome":
            return webdriver.Chrome()


if __name__ == "__main__":
    # tyc("chrome").run(sys.argv[1])
    # tyc("phantomjs").run(sys.argv[1])
    # tyc("phantomjs").run('美乐达（北京）商业管理有限公司')
    # print(type('美乐达（北京）商业管理有限公司'))
    # tyc("phantomjs").run()
    thefiletoread = sys.argv[1]
    # for i in open('sample.csv', 'r'):
    for i in open(thefiletoread, 'r'):
        print(i)
        try:
            tyc("phantomjs").run(i.replace("\n",""))
            print(" we are now in!")
        except:
            traceback.print_exc()
            print("oops, some errors occur'ed")
            continue








