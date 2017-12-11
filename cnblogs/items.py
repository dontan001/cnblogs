# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CnblogsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 定义容器
class WordItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    body = scrapy.Field()
