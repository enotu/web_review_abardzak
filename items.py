import scrapy

class CurrencyItem(scrapy.Item):
    lector = scrapy.Field()
    groups = scrapy.Field()
    auditory = scrapy.Field()
    course = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()