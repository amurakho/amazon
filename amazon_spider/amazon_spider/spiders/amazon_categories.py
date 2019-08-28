# -*- coding: utf-8 -*-
import scrapy
from pprint import pprint
from ..items import AmazonSpiderItem
from scrapy import signals
from collections import deque

class AmazonSpider(scrapy.Spider):
    name = 'amazon_categories'
    allowed_domains = ['amazon.in']
    start_urls = ['https://www.amazon.in/gp/bestsellers/']
    custom_settings = {
        # 'SPIDER_MIDDLEWARES': {
        #     'amazon_spider.middlewares.AmazonSpiderSpiderMiddleware': 543,
        # },
        # 'DOWNLOAD_DELAY': 5,
        # 'USER-AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
    }

    # base_category_url = 'https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3D{}&field-keywords='
    base_url = 'https://www.amazon.in'

    category_urls = []

    def parse(self, response):
        blocks = response.xpath('//ul[@id="zg_browseRoot"]//@href').getall()
        print(blocks)
        for url in blocks:
            if url not in self.category_urls:
                self.category_urls.extend(url)
                yield scrapy.Request(url, callback=self.parse)


    def closed(self, reason):
        for item in self.category_urls:
            print(item)
