# -*- coding: utf-8 -*-

# Scrapy settings for spider_official_websites project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#
# DEPTH_PRIORITY = 1
# SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
# SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

BOT_NAME = 'spider_websites_content_frontera'

SPIDER_MODULES = ['spider_websites_content_frontera.spiders']
NEWSPIDER_MODULE = 'spider_websites_content_frontera.spiders'

DELTAFETCH_ENABLED = True
DELTAFETCH_DIR = '/mnt/qinzhihao/spider_websites_content_frontera/'
# DELTAFETCH_DIR = '/root/users/JH/company_info_gleaner_II/spider_websites_content_frontera/'

# Frontera Settings
SCHEDULER = 'frontera.contrib.scrapy.schedulers.frontier.FronteraScheduler'

FRONTERA_SETTINGS = 'frontier.spider_settings'

# Logging Settings
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'crawler.log'
LOG_LEVEL = 'INFO'
LOG_STDOUT = True

# Exporting Settings
# FEED_URI = '/Users/Han/Desktop/Code/company_info_gleaner_II/spider_official_websites/%(name)s_20170627.txt'
# FEED_URI = '/mnt/qinzhihao/Try/spider_websites_content/%(name)s_%(time)s.txt'
# FEED_FORMAT = 'csv'
# FEED_STORAGES = {'file': 'scrapy.extensions.feedexport.FileFeedStorage',}
# FEED_EXPORTERS = {'csv': 'spider_official_websites.items.TxtItemExporter',}
# FEED_STORE_EMPTY = False
# FEED_EXPORT_FIELDS = ["host_url",
#                      "url",
#                      "email",
#                      "mobile"
#                      ]
# CSV_DELIMITER = "|"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'spider_official_websites (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 200,
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerSpiderMiddleware': 999
}

REDIRECT_ENABLED = False

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'spider_websites_content_frontera.middlewares.RandomUserAgentMiddleware': 200,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'frontera.contrib.scrapy.middlewares.schedulers.SchedulerDownloaderMiddleware': 999
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'spider_websites_content_frontera.pipelines.SpiderOfficialWebsitesPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 2
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = True

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = False
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
