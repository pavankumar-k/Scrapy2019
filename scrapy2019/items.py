# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class scrapy2019Item(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    subtitle = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    author = scrapy.Field()
    affli = scrapy.Field()
    event = scrapy.Field()
    session = scrapy.Field()
    topics = scrapy.Field()
    date = scrapy.Field()
    citation = scrapy.Field()
    disc = scrapy.Field()