# -*- coding: utf-8 -*-

# Scrapy settings for itjuzi_history project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'itjuzi_history'

SPIDER_MODULES = ['itjuzi_history.spiders']
NEWSPIDER_MODULE = 'itjuzi_history.spiders'

# Exporting Settings
# FEED_URI = '/Users/Han/Desktop/Code/company_info_gleaner/itjuzi_history/%(name)s.txt'
FEED_URI = '/root/users/JH/itjuzi_history/%(name)s.txt'
FEED_FORMAT = 'csv'
FEED_STORAGES = {'file': 'scrapy.extensions.feedexport.FileFeedStorage',}
FEED_EXPORTERS = {'csv': 'itjuzi_history.items.TxtItemExporter',}
FEED_STORE_EMPTY = False
FEED_EXPORT_FIELDS = ["it_co_id",
                      "it_short_name",
                      "it_full_name",
                      "it_short_desc",
                      "it_full_desc",
                      "it_desc_tag",
                      "it_ind_tag",
                      "it_location",
                      "it_website",
                      "it_estab_time",
                      "it_ee_size",
                      "it_active_status",
                      "it_investment_info",
                      "it_mgmt_name",
                      "it_mgmt_desc",
                      "it_prd_info",
                      "it_news",
                      "it_milestone",
                      "it_co_views",
                      "it_co_followers",
                      "it_update_time"]
CSV_DELIMITER = "|"

# Logging Settings
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'itjuzi_history.log'
LOG_LEVEL = 'INFO'
LOG_STDOUT = True

# Broad Crawling Ajax Enabled
#AJAXCRAWL_ENABLED = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'itjuzi_history (+http://www.nba.com)'
#USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 16

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 8

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Failure Retries
RETRY_ENABLED = True
RETRY_TIMES = 10
# RETRY_HTTP_CODES = [400,500,502,503,408]
RETRY_HTTP_CODES = [400,403,404,408,429,500,502,503]

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = False
# The initial download delay
AUTOTHROTTLE_START_DELAY = 1
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 10
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

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
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'itjuzi_history.middlewares.ProxyMiddleware':300,
    'itjuzi_history.middlewares.RandomUserAgentMiddleware':200,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# DOWNLOADER_MIDDLEWARES = {
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'itjuzi_history.pipelines.RemoveEmptyPipeline': 300,
}

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# DOWNLOADER_CLIENTCONTEXTFACTORY = 'itjuzi_history.contextfactory.CustomClientContextFactory'
