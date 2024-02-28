# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReviewscraperItem(scrapy.Item):
    restaurant_name = scrapy.Field()
    rating = scrapy.Field()
    quote = scrapy.Field()
    number = scrapy.Field()
    review = scrapy.Field()
    website = scrapy.Field()
    pass
