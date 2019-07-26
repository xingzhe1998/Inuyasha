# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item,Field


class BookItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    book_type = Field()
    book_title = Field()
    author = Field()
    # book_size = Field()
    book_intro = Field()
    # book_img = Field()
    download_url = Field()
    section = Field()
    file_path = Field()




