# -*- coding: utf-8 -*-

# Scrapy settings for Nine project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Nine'

SPIDER_MODULES = ['Nine.spiders']
NEWSPIDER_MODULE = 'Nine.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Nine (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.qishu.cc',
    'Referer': 'http://www.qishu.cc/',
    'Upgrade-Insecure-Requests': '1',
    'cookies': '__music_index__=2; ASPSESSIONIDQCCDCART=ADCJOKECHKHHPNKBMIIHEKAH; NewAspUsers%5FOnline=UserSessionID=11331555654; UM_distinctid=16bbcaa112913e-0cb611d1b8ed31-7a1437-1fa400-16bbcaa112a68; 37cs_user=37cs52163986298; 37cs_show=69; __music_index__=2; CNZZDATA1642736=cnzz_eid%3D1136135112-1562239206-null%26ntime%3D1562239206; bdshare_firstime=1562240402471; _d_id=3533d113318a3ac920446bc8666b3b; CNZZDATA1835761=cnzz_eid%3D195897192-1562236194-null%26ntime%3D1562247708; Hm_lvt_0b955fc6fbfeb4990aa7b8d5c8d944aa=1562238391,1562238967,1562247135,1562248118; Hm_lpvt_0b955fc6fbfeb4990aa7b8d5c8d944aa=1562251398',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
}
# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'Nine.middlewares.NineSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'Nine.middlewares.NineDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'Nine.pipelines.TextPipeline': 100,
   'Nine.pipelines.MysqlPipline': 200,

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
MYSQL_HOST = ''           # 主机名，请修改
MYSQL_DBNAME = ''         #数据库名字，请修改
MYSQL_USER = ''             #数据库账号，请修改
MYSQL_PASSWD = ''         #数据库密码，请修改
MYSQL_PORT = 3306               #数据库端口，在dbhelper中使用

LOG_FILE = 'nine.log'
LOG_LEVEL = 'DEBUG'
