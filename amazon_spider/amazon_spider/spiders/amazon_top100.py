# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonProductItem
import time
from inline_requests import inline_requests
import random
import json

class AmazonTop100Spider(scrapy.Spider):
    """
    KEYWORDS:
        image=""    -   download image or only save the link
                        by default this keyword have "link"
                        parameter which mean, that scrapper
                        will be only save the link, and if
                        you want turn on download option you,
                        schould change that keyword to anyone
                        except "link": expample -a image="asd"

    """
    name = 'amazon_top100'
    allowed_domains = ['amazon.in']
    start_urls = []

    base_url = 'https://www.amazon.in'

    custom_settings = {
        'ITEM_PIPELINES': {
            'amazon_spider.pipelines.AmazonProductPipeline': 300,
            'amazon_spider.pipelines.AmazonProductDump': 301,

        },
        # this is delays between requests(in sec).
        # If you want get faster, you can change it, but it is on your own risk
        'DOWNLOAD_DELAY': 0.5,
    }

    default_stars = {
        'one_star': 1,
        'two_star': 2,
        'three_star': 3,
        'four_star': 4,
        'five_star': 5,
    }

    def __init__(self, *args, **kwargs):
        super(AmazonTop100Spider, self).__init__(*args, **kwargs)

        self.with_rewiews = kwargs.get('reviews', None)
        self.image_manage = kwargs.get('image', 'link')

    def start_requests(self):
        # url = 'https://www.amazon.in/Fashion-Digital-Black-Colour-Watch/dp/B07V1P3Z95/'
        # yield scrapy.Request(url=url, callback=self.parse_product, meta={
        #             'page': 1,
        #         })
        with open('cat.csv') as file:
            for idx, url in enumerate(file.readlines()):
                if idx < 2:
                    continue
                yield scrapy.Request(url=url, callback=self.parse_page_result)
                break

    def parse_page_result(self, response):
        # check the captcha
        error_text = response.xpath('//p[@class="a-last"]/text()').get()
        if error_text == "Sorry, we just need to make sure you're not a robot. " \
                         "For best results, please make sure your browser is accepting cookies.":
            # time.sleep(10)
            user_agent = random.choice(self.settings.get('USER_AGENTS'))
            yield scrapy.Request(url=response.url, callback=self.parse_page_result,
                                 headers={'User-Agent': user_agent},
                                 dont_filter=True, meta=response.meta)

        else:
            blocks = response.css('.zg-item')
            for block in blocks:
                if block.css('.a-icon-small').get():
                    isprime = True
                else:
                    isprime = False
                url = self.base_url + block.css('.a-link-normal::attr(href)').get()
                yield scrapy.Request(url=url, callback=self.parse_product, meta={
                    'isprime': isprime,
                })
            if response.xpath('//li[@class="a-last"]').get():
                url = response.url + '&pg=2'
                yield scrapy.Request(url=url, callback=self.parse_page_result, meta={
                    'keyword': response.meta.get('keyword'),
                })

    def get_review(self, response):
        # get reviews
        item = []
        blocks = response.css('.review-text-content span')[:5]
        dates = response.css('#cm_cr-review_list .review-date')[:5]
        for block, date in zip(blocks, dates):
            rewiev = {
                'date': date.css('::text').get(),
                'text': ' '.join(block.css('::text').getall())
            }
            item.append(rewiev)
        return item

    @inline_requests
    def parse_product(self, response):
        # check the captcha
        error_text = response.xpath('//p[@class="a-last"]/text()').get()
        if error_text == "Sorry, we just need to make sure you're not a robot. " \
                         "For best results, please make sure your browser is accepting cookies.":
            # print('error')
            # time.sleep(10)
            user_agent = random.choice(self.settings.get('USER_AGENTS'))
            yield scrapy.Request(url=response.url, callback=self.parse_product,
                                 headers={'User-Agent': user_agent},
                                 dont_filter=True, meta=response.meta)
        else:
            item = AmazonProductItem()
            item['title'] = response.xpath('//span[@id="productTitle"]/text()').get()
            item['description'] = response.xpath('//*[@id="feature-bullets"]//li//text()').getall()
            if not item['description']:
                item['description'] = response.xpath('//div[@id="bookDescription_feature_div"]/noscript/div/text()').getall()
            if not item['description']:
                item['description'] = response.xpath('//div[@id="productDescription_feature_div"]//p/text()').getall()
            url = response.url
            item['url'] = url[:url.find('/ref') + 1]
            item['price'] = response.xpath('//span[@id="priceblock_dealprice"]//text()').get()
            if not item['price']:
                item['price'] = response.css('#priceblock_ourprice::text').get()
            if not item['price']:
                price_block = response.xpath('//fieldset[@class="forScreenreaders"]//li/@data-p13n-asin-metadata').get()
                if price_block:
                    item['price'] = json.loads(price_block)['price']
            if not item['price']:
                item['price'] = response.css('.price3P::text').get()
            item['asin'] = url[url.find('/dp/') + 4:url.find('/ref')]
            if not item['price']:
                item['price'] = response.css('#priceblock_ourprice::text').get()
            if not item['price']:
                price_block = response.xpath('//fieldset[@class="forScreenreaders"]//li/@data-p13n-asin-metadata').get()
                item['price'] = json.loads(price_block)['price']
            delivery = response.css('#price-shipping-message b::text').get()
            if delivery == 'FREE Delivery':
                item['free_delivery'] = True
            else:
                item['free_delivery'] = False
            item['stars'] = response.xpath('//div[@id="averageCustomerReviews_feature_div"]'
                                           '//span[@id="acrPopover"]/@title').get()
            item['prime'] = response.meta.get('isprime')
            item['keyword'] = response.meta.get('keyword')
            item['reviews'] = response.xpath('//span[@id="acrCustomerReviewText"]/text()').get()
            item['image'] = response.xpath('//div[@id="imageBlock_feature_div"]/script').get()
            item['top_100'] = True
            if response.css('.ac-badge-wrapper'):
                item['is_amazonchoice'] = True
            else:
                item['is_amazonchoice'] = False

            table = response.css('.attrG')
            if table:
                item['product_rank'] = table[0].xpath(
                    '//td[contains(text(), "Amazon Bestsellers Rank")]/following::node()[1]'
                    '//text()').getall()
                if not item['product_rank']:
                    table = response.css('.attrG')
                    item['product_rank'] = table[1].xpath(
                        '//td[contains(text(), "Amazon Bestsellers Rank")]/following::node()[1]'
                        '//text()').getall()
            else:
                    item['product_rank'] = response.xpath('//li[@id="SalesRank"]/text()').getall()
                    item['product_rank'].extend(response.xpath('//li[@id="SalesRank"]/ul//text()').getall())
            item['seller'] = response.xpath('//a[@id="sellerProfileTriggerId"]/text()').get()
            if not item['seller']:
                item['seller'] = 'Amazon'
            # get the links of reviews page and send requests
            table = response.xpath('//td[@class="aok-nowrap"]//@href').getall()
            item['top5_rewiews'] = []
            if self.with_rewiews:
                for idx, elem in enumerate(table):
                    for default_star in self.default_stars:
                        if default_star in elem:
                            url_star = default_star
                    url = self.base_url + elem
                    res = yield scrapy.Request(url=url)
                    item['top5_rewiews'].append(
                        {self.default_stars[url_star]: self.get_review(res)}
                    )
            yield item
