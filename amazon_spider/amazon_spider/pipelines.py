# -*- coding: utf-8 -*-
"""
After scrapy getting data from site, he comes here - here scrapy format the data and download the image
If you want to create new function for edding the data, you should add new "if block" in "process_item"
function, and pass it
"""
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import mysql.connector
import json


class AmazonProductPipeline(ImagesPipeline):
    def process_item(self, item, spider):
        if item.get('name'):
            item['name'] = item.get('name').strip()
        if item.get('description'):
            item['description'] = self.parse_desc(item.get('description'))
        if item.get('product_rank'):
            item['product_rank'] = self.parse_product_rank(item.get('product_rank'))
        if item.get('image'):
            item['image'] = self.parse_image(item.get('image'))
        if not item.get('is_freedelivery'):
            item['is_freedelivery'] = False
        if not item.get('is_amazonchoice'):
            item['is_amazonchoice'] = False
        if not item.get('is_prime'):
            item['is_prime'] = False
        if not item.get('sponsored'):
            item['sponsored'] = False
        # If you want add new function for data edding
        # Example:
        # if item.get('FIELD WHICH YOU NEED TO EDIT'):
        #   item['FIELD WHICH YOU NEED TO EDIT'] = self.CUSTOM_FUNCTION(...)
        return super(ImagesPipeline, self).process_item(item, spider)

    # def COSTOM_FUNC(self, ...):
    #   pass

    def parse_image(self, item):
        item = dict(json.loads(item))
        return list(item.keys())[0]

    def parse_desc(self, item):
        item = ''.join(item)
        item = item.replace('\t', '')
        return item

    def parse_product_rank(self, item):
        for idx, _ in enumerate(item):
            item[idx] = item[idx].replace('\n', '')
            item[idx] = item[idx].strip()
        item = ' '.join(item)
        return item

    def get_media_requests(self, item, info):
        if item['name'] and info.spider.image_manage != 'link':
            yield scrapy.Request(item['image'], meta={'item': item})
        else:
            return item

    def image_downloaded(self, response, request, info):
        for path, image, buf in self.get_images(response, request, info):
            if not response.meta['item']['image']:
                return
            name = response.meta['item']['name'].replace('/', '-')
            file_name = name + '_' + str(response.meta['item']['asin'])
            path = '{}.jpg'.format(file_name)
            self.store.persist_file(
                path, buf, info,
                headers={'Content-Type': 'image/jpeg'})
        return response.meta['item']


class AmazonProductDump(object):
    """
    Class for connect to DB.
    Change settings for you in "create_connection" func

    """

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        """
        Change settings for your connection to MySql
        """
        self.conn = mysql.connector.connect(
            host='localhost',
            user='demouser',
            passwd='demopassword',
            database='demodb'
        )
        self.curr = self.conn.cursor()

    def create_table(self):
        """
        Here i create the table
        and dump the data into base
        """
        self.curr.execute(
            """
            CREATE TABLE IF NOT EXISTS demodb(
                asin text,
                product_name text,
                descriprion text,
                url text,
                price text,
                image_url text,
                product_review_stars text,
                seller text,
                reviews text,
                is_prime text,
                is_amazonchoice text,
                if_freedelivery text,
                product_rank text,
                top5_reviews text,
                is_sponsored text,
                sponsored_pos text,
                sponsored_page text,
                keyword text
            )
            """
        )

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        if item['name']:
            for key in item:
                item[key] = json.dumps(item[key])

        if item['name']:
            self.curr.execute(
                """SELECT * FROM demodb
                    WHERE asin = (%s)""", (
                    item['asin'],
            ))
            row = self.curr.fetchone()
            if row:
                return
            self.curr.execute(
                """INSERT INTO demodb values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                    item['asin'],
                    item['name'],
                    item['description'],
                    item['url'],
                    item['price'],
                    item['image'],
                    item['stars'],
                    item['seller'],
                    item['reviews'],
                    item['is_prime'],
                    item['is_amazonchoice'],
                    item['is_freedelivery'],
                    item['product_rank'],
                    item['top5_rewiews'],
                    item['sponsored'],
                    item['sponsored_pos'],
                    item['sponsored_page'],
                    item['keyword']
            ))
            self.conn.commit()
