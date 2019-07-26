# -*- coding: utf-8 -*-
import requests
from scrapy import Spider, Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.request import urljoin
from Nine.items import BookItem
from requests.exceptions import ConnectionError
from urllib.request import urljoin
from urllib.parse import quote
import string


class SpiderSpider(CrawlSpider):
    name = 'spider'
    allowed_domains = ['qishu.cc']
    start_urls = ['http://www.qishu.cc/']
    base_url = 'http://www.qishu.cc/'
    rules = [
        Rule(LinkExtractor(allow=r'/\w+/list\d+_1.html$')),
        # 起始位置如何定位？
        Rule(LinkExtractor(restrict_xpaths='//var[@class="morePage"]/code/a[@class="active"]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//var[@class="morePage"]/dfn'), follow=True),
        Rule(LinkExtractor(allow=r'/txt/\d+\.html$'), callback='parse_detail', follow=True)
    ]


    def parse_detail(self, response):
        item = BookItem()
        item['book_title'] = response.xpath('//dl[@id="downInfoArea"]/dt[@id="downInfoTitle"]/text()').get().split('T')[0]
        book_info = response.xpath('//dd[@class="downInfoRowL"]//text()').getall()
        item['book_type'] = book_info[7]
        item['author'] = book_info[10]
        item['book_intro'] = ''.join(response.xpath('//div[@id="mainSoftIntro"]//text()').getall()[1:]).strip()
        download_url = response.xpath('//div[@id="downAddress"]/a[2]/@href').get()
        new_url = quote(download_url, safe=string.printable)
        item['download_url'] = new_url
        item['file_path'] = ''
        item['section'] = ''
        yield item








# class SpiderSpider(CrawlSpider):
#     name = 'spider'
#     allowed_domains = ['qisuu.la']
#     start_urls = ['https://www.qisuu.la/']
#     base_url = 'https://www.qisuu.la/'
#     rules = [
#         Rule(LinkExtractor(allow=r'/\w+/sort\d+/$')),
#         # 起始位置如何定位？
#         Rule(LinkExtractor(allow=r'/\w+/sort\d+/index_\d+\.html$'),callback='parse_index', follow=True),
#         Rule(LinkExtractor(allow=r'/Shtml\d+\.html$'), callback='parse_detail', follow=True),
#     ]
#
#
#     def parse_index(self, response):
#         item = BookItem()
#         book_type = response.xpath('//div[@class="listTab"]/h1/text()').get()
#         book_items = response.xpath('//div[@class="listBox"]/ul//li')
#         for book_item in book_items:
#             item['book_type'] = book_type
#             book_info = book_item.xpath('./div[@class="s"]/text()').getall()
#             item['author'] = book_info[0]
#             item['book_size'] = book_info[1]
#             item['book_title'] = book_item.xpath('./a/text()').get()
#             item['book_intro'] = book_item.xpath('./div[@class="u"]/text()').get()
#             item['newset_chapter'] = book_item.xpath('./div/a/text()').get()
#             item['book_img'] = urljoin(self.base_url, book_item.xpath('./a/img/@src').get())
#             # yield item
#
#
#     def parse_detail(self, response):
#         url_content = response.xpath('//div[@class="showDown"]/ul/li/script/text()').get()
#         download_url = url_content.split(',')[1]
#         new_url = quote(download_url, safe=string.printable)
#         print(new_url)
#
#
