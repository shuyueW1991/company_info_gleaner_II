# -*- coding: utf-8 -*-

# Scrapy settings for liepin project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'liepin'

SPIDER_MODULES = ['liepin.spiders']
NEWSPIDER_MODULE = 'liepin.spiders'
# SPLASH_URL = 'http://localhost:8050/info?wait=0.5&images=1&expand=1&timeout=60.0&url=http%3A%2F%2F36kr.com&lua_source=function+main%28splash%29%0D%0A++local+url+%3D+splash.args.url%0D%0A++assert%28splash%3Ago%28url%29%29%0D%0A++assert%28splash%3Await%280.5%29%29%0D%0A++return+%7B%0D%0A++++html+%3D+splash%3Ahtml%28%29%2C%0D%0A++++png+%3D+splash%3Apng%28%29%2C%0D%0A++++har+%3D+splash%3Ahar%28%29%2C%0D%0A++%7D%0D%0Aend'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Exporting Settings
# FEED_URI = '/Users/Han/Desktop/Code/company_info_gleaner/itjuzi_history/%(name)s.txt'
# FEED_URI = '%(name)s_%(time)s.csv'
FEED_URI = '/mnt/qinzhihao/url_crawl/%(name)s_%(searchword)s_%(time)s.csv'
FEED_FORMAT = 'csv'
FEED_STORAGES = {'file': 'scrapy.extensions.feedexport.FileFeedStorage',}
FEED_EXPORTERS = {'csv': 'liepin.items.TxtItemExporter',}
FEED_STORE_EMPTY = False
FEED_EXPORT_FIELDS = ["lp_job_id",
                      "companyFullName",
                      "lp_co_lk",
                      "industryField",
                      "companySize",
                      "financeStage",
                      "lp_co_add",
                      "lp_co_intro",
                      "lp_job_pub_nm",
                      "lp_job_pub_pos",
                      "lp_job_apply_check_rate",
                      "lp_job_apply_check_dur",
                      "positionName",
                      "salary",
                      "lp_job_apply_fdbk",
                      "lp_job_add",
                      "lp_job_pub_time",
                      "lp_job_quals",
                      "description",
                      "lp_job_dept",
                      "lp_job_major",
                      "lp_job_boss",
                      "lp_job_subordinate"]
CSV_DELIMITER = "|"


# Logging Settings
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'liepinsearch.log'
LOG_LEVEL = 'INFO'
LOG_STDOUT = True


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'liepin (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16





# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}
LOG_LEVEL = 'INFO'
# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
   'liepin.middlewares.ProxyMiddleware': 543,
}
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    '
#}
DOWNLOADER_MIDDLEWARES = {
    # 'scrapy_splash.SplashCookiesMiddleware': 723,
    # 'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'liepin.spiders.rotate_useragent.RotateUserAgentMiddleware' :400,
    # 'liepin.middlewares.ProxyMiddleware': 543,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
CODELTAFETCH_ENABLED = True
CODELTAFETCH_DIR = '/mnt/qinzhihao/search'



ITEM_PIPELINES = {
   'liepin.pipelines.CoDeltaFetch': 200,
   'liepin.pipelines.LiepinPipeline': 100,
}



FEED_STORE_EMPTY = False

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
