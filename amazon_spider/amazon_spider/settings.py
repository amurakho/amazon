# -*- coding: utf-8 -*-

BOT_NAME = 'amazon_spider'

SPIDER_MODULES = ['amazon_spider.spiders']
NEWSPIDER_MODULE = 'amazon_spider.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16


DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy_rotated_proxy.downloadmiddlewares.proxy.RotatedProxyMiddleware': 750,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
}

# the path for image store
IMAGES_STORE = 'images'

# just need to add new field
USER_AGENTS = [
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/57.0.2987.110 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) '
     'Chrome/61.0.3163.79 '
     'Safari/537.36'),  # chrome
    ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
     'Gecko/20100101 '
     'Firefox/55.0'),  # firefox
    ('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'),
    ('Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12 Version/12.16'),
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'),
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36 Mozilla/5.0 (Windows N'),
    ('Mozilla/5.0 (X11; Xubuntu 19.04; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'),
    ('PmSxxdk9XTpCCp 9jZDZZmoFZM uppPHe23WBJZ1oZ QwxZHYrIPI1aL Gecko/12.6 eDuO7wF0s9SjvS3 Opera/68464427 9lZmqXyR71 m99LTwPF fU7eC9exBKjBZj ZTLqQo1ZB5x (Ubuntu 43.4; Win1312; x168; rv:914.10)')
]

# if you dont use proxy turn on it to True
ROTATED_PROXY_ENABLED = False

# # Proxy list
# HTTP_PROXIES = [
#     'http://user:pass@proxy1:8888',
# ]
# HTTPS_PROXIES = [
#     'https://user:pass@proxy1:8888',
# ]