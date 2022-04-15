# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item

class Test1Item(Item):
    #content = Field(serializer=content_serializer)
    building_name = scrapy.Field()
    unit = scrapy.Field()
    beds = scrapy.Field()
    baths = scrapy.Field()
    price = scrapy.Field()
    url_py = scrapy.Field()
    price_min = scrapy.Field()
    free_month = scrapy.Field()
    lease_month = scrapy.Field()


