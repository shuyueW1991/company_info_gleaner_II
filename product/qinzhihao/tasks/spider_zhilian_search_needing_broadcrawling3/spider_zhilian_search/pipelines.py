# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import pymysql
import traceback
import datetime
from scrapy.exceptions import DropItem

import logging
import os
import time

from scrapy.http import Request
from scrapy.item import BaseItem
from scrapy.utils.request import request_fingerprint
from scrapy.utils.project import data_path
from scrapy.utils.python import to_bytes
from scrapy.exceptions import NotConfigured
from scrapy import signals

logger = logging.getLogger(__name__)

class CoDeltaFetch(object):
    """
    This is a spider middleware to ignore requests to pages containing items
    seen in previous crawls of the same spider, thus producing a "delta crawl"
    containing only new items.

    This also speeds up the crawl, by reducing the number of requests that need
    to be crawled, and processed (typically, item requests are the most cpu
    intensive).
    """

    def __init__(self, dir, reset=False, stats=None):
        dbmodule = None
        try:
            dbmodule = __import__('bsddb3').db
        except ImportError:
            raise NotConfigured('bsddb3 is required')
        self.dbmodule = dbmodule
        self.dir = dir
        self.reset = reset
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        s = crawler.settings
        if not s.getbool('CODELTAFETCH_ENABLED'):
            raise NotConfigured
        dir = data_path(s.get('CODELTAFETCH_DIR', 'codeltafetch'))
        reset = s.getbool('CODELTAFETCH_RESET')
        o = cls(dir, reset, crawler.stats)
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_opened(self, spider):
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        dbpath = os.path.join(self.dir, 'company_info.db' )
        reset = self.reset or getattr(spider, 'codeltafetch_reset', False)
        flag = self.dbmodule.DB_TRUNCATE if reset else self.dbmodule.DB_CREATE
        try:
            self.db = self.dbmodule.DB()
            self.db.open(filename=dbpath,
                         dbtype=self.dbmodule.DB_HASH,
                         flags=flag)
        except Exception:
            logger.warning("Failed to open CoDeltaFetch database at %s, "
                           "trying to recreate it" % dbpath)
            if os.path.exists(dbpath):
                os.remove(dbpath)
            self.db = self.dbmodule.DB()
            self.db.open(filename=dbpath,
                         dbtype=self.dbmodule.DB_HASH,
                         flags=self.dbmodule.DB_CREATE)

    def spider_closed(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        r = item
        if isinstance(r, (BaseItem, dict)):
            key = self._get_key(r)
            if key in self.db:
                logger.info("Ignoring already crawl: %s" % r)
                if self.stats:
                    self.stats.inc_value('codeltafetch/skipped', spider=spider)
            else:
                self.db[key] = str(time.time())
                if self.stats:
                    self.stats.inc_value('codeltafetch/stored', spider=spider)
                return r

    def _get_key(self, item):
        try:
            key = item['companyFullName']
            key = to_bytes(key)
        except:
            key = item['companyFullName'][0]
            print(type(key))
            key = to_bytes(key)
        # request_fingerprint() returns `hashlib.sha1().hexdigest()`, is a string
        return key

class SpiderZhilianSearchPipeline(object):
    # def __init__(self):
    #     # upload to database ...
    #     self.source_mysql_host = "rm-bp1tp2w15f1qlap94.mysql.rds.aliyuncs.com"
    #     self.source_mysql_db = "buz_source_data"
    #     self.source_mysql_user = "root"
    #     self.source_mysql_passwd = "u8!7-ZXC"
    #     self.conn = pymysql.connect(host=self.source_mysql_host, user=self.source_mysql_user,
    #                                 passwd=self.source_mysql_passwd, db=self.source_mysql_db, charset='utf8')
    #     self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)



    def process_item(self, item, spider):
        # sql = "insert into wuyaojob_co_template(wuyaojob_co_web_id,co_nm,co_staff_num,co_type,co_short_desc,co_add)\
        # values ('{0}', '{1}', '{2}', '{3}', '{4}','{5}')"

        try:
            print(item['companyFullName'])
            if len(item):
                print(len(item))
            else:
                print('rien in item!!')
            # if item['co_nm']:
                # self.cursor.execute(sql.format(item['wuyaojob_co_web_id'], item['co_nm'], item['co_staff_num'], item['co_type'], item['co_short_desc']\
                #                            , item['co_add']))
                # self.conn.commit()
                # return item
            flag = 'pos'

            neg_list = ['上海外滩','海外游','海外旅游','房产中介','链家','海底捞','海外背景','海外留学','海外置业','跟单','编辑','买手','采购','推广','广告投放','房产投资','房产','运营','清关','SNS','SEO','facebook','亚马逊','google','SEM','移民','置业','理财','招商','创业','老师','教师','培训','护士','厨师','保险','房产销售','上海外','珠海外','不动产','海外包','猎头']

            for word in neg_list:
                if word in item['companyFullName']:
                    flag = 'neg'
                    break
                for i, val in enumerate(item['positionName']):
                    if word in val:
                        flag = 'neg'
                        break

            if flag == 'pos':
                return item
            else:
                raise DropItem("neg word in item, so it is dropped.")



        except:
            traceback.print_exc()
            raise DropItem("Something nasty happens, nigger!")