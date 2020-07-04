# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XboxGamesItem(scrapy.Item):
    # define the fields for your item here like:
    # pass
    title = scrapy.Field()
    category = scrapy.Field()
    release = scrapy.Field()
    rating = scrapy.Field()
    review_count = scrapy.Field()
    price_now = scrapy.Field()
    price_original = scrapy.Field()
    price_premium = scrapy.Field()
    identifier = scrapy.Field()
    description = scrapy.Field()
    cover = scrapy.Field()
    link = scrapy.Field()
    publisher = scrapy.Field()
    developer = scrapy.Field()
    
    # last_update = scrapy.Field()
