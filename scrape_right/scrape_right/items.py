# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):

    language = scrapy.Field()
    url = scrapy.Field()
    authors = scrapy.Field()
    pub_datetime = scrapy.Field()
    modified_datetime = scrapy.Field()
    title = scrapy.Field()
    lead = scrapy.Field()
    text_blob = scrapy.Field()
    source = scrapy.Field()
    category = scrapy.Field()
