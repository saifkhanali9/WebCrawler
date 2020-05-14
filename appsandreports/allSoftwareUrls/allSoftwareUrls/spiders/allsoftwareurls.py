# -*- coding: utf-8 -*-
import json
import scrapy
from ..items import AllsoftwareurlsItem
from time import sleep

path = r'C:\Saif\Office\Python Projects\Crawler\appsandreports\categoryUrls\urls.json'


class AllsoftwareurlsSpider(scrapy.Spider):
    with open(path) as f:
        d = json.load(f)
        all_urls = d[0]['url']
    name = 'allsoftwareurls'
    page_number = 1
    urlIndex = 0
    a = []
    for i in range(len(all_urls)):
        a.append(all_urls[i])
    start_urls = [a[0]]
    current_url = a

    def parse(self, response):
        items = AllsoftwareurlsItem()
        incrementCheck = 0
        urls = response.css(' .mt-2:nth-child(1)').xpath('@href').extract()
        next_page_link = response.css('.active~ .page-item+ .page-item .page-link').xpath('@href').extract()
        items['urls'] = urls
        yield items

        if len(next_page_link) > 0:
            next_page_link = next_page_link[-1]
        else:
            if AllsoftwareurlsSpider.urlIndex == len(AllsoftwareurlsSpider.a) - 1:
                temp = ''
            else:
                AllsoftwareurlsSpider.urlIndex += 1
            AllsoftwareurlsSpider.page_number = 1
            incrementCheck = 1
        if AllsoftwareurlsSpider.urlIndex < len(AllsoftwareurlsSpider.a):
            if incrementCheck == 1:
                incrementCheck = 0
            else:
                AllsoftwareurlsSpider.page_number += 1
            sleep(4)
            next_page = AllsoftwareurlsSpider.a[AllsoftwareurlsSpider.urlIndex] + '?per_page=' + str(
                AllsoftwareurlsSpider.page_number)
            yield response.follow(next_page, callback=self.parse)
