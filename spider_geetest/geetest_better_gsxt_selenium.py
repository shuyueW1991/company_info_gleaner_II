#-*-coding:utf-8-*-
import requests
import re
import StringIO
from PIL import Image
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
from selenium.common.exceptions import TimeoutException, WebDriverException, ElementNotVisibleException


class crack_picture(object):
    def __init__(self, img_url1, img_url2):
        self.img1, self.img2 = self.picture_get(img_url1, img_url2)


    def picture_get(self, img_url1, img_url2):
        hd = {"Host": "static.geetest.com",
              "User-Agent": 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        img1 = StringIO.StringIO(self.repeat(img_url1, hd).content)
        img2 = StringIO.StringIO(self.repeat(img_url2, hd).content)
        return img1, img2


    def repeat(self, url, hd):
        times = 10
        while times > 0:
            try:
                ans = requests.get(url, headers=hd)
                return ans
            except:
                times -= 1


    def pictures_recover(self):
        xpos = self.judge(self.picture_recover(self.img1, 'img1.jpg'), self.picture_recover(self.img2, 'img2.jpg')) - 6
        return self.darbra_track(xpos)


    def picture_recover(self, img, name):
        a =[39, 38, 48, 49, 41, 40, 46, 47, 35, 34, 50, 51, 33, 32, 28, 29, 27, 26, 36, 37, 31, 30, 44, 45, 43, 42, 12, 13, 23, 22, 14, 15, 21, 20, 8, 9, 25, 24, 6, 7, 3, 2, 0, 1, 11, 10, 4, 5, 19, 18, 16, 17]
        im = Image.open(img)
        im_new = Image.new("RGB", (260, 116))
        for row in range(2):
            for column in range(26):
                right = a[row*26+column] % 26 * 12 + 1
                down = 58 if a[row*26+column] > 25 else 0
                for w in range(10):
                    for h in range(58):
                        ht = 58 * row + h
                        wd = 10 * column + w
                        im_new.putpixel((wd, ht), im.getpixel((w + right, h + down)))
        im_new.save(name)
        return im_new


    def darbra_track(self, distance):
        tracks = [[random.randint(-20, -10), random.randint(-20, -10), 0],
                  [0, 0, 0],
                  [1, 0, random.randint(0, 8) * 1.0 / 10],
                  [distance-10,0,random.randint(0, 8) * 1.0 / 10],
                  [3, 0, random.randint(0, 8) * 1.0 / 10],
                  [7, 0, random.randint(0, 8) * 1.0 / 10]]

        print('distance is {}'.format(distance))
        print('tracks is {}'.format(tracks))
        return tracks
 
    def diff(self, img1, img2, wd, ht):
        rgb1 = img1.getpixel((wd, ht))
        rgb2 = img2.getpixel((wd, ht))
        tmp = reduce(lambda x,y: x+y, map(lambda x: abs(x[0]-x[1]), zip(rgb1, rgb2)))
        return True if tmp >= 200 else False


    def col(self, img1, img2, cl):
        for i in range(img2.size[1]):
            if self.diff(img1, img2, cl, i):
                return True
        return False


    def judge(self, img1, img2):
        for i in range(img2.size[0]):
            if self.col(img1, img2, i):
                return i
        return -1


class gsxt(object):

    def __init__(self, br_name="phantomjs", searchword=u"京东金融"):
        # self.br = self.get_webdriver(br_name)
        self.br = webdriver.Chrome()
        self.wait = WebDriverWait(self.br, 10, 1.0)
        self.br.set_page_load_timeout(8)
        self.br.set_script_timeout(8)
        self.name_list = []

        self.searchword = searchword
        self.co_nm = "阿扎里"
        self.co_status = "存续"
        self.code = "119121120"
        self.rep = "刘强西"
        self.co_birth = "1991-02-31"
        self.co_gsxt_link = "www.taobao.com"
        self.co_tel = "110"
        self.co_email = "dick@nihao.edu.cn"
        self.capital = 'billionaire, mate.'

    def write(self):
        the_line = ""
        the_line = the_line + self.co_nm.replace(" ", "") + '|'
        the_line = the_line + self.co_status.replace(" ", "") + '|'
        the_line = the_line + self.co_code.replace(" ", "") + '|'
        the_line = the_line + self.co_rep.replace(" ", "") + '|'
        the_line = the_line + self.co_birth.replace(" ", "") + '|'
        the_line = the_line + self.capital.replace(" ", "") + '|'
        the_line = the_line + self.co_tel.replace(" ", "") + '|'
        the_line = the_line + self.co_email.replace(" ", "") + '\n'
        with open('file_info_bettergeetest_海外.txt', 'a') as the_file:
            the_file.write(the_line)
            the_file.flush()

    def input_params(self, name):
        self.br.get("http://www.gsxt.gov.cn/index")
        element = self.wait_for(By.ID, "keyword")
        element.send_keys(name)
        time.sleep(1.1)
        element = self.wait_for(By.ID, "btn_query")
        element.click()
        time.sleep(1.1)

    # Added method to read-in company name list for scraping
    def list_gen(self):
        file = pd.read_excel(list_file)
        self.name_list = self.name_list.append(list(file[file.columns[0]]))
        return self.name_list

    def drag_pic(self):
        return (self.find_img_url(self.wait_for(By.CLASS_NAME, "gt_cut_fullbg_slice")),
               self.find_img_url(self.wait_for(By.CLASS_NAME, "gt_cut_bg_slice")))

    def wait_for(self, by1, by2):
        return self.wait.until(EC.presence_of_element_located((by1, by2)))


    def find_img_url(self, element):
        try:
            return re.findall('url\("(.*?)"\)', element.get_attribute('style'))[0].replace("webp", "jpg")
        except:
            return re.findall('url\((.*?)\)', element.get_attribute('style'))[0].replace("webp", "jpg")

    def emulate_track(self, tracks):
        element = self.br.find_element_by_class_name("gt_slider_knob")
        ActionChains(self.br).click_and_hold(on_element=element).perform()
        for x, y, t in tracks:
            print(x, y, t)
            ActionChains(self.br).move_to_element_with_offset(
                to_element=element,
                xoffset=x + 22,
                yoffset=y + 22).perform()
            ActionChains(self.br).click_and_hold().perform()
            time.sleep(t)
        time.sleep(0.24)
        ActionChains(self.br).release(on_element=element).perform()
        time.sleep(0.8)
        element = self.wait_for(By.CLASS_NAME, "gt_info_text")
        ans = element.text.encode("utf-8")
        print(ans)
        return ans


    def run(self, sousuoci):
        self.hack_geetest(unicode(sousuoci, "utf-8"))
        time.sleep(0.95)

        self.quit_webdriver()



    def hack_geetest(self, company=u"招商银行"):
        flag = True
        self.input_params(company)
        while flag:
            img_url1, img_url2 = self.drag_pic()
            tracks = crack_picture(img_url1, img_url2).pictures_recover()
            tsb = self.emulate_track(tracks)
            if '通过' in tsb:
                time.sleep(1)
                soup = BeautifulSoup(self.br.page_source, 'html.parser')
                for sp in soup.find_all("a", attrs={"class":"search_list_item"}):
                    print re.sub("\s+", "", sp.get_text().encode("utf-8"))
                    print('marked ...')


                time.sleep(1.3)
                print("trying to get the signal of successful yanzheng....")
                time.sleep(3)
                try:
                    signal = self.br.find_element_by_class_name("search_result").text.encode("utf-8")
                    if signal.startswith('查询') or signal.startswith('用时'):
                        print('on le trouve')
                        yanzheng_flag = 0
                except:
                    yanzheng_flag = 1
                print('we are now in inside page!')
                break

            elif '吃' in tsb:
                time.sleep(5)
            else:
                self.input_params(company)

        menu_list = self.br.find_elements_by_class_name("search_list_item")


        val = menu_list[0]
        self.co_nm = val.find_element_by_class_name("f20").text.encode("utf-8")
        print(self.co_nm)
        self.co_status = val.find_element_by_class_name("wrap-corpStatus").text.encode("utf-8")
        print(self.co_status)
        self.co_code = val.find_element_by_class_name("div-map2").text.encode("utf-8")
        print(self.co_code)
        self.co_rep = val.find_element_by_class_name("div-user2").text.encode("utf-8")
        print(self.co_rep)
        self.co_birth = val.find_element_by_class_name("div-info-circle2").text.encode("utf-8")
        print(self.co_birth)
        time.sleep(0.3)
        self.co_gsxt_link = val.get_attribute('href').encode("utf-8")
        print(self.co_gsxt_link)

        time.sleep(1.5)


        while True:
            try:
                self.br.get(self.co_gsxt_link)
            except TimeoutException:
                print('we meet an timeout error, retrying...')
                continue
            else:
                break

        overview = self.br.find_element_by_class_name("overview")
        self.capital = overview.find_elements_by_class_name("result")[4].text.encode('utf-8')
        print(self.capital)


        self.br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(4.2)
        self.br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3.2)
        self.br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(6.2)
        self.br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2.1)
        self.br.execute_script("window.scrollTo(0, 0.5*document.body.scrollHeight);")
        time.sleep(2.1)

        WebDriverWait(self.br, 18).until(EC.presence_of_element_located((By.ID, "annual_menu")))
        # time.sleep(5.3)

        print('whole context')
        nianbao = self.br.find_element_by_id("annual_menu").text
        print(nianbao)
        nianbao = nianbao.encode("utf-8")


        if "查看" in nianbao:
            print('there is annual reportage!')
            chakan = self.br.find_element_by_id("annual_menu_table")
            self.br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(6.6)
            # WebDriverWait(self.br, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "clickToDetail")))
            print('wait to be clicked...')

            while True:
                try:
                    # chakan_click = chakan.find_element_by_class_name("clickToDetail").click()
                    chakan_click = WebDriverWait(self.br, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "clickToDetail"))).click()
                    print(chakan_click)
                    print('wait for 10 sec to make the button clickable manually')
                    time.sleep(10)


                except WebDriverException:
                    print('webdriverexceptioncontent:')
                    print(WebDriverException)
                    print('meet unclickable issue, retrying..')
                    time.sleep(1.2)
                    self.br.execute_script("window.scrollTo(0, 0.46*document.body.scrollHeight);")
                    time.sleep(0.3)
                    self.br.execute_script("window.scrollTo(0, 0.45*document.body.scrollHeight);")
                    # time.sleep(6.2)
                    continue
                else:
                    break

            # chakan_click = chakan.find_element_by_class_name("clickToDetail").click()

            time.sleep(1.1)
            self.br.execute_script("window.scrollTo(0, 150);")
            time.sleep(1.1)

            self.br.switch_to_window(self.driver.window_handles[1])
            time.sleep(10.5)

            self.co_tel = self.br.find_element_by_id("tel").text.encode("utf-8")
            print(self.co_tel)
            self.co_email = self.br.find_element_by_id("email").text.encode("utf-8")
            print(self.co_email)

            self.write()

        else:
            print('zan wu annual reportage!')
            self.co_tel = "unknown"
            print(self.co_tel)
            self.co_email = "unknown"
            print(self.co_tel)

            self.write()



    def quit_webdriver(self):
        self.br.quit()


    def get_webdriver(self, name):
        if name.lower() == "phantomjs":
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
            return webdriver.PhantomJS(desired_capabilities=dcap)

        elif name.lower() == "chrome":
            return webdriver.Chrome()


if __name__ == "__main__":
    #print crack_picture("http://static.geetest.com/pictures/gt/fc064fc73/fc064fc73.jpg", "http://static.geetest.com/pictures/gt/fc064fc73/bg/7ca363b09.jpg").pictures_recover()
    gsxt("chrome").run(sys.argv[1])



