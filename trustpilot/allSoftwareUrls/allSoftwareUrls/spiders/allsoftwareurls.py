# -*- coding: utf-8 -*-
import json
import scrapy
from ..items import AllsoftwareurlsItem
from time import sleep
import urllib.request
import urllib.request

path = r'C:\Saif\Office\WebCrawler\trustPilot\Files\caturls.txt'
f = open(path, 'r')
line = f.readlines()
lines = line[0].split(',,, ')
# print(lines)
# lines = ['https://www.trustpilot.com/categories/gaming_service_provider']
line = []
swurlArray = []


class AllsoftwareurlsSpider(scrapy.Spider):
    paginationCounter = 1
    name = 'allsoftwareurls'
    # allowed_domains = ['example.com']
    index = 0
    # for i in range(3):
    #     a.append(lines[i])
    start_urls = [lines[0]]
    urlFound = 5

    def parse(self, response):
        items = AllsoftwareurlsItem()
        print("INDEX", AllsoftwareurlsSpider.index)
        swurlArray = []
        urls = response.css('.businessUnitCardsContainer___Qhix1 a').xpath('@href').extract()
        # AllsoftwareurlsSpider.urlFound = len(urls)
        print('\n\n\n\n', len(urls), '\n\n\n\n')
        # Getting Category
        cat = lines[AllsoftwareurlsSpider.index].split('.com/categories/')
        cat = cat[1]
        for i in urls:
            swurlArray.append('https://www.trustpilot.com/' + i + ',,,,,' + cat)
        items['urls'] = swurlArray
        yield items
        print("Index: ", AllsoftwareurlsSpider.index, " Length: ", len(lines))
        next_pagination = response.css(".paginationLinkNext___1LQ14").extract()
        print("\n\n\nNextPage", next_pagination)

        # To handle redirection
        if len(next_pagination) > 0:
            temp = AllsoftwareurlsSpider.paginationCounter + 1
            next_pagination = lines[AllsoftwareurlsSpider.index] + '?page=' + str(temp)
            resp = urllib.request.urlopen(next_pagination)
            openedUrl = resp.geturl()
            if openedUrl != next_pagination:
                # print("\n\n\n\n1:", openedUrl, "\n\n\n\n2:", resp)
                next_pagination = []
        if len(next_pagination) > 0 and len(urls) > 5:
            # next_pagination = lines[AllsoftwareurlsSpider.index] + next_pagination[0]
            AllsoftwareurlsSpider.paginationCounter += 1
            next_pagination = lines[AllsoftwareurlsSpider.index] + '?page=' + str(
                AllsoftwareurlsSpider.paginationCounter)
            print(next_pagination)
            sleep(1)
            # Check if it's not being redirected
            yield response.follow(next_pagination, callback=self.parse)
        elif AllsoftwareurlsSpider.index < len(lines) - 1:
            AllsoftwareurlsSpider.paginationCounter = 1
            AllsoftwareurlsSpider.index += 1
            sleep(1)
            next_page = lines[AllsoftwareurlsSpider.index]
            print(next_page)
            yield response.follow(next_page, callback=self.parse)
