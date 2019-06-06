# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose
class CompanyItem(scrapy.Item):
    s_id = scrapy.Field()
    s_name = scrapy.Field()
    s_acro = scrapy.Field()
    s_isin = scrapy.Field()
    s_indus = scrapy.Field()