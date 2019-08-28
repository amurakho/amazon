from scrapy.crawler import CrawlerProcess
from amazon_spider.spiders.amazon_product import AmazonProductSpider
import tkinter as tk

def scrape():
    process = CrawlerProcess(
        {
            # just need to add new field
            'USER_AGENTS': [
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/601.4.4 (KHTML, like Gecko)'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/601.5.17 (KHTML, like Gecko)'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/601.5.17 (KHTML, like Gecko) Version/9.1 Safari/537.86.5'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.2.5 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.5'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.6.17 (KHTML, like Gecko) Version/9.1.1 Safari/601.6.17'),
                ('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.8 (KHTML, like Gecko) Safari/312.6'),
                ('Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-us) AppleWebKit/531.9 (KHTML, like Gecko) Version/4.0.3 Safari/531.9'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7'),
                ('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/412.7 (KHTML, like Gecko) Safari/412.5 '),
                ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'),
                ('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/312.1 (KHTML, like Gecko) Safari/312'),
                ('Mozilla/5.0 (Macintosh; U; PPC Mac OS X; en) AppleWebKit/418.8 (KHTML, like Gecko) Safari/419.3'),
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
            ],

            # the path for image store
            'IMAGES_STORE': 'images',

            # if you dont use proxy turn on it to True and add proxies to proxy list
            'ROTATED_PROXY_ENABLED': False,

            # # Proxy list
            # 'HTTP_PROXIES': [
            #     'http://user:pass@proxy1:8888',
            # ]
            # ,
            # 'HTTPS_PROXIES': [
            #     'https://user:pass@proxy1:8888',
            # ],

            'DOWNLOADER_MIDDLEWARES': {
                'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
                'scrapy_rotated_proxy.downloadmiddlewares.proxy.RotatedProxyMiddleware': 750,
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            },
            'ROBOTSTXT_OBEY': False,
        }
    )
    # keyword = 'shoes'
    process.crawl(AmazonProductSpider, keyword=str(keyword.get()))
    # process.crawl(AmazonProductSpider, keyword=keyword)
    process.start()


win = tk.Tk()

win.title('SCRAPER')

win.geometry('300x200+0+0')


keyword = tk.StringVar()

entry = tk.Entry(win, textvariable=keyword, width=33).place(x=10, y=50)
download_image = tk.IntVar()
check = tk.Checkbutton(win, text='download image', variable=download_image)


tk.Button(win, text='Scrape!', command=scrape).pack()


win.mainloop()


# scrape()