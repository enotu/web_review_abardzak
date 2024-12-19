# -*- coding:utf8 -*-

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import Join
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from coinmarketcap.items import CurrencyItem

class CurrencyLoader(ItemLoader):
    pass

class WeeklySpider(CrawlSpider):
    name = 'weekly'
    allowed_domains = ['student.psu.ru']
    start_urls = ['student.psu.ru/pls/stu_cus_et/tt_pkg.show_prep?P_TERM=&P_PEO_ID=&P_SDIV_ID='+str(i)+'&P_TY_ID=2024&P_WDAY=&P_WEEK=16']
    only_2018_april_regex = '/201904[0-9]{2}' # full history parsing takes ~4 hrs

    rules = (
        Rule(LinkExtractor(allow=(only_2018_april_regex, )), callback='parse_weekly_report', follow=False),
    )

    def parse_weekly_report(self, response):

        hxs = Selector(response)
        items_html = hxs.xpath('')
        #print(len(items_html),type(items_html),dir(items_html))
        #print(items_html)
        items = []

        item_names = items_html.xpath('/html/body/table/tbody/tr[10]/td[2]').extract()
        item_symbols = items_html.xpath('/html/body/table/tbody/tr[18]/td[3]/div[5]').extract()
        item_caps = items_html.xpath('//td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap"]//p/text()').extract()
        item_prices = items_html.xpath('//td[@class="cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price"]//a/text()').extract()
        print(response.request.url)
        #print(len(item_prices),item_prices)

        for i in range(200):

            item = CurrencyItem()
            item['date'] = response.request.url.split('/')[-2]
            item['name'] = item_names[i]
            item['symbol'] = item_symbols[i]
            item['market_cap'] = item_caps[i]
            item['price'] = item_prices[i]

            yield item