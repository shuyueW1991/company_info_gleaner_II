# -*- coding: utf-8 -*-

# Scrapy settings for spider_chinahr project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'chinahr'

SPIDER_MODULES = ['spider_chinahr.spiders']
NEWSPIDER_MODULE = 'spider_chinahr.spiders'

DELTAFETCH_ENABLED = True
DELTAFETCH_DIR = '/home/qinzhihao/company_info_gleaner_II/spider_chinahr'

# Exporting Settings
# FEED_URI = '%(name)s_20170613.txt'
# # FEED_URI = '/Users/Han/Desktop/Code/company_info_gleaner_II/spider_chinahr/%(name)s_20170612.txt'
# FEED_FORMAT = 'csv'
# FEED_STORAGES = {'file': 'scrapy.extensions.feedexport.FileFeedStorage',}
# FEED_EXPORTERS = {'csv': 'spider_chinahr.items.TxtItemExporter',}
# FEED_STORE_EMPTY = False
# FEED_EXPORT_FIELDS = ["chr_co_name",
#                       "chr_co_city",
#                       "chr_co_industry"
#                       "chr_co_ownership",
#                       "chr_co_estab",
#                       "chr_co_regcap",
#                       "chr_contact_name",
#                       "chr_mobile_num",
#                       "chr_fixline_num",
#                       "chr_email_addr",
#                       "chr_co_address",
#                       "chr_co_des",
#                       "chr_co_url"]


# FEED_EXPORT_FIELDS = ["chr_co_url"]

# CSV_DELIMITER = "|"

# Logging Settings
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FILE = 'chinahr.log'
LOG_LEVEL = 'INFO'
LOG_STDOUT = True

# Failure Retries
RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [400,403,404,408,429,500,502,503]

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'spider_chinahr.middlewares.RandomUserAgentMiddleware': 200,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_deltafetch.DeltaFetch': 200,
}

ITEM_PIPELINES = {
    'spider_chinahr.pipelines.SpiderChinahrPipeline': 300,
}
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 0.5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 2
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

CONCURRENT_REQUESTS = 32
DOWNLOAD_DELAY = 0.2
