# -*- coding: utf-8 -*-
import scrapy
from ..items import AmazonProductItem
import time
from inline_requests import inline_requests
from scrapy.utils.project import get_project_settings
import random
import json

class AmazonProductSpider(scrapy.Spider):
    """
    KEYWORDS:
        keyword=""  -   which product you want to scrape

        image=""    -   download image or only save the link
                        by default this keyword have "link"
                        parameter which mean, that scrapper
                        will be only save the link, and if
                        you want turn on download option you,
                        schould change that keyword to anyone
                        except "link": expample -a image="asd"

        pages=""    -   max count of page, what you want to scrape

    """
    name = 'amazon_product'
    allowed_domains = ['amazon.in']

    base_url = 'https://www.amazon.in'

    start_urls = [
        'https://www.example.com'
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'amazon_spider.pipelines.AmazonProductPipeline': 300,
            'amazon_spider.pipelines.AmazonProductDump': 301,

        },
        # this is delays between requests(in sec).
        # If you want get faster, you can change it, but it is on your own risk

        # Write now i know, that you can make delay to 0.5 sec!! So it will be faster
        'DOWNLOAD_DELAY': 0.5,
    }
    settings = get_project_settings()

    default_stars = {
        'one_star': 1,
        'two_star': 2,
        'three_star': 3,
        'four_star': 4,
        'five_star': 5,
    }

    def __init__(self, *args, **kwargs):
        super(AmazonProductSpider, self).__init__(*args, **kwargs)

        self.keyword = kwargs.get('keyword', None)
        self.image_manage = kwargs.get('image', 'link')
        self.max_pages = kwargs.get('pages', None)

    def parse(self, response):
        # For test!
        url = 'https://www.amazon.in/HP-Chromebook-Touchscreen-180-degree-14-ca002TU/dp/B07QNM5LZ5/'
        yield scrapy.Request(url=url, callback=self.parse_product, meta={
            'page': 1,
            'keyword': self.keyword
        })

        # # next we create the request for our keyword
        # if self.keyword:
        #     searching_url = 'https://www.amazon.in/s?k={}'
        #     url = searching_url.format(self.keyword)
        #     yield scrapy.Request(url=url, callback=self.parse_page_result, meta={
        #                                                                         'page': 1,
        #                                                                          'keyword': self.keyword
        #                                                                          })

    def parse_page_result(self, response):

        # check the captcha
        error_text = response.xpath('//p[@class="a-last"]/text()').get()
        if error_text == "Sorry, we just need to make sure you're not a robot. " \
                         "For best results, please make sure your browser is accepting cookies.":
            # time.sleep(15)
            user_agent = random.choice(self.settings.get('USER_AGENTS'))
            yield scrapy.Request(url=response.url, callback=self.parse_page_result,
                                 headers={'User-Agent': user_agent},
                                 dont_filter=True, meta=response.meta)
        else:
            # we take all results from page
            blocks = response.css('.s-result-item')
            page = response.meta.get('page')
            # passing all blocks, get the info, and pass request to the product page
            for block in blocks:
                asin = block.xpath('@data-asin').get()
                if not asin:
                    continue
                if block.css('.a-spacing-micro .a-color-secondary').get():
                    sponsored = True
                    page_number = page
                    position = block.xpath('@data-index').get()
                else:
                    sponsored = False
                    page_number = None
                    position = None
                if block.css('.s-prime .a-icon-medium').get():
                    isprime = True
                else:
                    isprime = False
                if block.css('.s-align-children-center .s-align-children-center+ .a-row span').get():
                    freedelivery = True
                else:
                    freedelivery = False
                url = self.base_url + block.css('.a-size-mini a::attr(href)').get()
                yield scrapy.Request(url, callback=self.parse_product, meta={
                                                                            'sponsored': sponsored,
                                                                            'isprime': isprime,
                                                                            'freedelivery': freedelivery,
                                                                            'page_number': page_number,
                                                                            'position': position,
                                                                            'asin': asin,
                                                                            'keyword': response.meta.get('keyword'),
                                                                                },
                                     dont_filter=True)
            # pagination
            if response.xpath('//li[@class="a-last"]').get() and page != self.max_pages:
                page += 1
                url = 'https://www.amazon.in/s?k={}&page={}'.format(response.meta.get('keyword'), page)
                yield scrapy.Request(url=url, callback=self.parse_page_result, meta={
                                                                                    'keyword': response.meta.get('keyword'),
                                                                                    'page': page
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
            # time.sleep(15)
            user_agent = random.choice(self.settings.get('USER_AGENTS'))
            yield scrapy.Request(url=response.url, callback=self.parse_product,
                                 headers={'User-Agent': user_agent},
                                 dont_filter=True, meta=response.meta)
        else:
            item = AmazonProductItem()
            item['name'] = response.xpath('//span[@id="productTitle"]/text()').get()
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
            item['is_freedelivery'] = response.meta.get('freedelivery')
            item['asin'] = response.meta.get('asin')
            item['stars'] = response.xpath('//div[@id="averageCustomerReviews_feature_div"]'
                                           '//span[@id="acrPopover"]/@title').get()
            item['sponsored'] = response.meta.get('sponsored')
            item['sponsored_page'] = response.meta.get('page_number')
            item['sponsored_pos'] = response.meta.get('position')
            item['is_prime'] = response.meta.get('isprime')
            item['keyword'] = response.meta.get('keyword')
            item['reviews'] = response.xpath('//span[@id="acrCustomerReviewText"]/text()').get()
            item['image'] = response.xpath('//div[@id="imgTagWrapperId"]/img/@data-a-dynamic-image').get()
            if not item['image']:
                item['image'] = response.xpath('//img[@id="imgBlkFront"]//@data-a-dynamic-image').get()
            item['top_100'] = False
            if response.css('.ac-badge-wrapper'):
                item['is_amazonchoice'] = True
            else:
                item['is_amazonchoice'] = False

            table = response.css('.attrG')
            if table:
                item['product_rank'] = table[0].xpath('//td[contains(text(), "Amazon Bestsellers Rank")]/following::node()[1]'
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
