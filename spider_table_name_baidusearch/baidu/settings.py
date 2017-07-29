# -*- coding: utf-8 -*-

# Scrapy settings for baidu project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'baidu'

SPIDER_MODULES = ['baidu.spiders']
NEWSPIDER_MODULE = 'baidu.spiders'
# SPLASH_URL = 'http://localhost:8050/info?wait=0.5&images=1&expand=1&timeout=60.0&url=http%3A%2F%2F36kr.com&lua_source=function+main%28splash%29%0D%0A++local+url+%3D+splash.args.url%0D%0A++assert%28splash%3Ago%28url%29%29%0D%0A++assert%28splash%3Await%280.5%29%29%0D%0A++return+%7B%0D%0A++++html+%3D+splash%3Ahtml%28%29%2C%0D%0A++++png+%3D+splash%3Apng%28%29%2C%0D%0A++++har+%3D+splash%3Ahar%28%29%2C%0D%0A++%7D%0D%0Aend'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'baidu (+http://www.yourdomain.com)'

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

# Failure Retries
RETRY_ENABLED = True
RETRY_TIMES = 10
# RETRY_HTTP_CODES = [400,500,502,503,408]
RETRY_HTTP_CODES = [400,403,404,408,429,500,502,503]


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
   # 'baidu.middlewares.BaiduSpiderMiddleware': 543,
    # 'baidu.middlewares.ProxyMiddleware': 543,

   'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,

}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'baidu.spiders.rotate_useragent.RotateUserAgentMiddleware' :400,

   # 'baidu.middlewares.MyCustomDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'baidu.pipelines.BaiduPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
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
