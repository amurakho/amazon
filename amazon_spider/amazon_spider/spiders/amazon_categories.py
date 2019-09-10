# -*- coding: utf-8 -*-
import scrapy


class AmazonSpider(scrapy.Spider):
    name = 'amazon_categories'
    allowed_domains = ['amazon.in']
    start_urls = ['https://www.amazon.in/gp/bestsellers/']
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    base_url = 'https://www.amazon.in'

    category_urls = []

    def parse(self, response):
        blocks = response.xpath('//ul[@id="zg_browseRoot"]//@href').getall()
        yield {"url": response.url}
        for url in blocks:
            if url not in self.category_urls:
                self.category_urls.extend(url)
                yield scrapy.Request(url, callback=self.parse)
