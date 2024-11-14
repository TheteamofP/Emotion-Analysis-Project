# Scrapy settings for weibo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "weibo_crawler"

SPIDER_MODULES = ["weibo_crawler.spiders"]
NEWSPIDER_MODULE = "weibo_crawler.spiders"

LOG_LEVEL = "ERROR"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "weibo (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# 访问完一个页面再访问下一个时需要等待的时间，默认为10秒
DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7', 'cookie': 'SCF=AqzItcpERSRncgfjCZPczes-KRr42yTKgqFPHbm7QwBvoNb8eB4tqbFp-F5CsEkncIEfsUbrJQNxUr4PASYxlZM.; SINAGLOBAL=6119462789861.474.1730040034674; ALF=1734005870; SUB=_2A25KNzc-DeRhGeBN7FUZ-CzEyjiIHXVpTTb2rDV8PUJbkNAbLWLfkW1NRDwy-I0O1adphGDLXMzROdCh9-f2D5Fj; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF30phkrMm8z.FbwdOzBlmJ5JpX5KMhUgL.Foq0S0MR1hzReKB2dJLoI7p39g4_qg4.Ug4DdJ.t; WBPSESS=mrYjkxQaCtAUTyP-YmCbdzbXx7p1BwGpxOFCP-0UaUQ_VwPVGujJD8ZAC-wNDz4VPg4aqSi-sBH7e1y8CFnUqCoH_82jF8wUMlQpHjD3yXLNmnEQmhBgqHHcSsDF2owoV-SREXeuv-0YxNQen-T1FA==; ULV=1731509151437:3:2:2:6820767867987.472.1731509151399:1731427839841; XSRF-TOKEN=ii6Qj8Lqt85MfRepc4dwpOOy'}


KEYWORD_LIST = ['jennie', 'kim jennie']

REGION = []

# 要搜索的微博类型，0代表搜索全部微博，1代表搜索全部原创微博，2代表热门微博，3代表关注人微博，4代表认证用户微博，5代表媒体微博，6代表观点微博
WEIBO_TYPE = 0

# 筛选结果微博中必需包含的内容，0代表不筛选，获取全部微博，1代表搜索包含图片的微博，2代表包含视频的微博，3代表包含音乐的微博，4代表包含短链接的微博
CONTAIN_TYPE = 1

# 搜索的起始日期，为yyyy-mm-dd形式，搜索结果包含该日期
START_DATE = '2024-11-13'
# 搜索的终止日期，为yyyy-mm-dd形式，搜索结果包含该日期
END_DATE = '2024-11-14'

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "weibo.middlewares.WeiboSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    "weibo.middlewares.WeiboDownloaderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "weibo.pipelines.WeiboPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"

FEED_EXPORT_ENCODING = "utf-8"

TWISTED_REACTOR = "twisted.internet.selectreactor.SelectReactor"

