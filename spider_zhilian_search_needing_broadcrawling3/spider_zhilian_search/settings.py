# -*- coding: utf-8 -*-

# Scrapy settings for spider_zhilian_search project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'spider_zhilian_search'

SPIDER_MODULES = ['spider_zhilian_search.spiders']
NEWSPIDER_MODULE = 'spider_zhilian_search.spiders'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'spider_zhilian_search (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

LOG_LEVEL = 'DEBUG'
# Failure Retries
RETRY_ENABLED = True
RETRY_TIMES = 3
# RETRY_HTTP_CODES = [400,500,502,503,408]
RETRY_HTTP_CODES = [400,403,404,408,429,500,502,503]


# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   # 'spider_zhilian_search.middlewares.SpiderZhilianSearchSpiderMiddleware': 543,
   'scrapy_splash.SplashDeduplicateArgsMiddleware': 100
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'spider_zhilian_search.defaultpackages.RandomUserAgentMiddleware': 200,
    # 'spider_zhilian_search.middlewares.ProxyMiddleware': 300,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'spider_zhilian_search.pipelines.SpiderZhilianSearchPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = False
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 0.1
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 1
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 32
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


# Exporting Settings
FEED_URI = '/mnt/qinzhihao/Data/%(name)s_%(time)s.csv'
# FEED_URI = '%(name)s_%(time)s.csv'
# FEED_URI = '/root/users/WSY/spider_zhilian_search_needing_broadcrawling/%(name)s_20170605.txt'
FEED_FORMAT = 'csv'
FEED_STORAGES = {'file': 'scrapy.extensions.feedexport.FileFeedStorage',}
FEED_EXPORTERS = {'csv': 'spider_zhilian_search.items.TxtItemExporter',}
FEED_STORE_EMPTY = False
FEED_EXPORT_FIELDS = ["positionName",
                      "salary",
                      "job_loc",
                      "description",
                      "co_id",
                      "companyFullName",
                      "financeStage",
                      "companySize",
                      "co_link",
                      "industryField",
                      "co_add",
                      "co_desc"]
# FEED_EXPORT_FIELDS = ["co_id",
#                       "co_nm",
#                       "co_ownership",
#                       "co_ee_size",
#                       "co_link",
#                       "co_industry",
#                       "co_add",
#                       "co_desc"]

CSV_DELIMITER = "|"

# Logging Settings
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'zhilian_search.log'
LOG_LEVEL = 'DEBUG'
LOG_STDOUT = True
