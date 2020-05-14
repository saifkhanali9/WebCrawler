# -*- coding: utf-8 -*-
import scrapy
from ..items import CaturlsItem

caturls = []


class CaturlsSpider(scrapy.Spider):
    name = 'caturls'
    allowed_domains = ['trustpilot.com/categories']
    start_urls = ['http://trustpilot.com/categories/']

    def parse(self, response):
        items = CaturlsItem()
        all_urls = response.css('a').xpath('@href').extract()
        items['urls'] = all_urls
        for i in all_urls:
            if '/categories/' in i and i.count('/') == 2:
                caturls.append(i)
        f = open(r'C:\Saif\Office\WebCrawler\trustPilot\Files\caturls.txt', 'w')
        for i in range(0,len(caturls)):
            if i == len(caturls) - 1:
                f.write('https://www.trustpilot.com' + caturls[i])
            else:
                f.write('https://www.trustpilot.com' + caturls[i] + ',,, ')

        yield items
        # all_urls = response.css('.subCategoryItem___3ksKz span'.xpath('@href').extract()
