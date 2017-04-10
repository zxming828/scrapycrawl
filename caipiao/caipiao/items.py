# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SSQItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = scrapy.Field()
    red = scrapy.Field()
    blue = scrapy.Field()

class DLTItem(scrapy.Item):
    date = scrapy.Field()
    red = scrapy.Field()
    blue = scrapy.Field()
