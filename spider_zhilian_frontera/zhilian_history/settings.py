# -*- coding: utf-8 -*-

# Scrapy settings for zhilian_history project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhilian'

SPIDER_MODULES = ['zhilian_history.spiders']
NEWSPIDER_MODULE = 'zhilian_history.spiders'

# Frontera Settings
SCHEDULER = 'frontera.contrib.scrapy.schedulers.frontier.FronteraScheduler'
# REACTOR_THREADPOOL_MAXSIZE = 32
# DNS_TIMEOUT = 180

FRONTERA_SETTINGS = 'frontier.spider_settings'

# Exporting Settings
# FEED_URI = '/Users/Han/Desktop/Code/company_info_gleaner/zhilian_history/%(name)s_20170602.txt'
FEED_URI = '/root/users/JH/company_info_gleaner_II/zhilian_history/%(name)s_20170611.txt'
FEED_FORMAT = 'csv'
FEED_STORAGES = {'file': 'scrapy.extensions.feedexport.FileFeedStorage',}
FEED_EXPORTERS = {'csv': 'zhilian_history.items.TxtItemExporter',}
FEED_STORE_EMPTY = False
FEED_EXPORT_FIELDS = ["zl_co_id",
                      "zl_co_name",
                      "zl_co_tags",
                      "zl_co_website",
                      "zl_co_type",
                      "zl_co_ee_size",
                      "zl_co_address",
                      "zl_co_desc",
                      "zl_update_time"]
CSV_DELIMITER = "|"

# Logging Settings
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'zhilian_history.log'
LOG_LEVEL = 'INFO'
LOG_STDOUT = True

# Broad Crawling Ajax Enabled
#AJAXCRAWL_ENABLED = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_IP = 8

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Failure Retries
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [400,403,404,408,429,500,502,503]

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
AUTOTHROTTLE_START_DELAY = 0.1
AUTOTHROTTLE_MAX_DELAY = 1
AUTOTHROTTLE_TARGET_CONCURRENCY = 32
AUTOTHROTTLE_DEBUG = False

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': None,
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerSpiderMiddleware': 999,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'zhilian_history.middlewares.RandomUserAgentMiddleware': 200,
    'zhilian_history.middlewares.ProxyMiddleware':None,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerDownloaderMiddleware': 999,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'zhilian_history.pipelines.RemoveEmptyPipeline': 300,
}


