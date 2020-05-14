# -*- coding: utf-8 -*-
import scrapy
from ..items import CategoryurlsItem

class CaturlsSpider(scrapy.Spider):
    name = 'catUrls'
    start_urls = ['https://www.appsandreports.com/all-software-categories']

    def parse(self, response):
        items = CategoryurlsItem()
        all_urls = response.css('div.mt-3 .srchTable a').xpath('@href').extract()
        items['url'] = all_urls
        yield items